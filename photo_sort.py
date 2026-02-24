import argparse
import filecmp
import os
import shutil
from datetime import datetime

# Supported photo and metadata extensions
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp', '.mov', '.mp4', '.avif'}
METADATA_EXTENSIONS = {'.json', '.xmp', '.xml', '.txt', '.aae'}


def get_file_date(path):
    """Get file date from modification time, falling back to creation time."""
    try:
        timestamp = os.path.getmtime(path)
    except Exception:
        timestamp = os.path.getctime(path)
    return datetime.fromtimestamp(timestamp)


def should_sort(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in PHOTO_EXTENSIONS or ext in METADATA_EXTENSIONS


def print_summary(stats):
    print("\n--- Summary ---")
    print(f"  Moved:      {stats['moved']}")
    print(f"  Duplicates: {stats['duplicates']}")
    print(f"  Skipped:    {stats['skipped']}")
    print(f"  Errors:     {stats['errors']}")


def sort_photos(base_path, resort=False):
    stats = {'moved': 0, 'duplicates': 0, 'skipped': 0, 'errors': 0}

    # Collect all files to move first, to avoid issues with moving while walking
    files_to_move = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not should_sort(file):
                continue
            # Skip files already in a year/month folder at the root
            if not resort:
                rel_path = os.path.relpath(file_path, base_path)
                parts = rel_path.split(os.sep)
                if len(parts) >= 3 and parts[0].isdigit() and len(parts[0]) == 4 and len(parts[1]) >= 4 and parts[1][:2].isdigit() and parts[1][2] == '_':
                    stats['skipped'] += 1
                    continue
            files_to_move.append(file_path)

    try:
        for file_path in files_to_move:
            try:
                file = os.path.basename(file_path)
                date = get_file_date(file_path)
                year_folder = os.path.join(base_path, str(date.year))
                month_folder = os.path.join(year_folder, date.strftime('%m_%B'))
                os.makedirs(month_folder, exist_ok=True)
                dest_path = os.path.join(month_folder, file)
                base, ext = os.path.splitext(file)
                counter = 1
                # Check for duplicates: if file exists and is identical, skip moving
                while os.path.exists(dest_path):
                    # Skip duplicate check if source and destination are the same file
                    if os.path.abspath(file_path) == os.path.abspath(dest_path):
                        stats['skipped'] += 1
                        break
                    try:
                        if filecmp.cmp(file_path, dest_path, shallow=False):
                            print(f"Duplicate found and removed: {file_path} == {dest_path}")
                            os.remove(file_path)
                            stats['duplicates'] += 1
                            break
                    except Exception as cmp_err:
                        print(f"Warning: could not compare {file_path} and {dest_path}: {cmp_err}")
                    dest_path = os.path.join(month_folder, f"{base}_{counter}{ext}")
                    counter += 1
                else:
                    source_size = os.path.getsize(file_path)
                    shutil.move(file_path, dest_path)
                    # Verify move
                    if not os.path.exists(dest_path) or os.path.getsize(dest_path) != source_size:
                        raise RuntimeError(f"Move verification failed for {file_path} -> {dest_path}")
                    print(f"Moved: {file_path} -> {dest_path}")
                    stats['moved'] += 1
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                stats['errors'] += 1
    finally:
        print_summary(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort photos into YYYY/MM_MonthName folders by date.")
    parser.add_argument("directory", help="Directory path to sort")
    parser.add_argument("--resort", action="store_true",
                        help="Re-sort files already in year/month folders")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Invalid directory path.")
    else:
        try:
            sort_photos(args.directory, resort=args.resort)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
