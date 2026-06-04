#!/usr/bin/env python3
import http.server
import os
import json
import urllib.request
import urllib.error

SUPABASE_URL = "https://muhxkvtniuinrspwhzhn.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_e_iKvOS5K65ou7AQTtTsWA_JUHjM7fZ"
N8N_WEBHOOK_URL = "https://api.ihflow.com/webhook/IG-connect"
N8N_PRODUCTS_URL = "https://api.ihflow.com/webhook/50226b32-81d3-4348-a064-c6be64a22ca6"

# Secret lives only on the server — never sent to the browser
_IG_SECRET = os.environ.get(
    "IG_WEBHOOK_SECRET",
    "13df50d99bbf9b0c8508f14c9a3a454c21b7f236484e00925049fffeedfd3729",
)


class SecureHandler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/ig-connect":
            self._handle_ig_connect()
        elif self.path == "/api/ig-products":
            self._handle_ig_products()
        else:
            self.send_error(404, "Not found")

    def _handle_ig_connect(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            access_token = (body.get("access_token") or "").strip()

            if not access_token:
                self._json(400, {"error": "Missing access_token"})
                return

            # 1. Verify the session with Supabase to get the real user_id
            verify_req = urllib.request.Request(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "apikey": SUPABASE_ANON_KEY,
                },
            )
            try:
                with urllib.request.urlopen(verify_req, timeout=10) as r:
                    user_data = json.loads(r.read())
            except urllib.error.HTTPError as e:
                self._json(401, {"error": "Invalid or expired session", "detail": str(e)})
                return

            user_id = user_data.get("id")
            if not user_id:
                self._json(401, {"error": "Could not resolve user id from session"})
                return

            # 2. Call n8n webhook server-side — secret never leaves the server
            payload = json.dumps({
                "secret": _IG_SECRET,
                "user_id": user_id,
            }).encode()

            n8n_req = urllib.request.Request(
                N8N_WEBHOOK_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            try:
                with urllib.request.urlopen(n8n_req, timeout=20) as r:
                    resp_body = r.read().decode("utf-8", errors="replace")
                    resp_status = r.status
                try:
                    resp_data = json.loads(resp_body)
                except Exception:
                    resp_data = {"raw": resp_body}
                self._json(200, {"ok": True, "status": resp_status, "data": resp_data})

            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                self._json(502, {
                    "error": f"Webhook returned {e.code}",
                    "detail": err_body,
                })

        except json.JSONDecodeError:
            self._json(400, {"error": "Invalid JSON body"})
        except Exception as e:
            self._json(500, {"error": str(e)})

    def _handle_ig_products(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            bot_id = (body.get("bot_id") or "").strip()

            if not bot_id:
                self._json(400, {"error": "Missing bot_id"})
                return

            payload = json.dumps({
                "bot_id": bot_id,
                "secret": _IG_SECRET,
            }).encode()

            n8n_req = urllib.request.Request(
                N8N_PRODUCTS_URL,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-ihflow-secret": _IG_SECRET,
                },
                method="POST",
            )

            try:
                with urllib.request.urlopen(n8n_req, timeout=20) as r:
                    resp_body = r.read().decode("utf-8", errors="replace")
                try:
                    resp_data = json.loads(resp_body)
                except Exception:
                    resp_data = {"raw": resp_body}
                self._json(200, {"ok": True, "data": resp_data})

            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                self._json(502, {"error": f"Webhook returned {e.code}", "detail": err_body})

        except json.JSONDecodeError:
            self._json(400, {"error": "Invalid JSON body"})
        except Exception as e:
            self._json(500, {"error": str(e)})

    def _json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin")
        self.send_header("Permissions-Policy",
                         "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src * data: blob:; "
            "connect-src 'self' "
            "https://muhxkvtniuinrspwhzhn.supabase.co "
            "wss://muhxkvtniuinrspwhzhn.supabase.co "
            "https://graph.facebook.com "
            "https://www.facebook.com; "
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
    print("Serving on http://0.0.0.0:5000")
    server.serve_forever()
