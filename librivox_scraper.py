import os
import json
import requests
from tqdm import tqdm

# --- Config ---
BASE_URL = "https://librivox.org/api/feed/audiobooks"
RAW_DIR = "voice-data/librivox/raw"
NUM_BOOKS = 5  # You can increase this later

PARAMS = {
    "format": "json",
    "language": "English",
    "fields": "title,authors,totaltimesecs,url_librivox,url_zip_file,url_text_source",
    "limit": NUM_BOOKS,
    "sort_order": "popular"
}

# --- Utilities ---

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip()

def download_file(url, dest_path):
    if not url:
        print(f"⚠️  No URL provided for {dest_path}")
        return False
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total = int(response.headers.get('content-length', 0))

        with open(dest_path, 'wb') as f, tqdm(
            desc=os.path.basename(dest_path),
            total=total,
            unit='B',
            unit_scale=True
        ) as bar:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                bar.update(len(chunk))
        return True
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return False

def save_metadata(book, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(book, f, indent=2)

# --- Main Scraper ---

def fetch_librivox_books():
    print("📡 Fetching audiobook metadata...")
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()
    data = response.json()
    return data.get("books", [])

def main():
    ensure_dir(RAW_DIR)
    books = fetch_librivox_books()
    print(f"🔎 Found {len(books)} books. Starting downloads...\n")

    for book in books:
        title = sanitize_filename(book["title"])
        zip_url = book.get("url_zip_file")
        text_url = book.get("url_text_source")

        print(f"📘 {title}")

        audio_path = os.path.join(RAW_DIR, f"{title}.zip")
        text_path = os.path.join(RAW_DIR, f"{title}.txt")
        meta_path = os.path.join(RAW_DIR, f"{title}_meta.json")

        if zip_url:
            download_file(zip_url, audio_path)
        if text_url and "gutenberg" in text_url:
            download_file(text_url, text_path)

        save_metadata(book, meta_path)
        print("✅ Done.\n")

    print("🎉 All downloads complete.")

if __name__ == "__main__":
    main()
