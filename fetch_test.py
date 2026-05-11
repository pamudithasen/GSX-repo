import urllib.request
import os

def download_file(url, destination):
    print(f"--- Starting File Transfer Test ---")
    print(f"Target URL: {url}")
    print(f"Destination: {destination}")
    
    try:
        with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            
        print(f"SUCCESS: File transferred successfully.")
        print(f"File size: {os.path.getsize(destination)} bytes")
        
        print("\n--- Content Preview ---")
        with open(destination, 'r') as f:
            print(f.read())
            
    except Exception as e:
        print(f"FAILURE: An error occurred during transfer.")
        print(f"Error: {e}")

if __name__ == "__main__":
    TEST_URL = "https://raw.githubusercontent.com/python/cpython/main/LICENSE"
    DEST_FILE = "verify_transfer.txt"
    
    download_file(TEST_URL, DEST_FILE)
