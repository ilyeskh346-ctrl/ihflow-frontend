#!/usr/bin/env python3
import http.server
import os

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        super().log_message(format, *args)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    server = http.server.HTTPServer(("0.0.0.0", 5000), NoCacheHandler)
    print("Serving on http://0.0.0.0:5000 (no-cache)")
    server.serve_forever()
