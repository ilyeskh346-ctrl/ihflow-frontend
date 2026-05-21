#!/usr/bin/env python3
import http.server
import os

class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src * data: blob:; "
            "connect-src 'self' https://muhxkvtniuinrspwhzhn.supabase.co wss://muhxkvtniuinrspwhzhn.supabase.co https://api.ihflow.com https://graph.facebook.com https://www.facebook.com; "
            "frame-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        super().end_headers()

    def log_message(self, format, *args):
        super().log_message(format, *args)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    server = http.server.HTTPServer(("0.0.0.0", 5000), SecureHandler)
    print("Serving on http://0.0.0.0:5000 (secure, no-cache)")
    server.serve_forever()
