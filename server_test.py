import http.server
import socketserver
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print(f"--- Starting Minimal HTTP Server ---")
print(f"IP Address: {get_ip()}")
print(f"Port: {PORT}")
print(f"To download files from this Pi, go to: http://{get_ip()}:{PORT} in your browser")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
