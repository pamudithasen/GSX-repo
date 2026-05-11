from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'

# Simple in-memory command queue
scan_pending = False

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return {"files": files}, 200

@app.route('/upload', methods=['POST'])
def upload_file():
    # This matches the binary stream sent by client_api.py
    filename = request.headers.get('File-Name', 'received_file.bin')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, 'wb') as f:
        f.write(request.data)
    
    return {"status": "success", "message": f"File saved as {filename}"}, 200

# Endpoint for Flutter to request a scan
@app.route('/trigger-scan', methods=['POST'])
def trigger_scan():
    global scan_pending
    scan_pending = True
    print("📡 Cloud: Scan request queued!")
    return {"status": "queued", "message": "Scan command sent to Pi"}, 200

# Endpoint for Pi to check if a scan is requested
@app.route('/check-scan', methods=['GET'])
def check_scan():
    global scan_pending
    if scan_pending:
        # Reset flag immediately so we don't scan twice
        scan_pending = False
        return {"scan_requested": True}, 200
    return {"scan_requested": False}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Backend server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
