from pathlib import Path
import imagehash
from PIL import Image
import exifread
import hashlib
import json

def scan_images(folder):
    photos = []
    for ext in ('.jpg', '.jpeg', '.png'):
        for img_path in Path(folder).rglob(f'*{ext}'):
            try:
                with Image.open(img_path) as img:
                    phash = str(imagehash.phash(img))
                with open(img_path, 'rb') as f:
                    sha256 = hashlib.sha256(f.read()).hexdigest()
                with open(img_path, 'rb') as f:
                    tags = exifread.process_file(f, stop_tag="DateTimeOriginal")
                    ts = str(tags.get('EXIF DateTimeOriginal', ''))
                photos.append({
                    "path": str(img_path),
                    "phash": phash,
                    "sha256": sha256,
                    "timestamp": ts
                })
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    return photos

if __name__ == "__main__":
    folder = input("Enter the photo folder: ")
    photo_meta = scan_images(folder)
    print(f"Found {len(photo_meta)} photos.")
    # Save output
    with open("photo_meta.json", "w") as f:
        json.dump(photo_meta, f, indent=2)
    print("Saved metadata to photo_meta.json")

