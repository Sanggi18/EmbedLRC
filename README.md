## EmbedLRC
Script EmbedLRC ini digunakan untuk embed lirik (.lrc) ke berbagai format audio seperti .mp3, .m4a, .flac, .aac, .alac Script ini mendukung subfolder, log otomatis, dan opsi hapus .lrc setelah embed selesai.

**this script was designed to embed lyrics acquired from [lrcget](https://github.com/tranxuanthang/lrcget) , [lrcput](https://github.com/JustOptimize/lrcput)**

## Requirements
- Python 3.x
- Required Python libraries (install using `pip install`):
  - mutagen
  - tqdm (for progress bar)

## Usage
1. Clone atau download repository ini.  
2. Pastikan folder audio dan .lrc berada di dalam folder yang sama atau subfolder.  
3. Letakkan script EmbedLRC.py di folder utama audio.  
4. Jalankan script dengan Python :
```sh
python EmbedLRC.py
```
5. Script akan mulai menghitung, menampilkan progress per file.  
6. Setelah selesai, jika ada file gagal (tidak memiliki .lrc), akan dibuat log di LOG_EmbedLRC.txt.  
7. Script akan menanyakan apakah ingin menghapus semua .lrc atau tidak

## Example Folder
Misalkan Anda memiliki struktur direktori sebagai berikut:
```
Music/
├─ ENGLISH/
│  ├─ song1.m4a
│  ├─ song1.lrc
├─ INDONESIA/
│  ├─ song2.mp3
│  ├─ song2.lrc
├─ EmbedLRC.py (Pastikan dalam 1 Folder)
```

## Log Files
**Semua file yang tidak memiliki .lrc atau gagal di-embed akan dicatat di LOG_EmbedLRC.txt**
Lokasi: folder yang sama dengan EmbedLRC.py

## Catatan
- Script akan overwrite lyrics yang ada sebelumnya.  
- Untuk format yang tidak didukung (misal .mp3 tanpa tag lirik), script akan skip dengan log FAIL.  
- Disarankan backup .lrc sebelum menghapus.
- Kalau mau download file .lrc kalian bisa akses aplikasi android di [Lyrically](https://t.me/lyricallyupdates) , [SongSync](https://github.com/Lambada10/SongSync) , [L Y R I C I F Y](https://t.me/LyricifyApp)
