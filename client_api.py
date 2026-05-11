import urllib.request
import os
import json

class GSXTransferClient:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def receive_file(self, endpoint, save_path):
        url = f"{self.backend_url}/{endpoint.lstrip('/')}"
        print(f"--- Receiving file from {url} ---")
        try:
            urllib.request.urlretrieve(url, save_path)
            print(f"SUCCESS: Received and saved to {save_path}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to receive file: {e}")
            return False

    def send_file(self, endpoint, file_path):
        url = f"{self.backend_url}/{endpoint.lstrip('/')}"
        print(f"--- Sending {file_path} to {url} ---")
        
        if not os.path.exists(file_path):
            print(f"ERROR: File {file_path} does not exist.")
            return False

        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Note: This is a simple binary POST. 
            # If your backend expects 'multipart/form-data', 
            # using 'requests' library is highly recommended.
            req = urllib.request.Request(url, data=file_data, method='POST')
            req.add_header('Content-Type', 'application/octet-stream')
            req.add_header('File-Name', os.path.basename(file_path))
            
            with urllib.request.urlopen(req) as response:
                result = response.read().decode()
                print(f"SUCCESS: Server responded with: {result}")
                return True
        except Exception as e:
            print(f"ERROR: Failed to send file: {e}")
            return False

if __name__ == "__main__":
    # Replace with your actual backend URL once hosted
    # For testing, you can use 'https://postman-echo.com/post' for the SEND test
    MY_BACKEND = "https://web-production-c5fe0.up.railway.app"
    
    client = GSXTransferClient(MY_BACKEND)
    
    # Example usage:
    # client.receive_file("get-config", "local_config.json")
    # client.send_file("upload-logs", "test_file.txt")
    
    print("GSX Transfer Client Initialized.")
    print(f"Configured Backend: {MY_BACKEND}")
