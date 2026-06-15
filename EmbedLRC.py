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
    failed_files = []
    successful_lrcs = []
    embedded_count = 0

    # UI Header
    print("=" * 50)
    print("           LRC EMBEDDER (MUTAGEN ONLY)            ")
    print("=" * 50)
    print("Mencari file audio di direktori...")

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
    print("[INFO] Memulai proses embedding...\n")
    time.sleep(0.5)

    for idx, audio_path in enumerate(audio_files, 1):
        file_name = os.path.basename(audio_path)
        ext = os.path.splitext(file_name)[1].lower()
        lrc_file_name = os.path.splitext(file_name)[0] + '.lrc'
        lrc_path = os.path.join(os.path.dirname(audio_path), lrc_file_name)

        # Kalkulasi persentase
        percent = int(idx / total_files * 100)
        # Format string untuk menjaga UI tetap rata
        progress_str = f"[{percent:3}%]"

        if not os.path.exists(lrc_path):
            print(f"{progress_str} 🟡 SKIP   | {file_name} (LRC tidak ditemukan)")
            failed_files.append(f"{file_name} (Missing .lrc)")
            continue

        try:
            with open(lrc_path, 'r', encoding='utf-8') as f:
                lyrics_text = f.read()

            if ext == '.flac':
                audio = FLAC(audio_path)
                audio['LYRICS'] = lyrics_text
                audio.save()
                
            elif ext == '.mp3':
                # Implementasi Mutagen untuk MP3 (menggunakan frame USLT)
                try:
                    audio = ID3(audio_path)
                except ID3NoHeaderError:
                    # Jika file MP3 belum punya tag sama sekali, buat baru
                    audio = ID3()
                
                # Hapus lirik lama jika ada untuk mencegah duplikasi/bentrok
                audio.delall("USLT") 
                # Masukkan lirik baru (encoding=3 adalah UTF-8)
                audio.add(USLT(encoding=3, lang='ind', desc='', text=lyrics_text))
                audio.save(audio_path, v2_version=3) # Simpan sebagai ID3v2.3 (paling kompatibel)
                
            elif ext in ['.m4a', '.aac', '.alac']:
                audio = MP4(audio_path)
                audio.tags['\xa9lyr'] = lyrics_text
                audio.save()

            print(f"{progress_str} 🟢 SUKSES | {file_name}")
            embedded_count += 1
            successful_lrcs.append(lrc_path)

        except Exception as e:
            print(f"{progress_str} 🔴 ERROR  | {file_name} -> {str(e)}")
            failed_files.append(f"{file_name} (Error: {str(e)})")
            
            if os.path.exists(lrc_path):
                try:
                    shutil.move(lrc_path, lrc_path + ".failed")
                except OSError:
                    pass

    # UI Footer / Ringkasan
    print("\n" + "=" * 50)
    print("                 RINGKASAN HASIL                  ")
    print("=" * 50)
    print(f"Total diproses : {total_files}")
    print(f"Berhasil embed : {embedded_count}")
    print(f"Gagal/Skip     : {len(failed_files)}\n")

    # Tulis log jika ada yang gagal
    if failed_files:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("Daftar file tanpa .lrc atau error:\n")
            f.write("-" * 40 + "\n")
            for song in failed_files:
                f.write(f"{song}\n")
        print(f"[INFO] List lagu gagal/skip dicatat di: {LOG_FILE}\n")

    # Prompt Hapus LRC
    if embedded_count > 0:
        print("Lyric sudah berhasil di-embed ke Lagu.")
        delete_lrc = input("Hapus File .lrc yang SUKSES di-embed?\ny (yes) n (no): ").strip().lower()
        
        if delete_lrc == 'y':
            for lrc in successful_lrcs:
                try:
                    os.remove(lrc)
                except OSError:
                    pass
            print("[✓] File .lrc yang berhasil di-embed telah dihapus.")
        else:
            print("[-] File .lrc tetap disimpan.")

if __name__ == "__main__":
    embed_lyrics(MUSIC_DIR)
