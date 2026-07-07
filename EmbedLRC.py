import os
import shutil
import time
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, USLT, ID3NoHeaderError

# Default directory = the folder where the script is located
MUSIC_DIR = os.path.dirname(os.path.abspath(__file__))

# Supported audio extensions (Commonly used formats)
AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.aac', '.alac']

# Log file
LOG_FILE = os.path.join(MUSIC_DIR, "LOG_EmbedLRC.txt")

def embed_lyrics(directory):
    audio_files = []
    successful_lrcs = []
    embedded_count = 0
    skip_count = 0
    error_count = 0

    # Dictionary to store logs per folder
    # Format: { '/path/to/folder': { 'folder_name': 'folder_name', 'logs': [] } }
    log_records = {}

    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    print("           EmbedLRC (MUTAGEN / ID3)           ")
    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    
    print("Searching for audio files in the directory...")
    time.sleep(1)

    # Find all audio files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
                audio_files.append(os.path.join(root, file))

    total_files = len(audio_files)
    if total_files == 0:
        print("[!] No audio files found.")
        return

    print(f"[INFO] Total audio files found: {total_files}")
    time.sleep(1)
    print("[INFO] Starting the embedding process...\n")
    time.sleep(3)

    print("PROCESSING")

    for audio_path in audio_files:
        file_name = os.path.basename(audio_path)
        dir_path = os.path.dirname(audio_path)
        folder_name = os.path.basename(dir_path)
        ext = os.path.splitext(file_name)[1].lower()
        lrc_file_name = os.path.splitext(file_name)[0] + '.lrc'
        lrc_path = os.path.join(dir_path, lrc_file_name)

        # Initialize dictionary if the folder doesn't exist
        if dir_path not in log_records:
            log_records[dir_path] = {'folder_name': folder_name, 'logs': []}

        if not os.path.exists(lrc_path):
            # Remove [LRC Not Found] message in the terminal to keep it clean
            print(f" 🟡 SKIP    | {file_name}")
            # But still record the reason in the log
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

            print(f" 🟢 SUCCESS | {file_name}")
            log_records[dir_path]['logs'].append(f"[SUCCESS] {file_name}")
            embedded_count += 1
            successful_lrcs.append(lrc_path)
            time.sleep(0.01)

        except Exception as e:
            error_msg = str(e) if str(e) else "Metadata Error / Invalid"
            # Hide specific error messages in the terminal to keep it clean
            print(f" 🔴 ERROR   | {file_name}")
            # But still record the specific error in the log
            log_records[dir_path]['logs'].append(f"[ERROR] {file_name} [{error_msg}]")
            error_count += 1
            time.sleep(0.01)
            
            if os.path.exists(lrc_path):
                try:
                    shutil.move(lrc_path, lrc_path + ".failed")
                except OSError:
                    pass

    # Write Detailed Log File per Folder
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("LOG EmbedLRC\n\n")
        for d_path, data in log_records.items():
            f.write(f"Folder: {data['folder_name']}\n")
            f.write(f"Path: ({d_path})\n")
            f.write("-" * 41 + "\n")
            for log_line in data['logs']:
                f.write(f"{log_line}\n")
            f.write("\n")

    # UI Footer / Summary
    time.sleep(1)
    print("\n" + "=" * 50)
    time.sleep(1)
    print("                  RESULT SUMMARY                  ")
    time.sleep(1)
    print("=" * 50)
    time.sleep(1)
    
    print("")
    time.sleep(1)
    print(f"Total processed       : {total_files}")
    time.sleep(1)
    print(f"Successfully embedded : {embedded_count}")
    time.sleep(1)
    print(f"Failed / Skipped      : {skip_count + error_count}")
    time.sleep(3)

    print(f"\n[INFO] The song list and status are logged in: {LOG_FILE}")
    time.sleep(0.5)

    # LRC Deletion Prompt
    if embedded_count > 0:
        print("\nLyrics have been successfully embedded into the audio files.")
        time.sleep(0.5)
        
        delete_lrc = input("Delete the SUCCESSFULLY embedded .lrc files?\ny (yes) or n (no): ").strip().lower()
        time.sleep(0.5)
        
        if delete_lrc == 'y':
            for lrc in successful_lrcs:
                try:
                    os.remove(lrc)
                except OSError:
                    pass
            print("\n[✓] Successfully embedded .lrc files have been deleted.")
            time.sleep(2)
        else:
            print("\n[-] The .lrc files were kept.")
            time.sleep(2)

if __name__ == "__main__":
    embed_lyrics(MUSIC_DIR)
