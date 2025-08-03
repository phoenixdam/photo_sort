# Photo Sort

Photo Sort is a Python script that organizes your photos and related metadata files into folders by year and month, based on each file's creation or modification date. It helps keep your photo collection tidy and easy to browse.

## Features
- Supports common photo formats (JPG, PNG, GIF, BMP, TIFF, HEIC, WEBP, MOV, MP4, AVIF)
- Also sorts metadata files (JSON, XMP, XML, TXT)
- Automatically creates folders for each year and month
- Skips files already sorted
- Detects and removes duplicate files

## Usage
1. Make sure you have Python 3 installed.
2. Place `photo_sort.py` in the directory of your choice.
3. Run the script:

```powershell
python photo_sort.py
```

4. When prompted, enter the path to the directory containing your photos.

## How It Works
- The script scans all files in the given directory and its subdirectories.
- For each supported file, it determines the creation/modification date.
- Files are moved into folders named by year and month (e.g., `2025/August/`).
- If a file with the same name already exists in the destination, the script checks if they are identical:
  - If identical, the duplicate is removed.
  - If not, the new file is renamed (e.g., `photo_1.jpg`).

## Notes
- Only files with supported extensions are sorted.
- The script will not move files already in a year/month folder at the root.
- Always back up your files before running any bulk file operation.

## License
This project is provided as-is, with no warranty. Use at your own risk.
