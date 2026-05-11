from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def trigger_scan():
    print("📸 Scan request received! Triggering camera...")
    try:
        # Run the camera_capture script (make sure it's in the same folder)
        # This will capture the photo and upload it to your Railway server
        result = subprocess.run(['python3', 'camera_capture.py'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Capture Successful")
            return {
                "status": "success", 
                "message": "Scan completed and uploaded to Railway",
                "output": result.stdout
            }, 200
        else:
            print(f"❌ Capture Failed: {result.stderr}")
            return {
                "status": "error", 
                "message": "Hardware scan failed",
                "details": result.stderr
            }, 500
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    # Run on all interfaces so your Mac can find it
    print("🚀 Pi Hardware Trigger listening on port 5000...")
    app.run(host='0.0.0.0', port=5000)
