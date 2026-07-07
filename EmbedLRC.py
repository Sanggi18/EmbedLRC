import os
import shutil
import time
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, USLT, ID3NoHeaderError

# Folder default = folder tempat skrip berada
MUSIC_DIR = os.path.dirname(os.path.abspath(__file__))

# Ekstensi audio yang didukung (Format yang umum dipakai)
AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.aac', '.alac']

# File log
LOG_FILE = os.path.join(MUSIC_DIR, "LOG_EmbedLRC.txt")

def embed_lyrics(directory):
    audio_files = []
    successful_lrcs = []
    embedded_count = 0
    skip_count = 0
    error_count = 0

    # Dictionary untuk menyimpan log per folder
    # Format: { '/path/to/folder': { 'folder_name': 'nama_folder', 'logs': [] } }
    log_records = {}

    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    print("           EmbedLRC (MUTAGEN / ID3)           ")
    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    
    print("Mencari file audio di direktori...")
    time.sleep(1)

    # Cari semua audio file
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
                audio_files.append(os.path.join(root, file))

    total_files = len(audio_files)
    if total_files == 0:
        print("[!] Tidak ada file audio ditemukan.")
        return

    print(f"[INFO] Total file audio ditemukan: {total_files}")
    time.sleep(1)
    print("[INFO] Memulai proses embedding...\n")
    time.sleep(3)

    print("PROCESSING")

    for audio_path in audio_files:
        file_name = os.path.basename(audio_path)
        dir_path = os.path.dirname(audio_path)
        folder_name = os.path.basename(dir_path)
        ext = os.path.splitext(file_name)[1].lower()
        lrc_file_name = os.path.splitext(file_name)[0] + '.lrc'
        lrc_path = os.path.join(dir_path, lrc_file_name)

        # Inisialisasi dictionary jika folder belum ada
        if dir_path not in log_records:
            log_records[dir_path] = {'folder_name': folder_name, 'logs': []}

        if not os.path.exists(lrc_path):
            # Hapus keterangan [LRC Tidak Ditemukan] di terminal
            print(f" 🟡 SKIP   | {file_name}")
            # Tapi tetap catat alasannya di log
            log_records[dir_path]['logs'].append(f"[SKIP] {file_name} [Missing .lrc]")
            skip_count += 1
            time.sleep(0.01)
            continue

        try:
            with open(lrc_path, 'r', encoding='utf-8') as f:
                lyrics_text = f.read()

            if ext == '.flac':
                audio = FLAC(audio_path)
                audio['LYRICS'] = lyrics_text
                audio.save()
                
            elif ext == '.mp3':
                try:
                    audio = ID3(audio_path)
                except ID3NoHeaderError:
                    audio = ID3()
                audio.delall("USLT") 
                audio.add(USLT(encoding=3, lang='ind', desc='', text=lyrics_text))
                audio.save(audio_path, v2_version=3)
                
            elif ext in ['.m4a', '.aac', '.alac']:
                audio = MP4(audio_path)
                audio.tags['\xa9lyr'] = lyrics_text
                audio.save()

            print(f" 🟢 SUKSES | {file_name}")
            log_records[dir_path]['logs'].append(f"[SUCCES] {file_name}")
            embedded_count += 1
            successful_lrcs.append(lrc_path)
            time.sleep(0.01)

        except Exception as e:
            error_msg = str(e) if str(e) else "Metadata Error / Invalid"
            # Hapus keterangan error di terminal agar rapi
            print(f" 🔴 ERROR  | {file_name}")
            # Tapi tetap catat error spesifiknya di log
            log_records[dir_path]['logs'].append(f"[ERROR] {file_name} [{error_msg}]")
            error_count += 1
            time.sleep(0.01)
            
            if os.path.exists(lrc_path):
                try:
                    shutil.move(lrc_path, lrc_path + ".failed")
                except OSError:
                    pass

    # Penulisan File Log Detail per Folder
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("LOG EmbedLRC\n\n")
        for d_path, data in log_records.items():
            f.write(f"Folder: {data['folder_name']}\n")
            f.write(f"Path: ({d_path})\n")
            f.write("-" * 41 + "\n")
            for log_line in data['logs']:
                f.write(f"{log_line}\n")
            f.write("\n")

    # UI Footer / Ringkasan
    time.sleep(1)
    print("\n" + "=" * 50)
    time.sleep(1)
    print("                 RINGKASAN HASIL                  ")
    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    
    print("")
    time.sleep(1)
    print(f"Total diproses : {total_files}")
    time.sleep(1)
    print(f"Berhasil embed : {embedded_count}")
    time.sleep(1)
    print(f"Gagal/Skip     : {skip_count + error_count}")
    time.sleep(3)

    print(f"\n[INFO] List lagu beserta status dicatat di: {LOG_FILE}")
    time.sleep(0.5)

    # Prompt Hapus LRC
    if embedded_count > 0:
        print("\nLyric sudah berhasil di-embed ke Lagu.")
        time.sleep(0.5)
        
        delete_lrc = input("Hapus File .lrc yang SUKSES di-embed?\ny (yes) n (no): ").strip().lower()
        time.sleep(0.5)
        
        if delete_lrc == 'y':
            for lrc in successful_lrcs:
                try:
                    os.remove(lrc)
                except OSError:
                    pass
            print("\n[✓] File .lrc yang berhasil di-embed telah dihapus.")
            time.sleep(2)
        else:
            print("\n[-] File .lrc tetap disimpan.")
            time.sleep(2)

if __name__ == "__main__":
    embed_lyrics(MUSIC_DIR)
