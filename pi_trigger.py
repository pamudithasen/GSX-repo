import time
import requests
import subprocess
import os

# Configuration
RAILWAY_URL = "https://web-production-c5fe0.up.railway.app"
CHECK_INTERVAL = 1.0  # Seconds between checks

def perform_capture():
    print("\n" + "="*40)
    print("📸 SCAN COMMAND RECEIVED FROM CLOUD!")
    print("="*40)
    
    try:
        print("🚀 Running 'python3 camera_capture.py'...")
        # Run your existing capture and upload script
        process = subprocess.run(
            ['python3', 'camera_capture.py'], 
            capture_output=True, 
            text=True
        )
        
        print("--- SCRIPT OUTPUT ---")
        print(process.stdout)
        
        if process.returncode == 0:
            print("✅ Capture and Upload to Railway Successful!")
        else:
            print(f"❌ Script failed: {process.stderr}")
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")

def main():
    print("\n" + "*"*50)
    print("📡 PI CLOUD LISTENER IS LIVE")
    print(f"🔗 Monitoring: {RAILWAY_URL}/check-scan")
    print("💡 Waiting for remote scan commands...")
    print("*"*50 + "\n")

    while True:
        try:
            # Check if there's a pending scan request
            response = requests.get(f"{RAILWAY_URL}/check-scan", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("scan_requested") == True:
                    perform_capture()
            
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
            time.sleep(5)  # Wait longer if server is down
            continue
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
