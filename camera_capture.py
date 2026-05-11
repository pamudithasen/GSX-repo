import subprocess
import os
import time
from client_api import GSXTransferClient

# Configuration
PHOTO_NAME = "gsx_capture.jpg"
BACKEND_URL = "https://web-production-c5fe0.up.railway.app"

def capture_image(filename):
    print("📸 Initializing Camera...")
    
    # Try libcamera-still first
    try:
        subprocess.run(["libcamera-still", "-o", filename, "--immediate", "-n"], check=True)
        print(f"✅ Photo captured using libcamera-still")
        return True
    except FileNotFoundError:
        # Fallback to raspistill for older OS
        print("⚠️ libcamera-still not found, trying raspistill...")
        try:
            subprocess.run(["raspistill", "-o", filename, "-t", "100"], check=True)
            print(f"✅ Photo captured using raspistill")
            return True
        except Exception as e:
            print(f"❌ Both libcamera and raspistill failed: {e}")
            return False
    except Exception as e:
        print(f"❌ Failed to capture photo: {e}")
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
