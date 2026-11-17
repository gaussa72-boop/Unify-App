#!/usr/bin/env python3
"""ULTIMA AI local companion — safe, localhost-only command gateway.
Python 3.8+, standard library only. No shell execution or remote listener.
"""
import argparse
import hmac
import json
import os
import secrets
import socket
import sys
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path.home() / "Library" / "Application Support" / "UltimaAI"
TOKEN_FILE = APP_DIR / "local.token"
HOST = "127.0.0.1"
PORT = 8765
MAX_BODY = 8192
ALLOWED_HOSTS = {
    "ultima-unify-45ne.onrender.com",
    "ultima-central-bt56.onrender.com",
    "github.com",
    "render.com",
}

def ensure_token():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(str(APP_DIR), 0o700)
    except OSError:
        pass
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if len(token) >= 40:
            return token
    token = secrets.token_urlsafe(48)
    fd = os.open(str(TOKEN_FILE), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(token + "\n")
    return token

def safe_open_url(raw_url):
    parsed = urllib.parse.urlparse(raw_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Only HTTPS links are allowed.")
    host = parsed.hostname.lower()
    if not any(host == item or host.endswith("." + item) for item in ALLOWED_HOSTS):
        raise ValueError("This domain is not on the local allowlist.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed.")
    webbrowser.open(raw_url, new=2)
    return {"opened": True, "host": host}

class Handler(BaseHTTPRequestHandler):
    server_version = "UltimaLocal/0.1"
    def log_message(self, fmt, *args):
        sys.stdout.write("[ULTIMA] " + (fmt % args) + "\n")

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            page = Path(__file__).with_name("index.html")
            data = page.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "bind": HOST, "port": PORT})
            return
        self.send_json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/api/command":
            self.send_json(404, {"error": "not_found"})
            return
        supplied = self.headers.get("X-Ultima-Token", "")
        if not hmac.compare_digest(supplied, self.server.token):
            self.send_json(401, {"error": "unauthorized"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > MAX_BODY:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            command = payload.get("command")
            if command == "status":
                result = {"assistant": "ULTIMA AI Local Companion", "status": "running",
                          "host": HOST, "port": PORT, "mode": "safe",
                          "capabilities": ["status", "open_allowlisted_https_url"],
                          "blocked": ["shell", "file_write", "email_send", "payments", "account_changes"]}
            elif command == "open_url":
                result = safe_open_url(str(payload.get("url", "")))
            else:
                self.send_json(403, {"error": "command_not_allowed",
                                     "allowed": ["status", "open_url"]})
                return
            self.send_json(200, {"ok": True, "result": result})
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception:
            self.send_json(500, {"error": "internal_error"})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="create local token and exit")
    args = parser.parse_args()
    token = ensure_token()
    if args.init:
        print("ULTIMA local token created at: " + str(TOKEN_FILE))
        print("Keep this file private. Do not paste the token into chat or commit it to Git.")
        return
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.token = token
    print("ULTIMA AI local companion listening only on http://%s:%s" % (HOST, PORT))
    print("Open this address on this Mac. Token file: %s" % TOKEN_FILE)
    print("Safe mode: no shell, file writes, email sending, payments or account changes.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
