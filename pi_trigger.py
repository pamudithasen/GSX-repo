from flask import Flask, request, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

# Manual CORS support for Flutter Web
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/scan', methods=['GET', 'POST', 'OPTIONS'])
def trigger_scan():
    if request.method == 'OPTIONS':
        return '', 204
        
    print("\n" + "="*40)
    print("🔔 NEW SCAN REQUEST RECEIVED")
    print("="*40)
    
    try:
        print("📸 Step 1: Initializing camera script...")
        # We'll use capture_output=False so it prints directly to the terminal for visibility
        # but we'll use a try-except to catch execution errors
        
        print(f"🚀 Step 2: Running 'python3 camera_capture.py'...")
        # Using check=True to raise error on failure
        process = subprocess.run(
            ['python3', 'camera_capture.py'], 
            capture_output=True, 
            text=True
        )
        
        # Print the script's output to the Pi terminal so the user sees it
        print("--- SCRIPT OUTPUT START ---")
        print(process.stdout)
        if process.stderr:
            print("--- SCRIPT ERRORS ---")
            print(process.stderr)
        print("--- SCRIPT OUTPUT END ---")

        if process.returncode == 0:
            print("✅ Step 3: Scan and Upload Successful!")
            return jsonify({
                "status": "success", 
                "message": "Scan completed and uploaded to Railway"
            }), 200
        else:
            print(f"❌ Step 3: Hardware scan failed with exit code {process.returncode}")
            return jsonify({
                "status": "error", 
                "message": "Hardware scan failed",
                "details": process.stderr
            }), 500
            
    except Exception as e:
        print(f"💥 FATAL ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "*"*50)
    print("🚀 PI HARDWARE TRIGGER IS LIVE")
    print("📡 Listening on: http://0.0.0.0:5000")
    print("💡 Waiting for requests from AgroSpectra app...")
    print("*"*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
