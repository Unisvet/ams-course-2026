import http.server
import socketserver
import webbrowser
from threading import Timer

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Ensure correct MIME types for static assets
        self.extensions_map.update({
            '.js': 'text/javascript',
            '.css': 'text/css',
            '.json': 'application/json',
            '.html': 'text/html',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
        })
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

if __name__ == "__main__":
    # Open browser after 1 second
    Timer(1.0, open_browser).start()
    
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"\n==================================================")
        print(f"AMS-Kurs 2026 - Lokaler Development Server gestartet")
        print(f"URL: http://localhost:{PORT}")
        print(f"==================================================")
        print("Drücke Strg+C (Ctrl+C), um den Server zu beenden.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer wird beendet...")
