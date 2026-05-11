from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Backend server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
