import os
import shutil
import time
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import eyed3

# Folder default = folder tempat skrip berada
MUSIC_DIR = os.path.dirname(os.path.abspath(__file__))

# Ekstensi audio yang didukung
AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.aac', '.alac', '.ogg', '.wav']

# File log
LOG_FILE = os.path.join(MUSIC_DIR, "LOG_EmbedLRC.txt")

def embed_lyrics(directory):
    audio_files = []
    failed_files = []
    embedded_count = 0

    # Cari semua audio file sesuai ekstensi
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
                audio_files.append(os.path.join(root, file))

    total_files = len(audio_files)
    if total_files == 0:
        print("Tidak ada file audio ditemukan.")
        return

    print(f"Total audio file ditemukan: {total_files}")
    print("Start embedding... (1 detik)")
    time.sleep(1)

    for idx, audio_path in enumerate(audio_files, 1):
        file_name = os.path.basename(audio_path)
        ext = os.path.splitext(file_name)[1].lower()
        lrc_file_name = os.path.splitext(file_name)[0] + '.lrc'
        lrc_path = os.path.join(os.path.dirname(audio_path), lrc_file_name)

        # Persentase progress
        percent = int(idx / total_files * 100)

        if not os.path.exists(lrc_path):
            print(f"Embedding LRC: {percent}% | {idx}/{total_files} | FAIL | {file_name}")
            failed_files.append(file_name)
            continue

        try:
            if ext == '.flac':
                audio = FLAC(audio_path)
                audio['LYRICS'] = open(lrc_path, 'r', encoding='utf-8').read()
                audio.save()
            elif ext == '.mp3':
                audio = eyed3.load(audio_path)
                if audio.tag is None:
                    audio.initTag()
                audio.tag.lyrics.set(open(lrc_path, 'r', encoding='utf-8').read())
                audio.tag.save(version=eyed3.id3.ID3_V2_3)
            elif ext in ['.m4a', '.mp4', '.alac', '.aac']:
                audio = MP4(audio_path)
                audio.tags['\xa9lyr'] = open(lrc_path, 'r', encoding='utf-8').read()
                audio.save()
            else:
                print(f"Embedding LRC: {percent}% | {idx}/{total_files} | FAIL | {file_name} (format tidak didukung)")
                failed_files.append(file_name)
                continue

            print(f"Embedding LRC: {percent}% | {idx}/{total_files} | SUCCESS | {file_name}")
            embedded_count += 1

        except Exception as e:
            print(f"Embedding LRC: {percent}% | {idx}/{total_files} | FAIL | {file_name}")
            failed_files.append(file_name)
            if os.path.exists(lrc_path):
                shutil.move(lrc_path, lrc_path + ".failed")

        time.sleep(0.1)  # jeda antar file

    # Tulis log untuk file gagal
    if failed_files:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("Lagu tanpa .lrc atau gagal embed:\n")
            for song in failed_files:
                f.write(f"{song}\n")
        print(f"\nList Lagu tanpa .lrc bisa dilihat di {LOG_FILE}")

    print(f"\nTotal diproses: {total_files}")
    print(f"Berhasil embed: {embedded_count}")
    print(f"Gagal embed: {len(failed_files)}")

    # Prompt hapus LRC
    if embedded_count > 0:
        print("\nLyric sudah di Embed ke Lagu")
        delete_lrc = input("Hapus File .lrc ?\ny (yes) n (no): ").strip().lower()
        if delete_lrc == 'y':
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.lrc'):
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            pass
            print("Semua file .lrc berhasil dihapus.")
        else:
            print("File .lrc tetap disimpan.")


if __name__ == "__main__":
    embed_lyrics(MUSIC_DIR)
