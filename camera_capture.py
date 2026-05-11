import subprocess
import os
import time
from client_api import GSXTransferClient

# Configuration
PHOTO_NAME = "gsx_capture.jpg"
BACKEND_URL = "https://web-production-c5fe0.up.railway.app"

def capture_image(filename):
    print("📸 Initializing Camera...")
    try:
        # 'libcamera-still' is the command for modern Raspberry Pi OS (Bullseye/Bookworm)
        # We use --immediate to skip the preview and -n to hide the preview window
        subprocess.run(["libcamera-still", "-o", filename, "--immediate", "-n"], check=True)
        print(f"✅ Photo captured and saved as {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to capture photo: {e}")
        print("Tip: If you are on an older Pi OS, you might need 'raspistill' instead.")
        return False

def main():
    # 1. Capture the photo
    if capture_image(PHOTO_NAME):
        # 2. Upload to Railway
        print("🚀 Uploading to Railway...")
        client = GSXTransferClient(BACKEND_URL)
        success = client.send_file("upload", PHOTO_NAME)
        
        if success:
            print("\n--- DONE ---")
            print(f"View your photo here: {BACKEND_URL}/download/{PHOTO_NAME}")
            print(f"Full list: {BACKEND_URL}/list")

if __name__ == "__main__":
    main()
