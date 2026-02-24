# Photo Sort

Photo Sort is a Python script that organizes your photos and related metadata files into folders by year and month, based on each file's creation or modification date. It helps keep your photo collection tidy and easy to browse.

## Features
- **EXIF date extraction** — uses the actual date a photo was taken (from EXIF metadata) instead of the file modification date, which is often wrong for transferred or exported files (e.g., Google Takeout)
- Supports common photo formats (JPG, PNG, GIF, BMP, TIFF, HEIC, WEBP, MOV, MP4, AVIF)
- Also sorts metadata files (JSON, XMP, XML, TXT, AAE)
- Automatically creates folders for each year and month
- Skips files already sorted
- Detects and removes duplicate files
- **Fault tolerant** — one bad file won't crash the whole run; errors are logged and a summary is printed at the end
- **Move verification** — confirms file size after each move to catch silent failures

## Usage
1. Make sure you have Python 3 installed.
2. Install the dependency:

```powershell
pip install -r requirements.txt
```

3. Run the script:

```powershell
python photo_sort.py
```

4. When prompted, enter the path to the directory containing your photos.

## How It Works
- The script scans all files in the given directory and its subdirectories.
- For each supported file, it extracts the EXIF date taken (for JPG, PNG, TIFF, HEIC, WEBP), falling back to file modification date if no EXIF data is available.
- Files are moved into folders named by year and month (e.g., `2025/01_January/`).
- If a file with the same name already exists in the destination, the script checks if they are identical:
  - If identical, the duplicate is removed.
  - If not, the new file is renamed (e.g., `photo_1.jpg`).

## Notes
- Only files with supported extensions are sorted.
- The script will not move files already in a year/month folder at the root.
- Always back up your files before running any bulk file operation.

## License
This project is provided as-is, with no warranty. Use at your own risk.
