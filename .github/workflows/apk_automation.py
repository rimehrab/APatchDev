import os
import requests
import zipfile
from datetime import datetime

# Configuration
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # Replace with your bot token
CHAT_ID = "YOUR_CHAT_ID"  # Replace with your chat ID
APK_DIRECTORY = "apk_directory"  # Local directory within GitHub runner workspace
ZIP_URL = "https://nightly.link/bmax121/APatch/workflows/build/main/APatch.zip"
ZIP_FILE_PATH = "APatch.zip"  # Zip file location

def send_message(text):
    """Send a message to Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.text}")

def download_zip():
    """Download the zip file."""
    response = requests.get(ZIP_URL, stream=True)
    if response.status_code == 200:
        with open(ZIP_FILE_PATH, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print("Zip file downloaded.")
        return True
    else:
        print(f"Failed to download zip file: {response.status_code}")
        return False

def extract_apk():
    """Extract APK from the zip."""
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        apk_files = [f for f in zip_ref.namelist() if f.endswith(".apk")]
        if not apk_files:
            print("No APK found in the zip.")
            return None
        apk_name = apk_files[0]
        apk_path = os.path.join(APK_DIRECTORY, apk_name)

        # If APK already exists, skip extraction
        if os.path.exists(apk_path):
            print(f"APK '{apk_name}' already exists. Skipping extraction.")
            return None

        # Extract new APK
        os.makedirs(APK_DIRECTORY, exist_ok=True)
        zip_ref.extract(apk_name, APK_DIRECTORY)
        print(f"Extracted APK: {apk_name}")
        return apk_name

def cleanup():
    """Delete the zip file."""
    if os.path.exists(ZIP_FILE_PATH):
        os.remove(ZIP_FILE_PATH)
        print("Zip file deleted.")

def main():
    """Main function."""
    if download_zip():
        apk_name = extract_apk()
        cleanup()

        if apk_name:
            send_message(f"*New APK Uploaded:*\n`{apk_name}`")
        else:
            print("No new APK. Notification skipped.")
    else:
        print("Download failed. Skipping further steps.")

if __name__ == "__main__":
    main()
