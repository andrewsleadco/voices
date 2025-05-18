import os
import zipfile

RAW_DIR = "voice-data/librivox/raw"
OUT_DIR = "voice-data/librivox/processed"

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip()

def unzip_file(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
for filename in os.listdir(RAW_DIR):
    print("📄 Found:", filename)  # New: always show files

    if filename.lower().endswith(".zip"):
        book_title = os.path.splitext(filename)[0]
        book_title_sanitized = sanitize_filename(book_title)
        output_path = os.path.join(OUT_DIR, book_title_sanitized)

        if os.path.exists(output_path) and len(os.listdir(output_path)) > 0:
            print(f"✅ Already extracted: {book_title_sanitized}")
            continue

        print(f"📦 Extracting: {book_title_sanitized}")
        try:
            unzip_file(os.path.join(RAW_DIR, filename), output_path)
            print(f"✅ Done: {book_title_sanitized}\n")
        except zipfile.BadZipFile:
            print(f"❌ Bad zip file: {filename}")
        except Exception as e:
            print(f"❌ Error extracting {filename}: {e}")


    print("🎉 All extractions complete.")

if __name__ == "__main__":
    main()
