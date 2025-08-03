import os
import shutil
from datetime import datetime
import filecmp

# Supported photo and metadata extensions
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp', '.mov', '.mp4', '.avif'}
METADATA_EXTENSIONS = {'.json', '.xmp', '.xml', '.txt'}

def get_file_date(path):
    """Get the creation date of the file as a datetime object."""
    try:
        timestamp = os.path.getmtime(path)
    except Exception:
        timestamp = os.path.getctime(path)
    return datetime.fromtimestamp(timestamp)

def should_sort(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in PHOTO_EXTENSIONS or ext in METADATA_EXTENSIONS

def sort_photos(base_path):
    # Collect all files to move first, to avoid issues with moving while walking
    files_to_move = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not should_sort(file):
                continue
            # Skip files already in a year/month folder at the root
            rel_path = os.path.relpath(file_path, base_path)
            parts = rel_path.split(os.sep)
            if len(parts) >= 3 and parts[0].isdigit() and len(parts[0]) == 4 and parts[1].isdigit() and len(parts[1]) == 2:
                continue
            files_to_move.append(file_path)

    for file_path in files_to_move:
        file = os.path.basename(file_path)
        date = get_file_date(file_path)
        year_folder = os.path.join(base_path, str(date.year))
        month_folder = os.path.join(year_folder, date.strftime('%B'))
        os.makedirs(month_folder, exist_ok=True)
        dest_path = os.path.join(month_folder, file)
        base, ext = os.path.splitext(file)
        counter = 1
        # Check for duplicates: if file exists and is identical, skip moving
        while os.path.exists(dest_path):
            # Skip duplicate check if source and destination are the same file
            if os.path.abspath(file_path) == os.path.abspath(dest_path):
                break
            try:
                if filecmp.cmp(file_path, dest_path, shallow=False):
                    print(f"Duplicate found and removed: {file_path} == {dest_path}")
                    os.remove(file_path)
                    break
            except Exception:
                pass
            dest_path = os.path.join(month_folder, f"{base}_{counter}{ext}")
            counter += 1
        else:
            shutil.move(file_path, dest_path)
            print(f"Moved: {file_path} -> {dest_path}")

if __name__ == "__main__":
    base_path = input("Enter the directory path to sort: ").strip()
    if not base_path or not os.path.isdir(base_path):
        print("Invalid directory path.")
    else:
        sort_photos(base_path)
