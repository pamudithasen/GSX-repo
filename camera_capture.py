import subprocess
import os
import time
from client_api import GSXTransferClient

# Configuration
PHOTO_NAME = "gsx_capture.jpg"
BACKEND_URL = "https://web-production-c5fe0.up.railway.app"

def capture_image(filename):
    print("📸 Initializing Camera...")
    
    # 1. Try picamera2 (Newest Pi Camera library - what your previous script used)
    try:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        config = picam2.create_still_configuration()
        picam2.configure(config)
        picam2.start()
        picam2.capture_file(filename)
        picam2.stop()
        print(f"✅ Photo captured using picamera2")
        return True
    except (ImportError, Exception) as e:
        print(f"⚠️ picamera2 failed or not found, trying other methods...")

    # 2. Try libcamera-still (Modern OS command line)
    try:
        subprocess.run(["libcamera-still", "-o", filename, "--immediate", "-n"], check=True)
        print(f"✅ Photo captured using libcamera-still")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # 3. Try raspistill (Older OS command line)
    try:
        subprocess.run(["raspistill", "-o", filename, "-t", "100"], check=True)
        print(f"✅ Photo captured using raspistill")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    print("❌ All capture methods failed.")
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
