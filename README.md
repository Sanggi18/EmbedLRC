## EmbedLRC
This script is used to embed lyrics (`.lrc`) into various audio formats such as `.mp3`, `.m4a`, `.flac`, `.aac`, and `.alac`. It supports subfolder scanning, automatic logging, and an option to delete `.lrc` files after the embedding process is complete.

**This script was designed to embed lyrics acquired from [lrcget](https://github.com/tranxuanthang/lrcget) and [lrcput](https://github.com/JustOptimize/lrcput).**

## Requirements
- Python 3.x
- Required Python libraries (install using `pip install`):
  - `mutagen`
  - `tqdm` (for progress bar)

## Usage
1. Clone or download this repository.  
2. Ensure that your audio files and `.lrc` files are located within the same folder or its subfolders.  
3. Place the `EmbedLRC.py` script into the main audio folder.  
4. Run the script using Python:
`(In Termux: $ cd Storage > $ cd Music)`

```sh
python EmbedLRC.py
```
5. ​The script will start counting the files and display a real-time progress bar.
6. ​After completion, if there are any failed files (e.g., missing .lrc files), a log will be generated in `LOG_EmbedLRC.txt`
7. ​The script will then ask whether you want to delete all .lrc files or keep them.

## Example Folder
Suppose you have the following directory structure:
```
Music/
├─ ENGLISH/
│  ├─ song1.m4a
│  ├─ song1.lrc
├─ INDONESIA/
│  ├─ song2.mp3
│  ├─ song2.lrc
├─ EmbedLRC.py (Ensure it is placed in the main folder)
```
## Log Files
**​All files that do not have a corresponding .lrc file or fail to embed will be recorded in LOG_EmbedLRC.txt**

Location: Same directory as EmbedLRC.py

## Notes
- The script will automatically overwrite any existing embedded lyrics.
- ​For unsupported formats (e.g., .mp3 files with corrupt or non-standard tags), the script will skip the file and log it as FAIL.
- ​It is highly recommended to back up your .lrc files before choosing to delete them.
​- If you need to download .lrc files, you can find them using these Android applications: [Lyrically](https://t.me/lyricallyupdates) , [SongSync](https://github.com/Lambada10/SongSync) , [L Y R I C I F Y](https://t.me/LyricifyApp)

