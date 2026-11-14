#!/usr/bin/env python3
"""Loopback-only AITE bridge: browser -> localhost:8765 -> Ollama localhost:11434."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json, os

HOST = "127.0.0.1"
PORT = int(os.environ.get("AITE_PORT", "8765"))
MODEL = os.environ.get("AITE_MODEL", "qwen2.5:3b")
OLLAMA = "http://127.0.0.1:11434"
ALLOWED_SUFFIXES = tuple(x.strip().lower() for x in os.environ.get("AITE_ALLOWED_SUFFIXES", ".onrender.com").split(",") if x.strip())
ALLOWED_EXACT = set(x.strip() for x in os.environ.get("AITE_ALLOWED_ORIGINS", "").split(",") if x.strip())

def allowed(origin):
    if not origin: return False
    if origin in ALLOWED_EXACT: return True
    try:
        from urllib.parse import urlparse
        p = urlparse(origin)
        host = (p.hostname or "").lower()
        return p.scheme == "https" and any(host.endswith(s) and host != s.lstrip(".") for s in ALLOWED_SUFFIXES)
    except Exception:
        return False

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass
    def send_json(self, code, data, origin=None):
        raw = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        if origin and allowed(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()
        self.wfile.write(raw)
    def do_OPTIONS(self):
        origin = self.headers.get("Origin")
        if not allowed(origin): return self.send_json(403, {"error":"Origin not allowed"})
        self.send_json(204, {}, origin)
    def do_GET(self):
        origin = self.headers.get("Origin")
        if self.path != "/health": return self.send_json(404, {"error":"Not found"}, origin)
        try:
            with urlopen(OLLAMA + "/api/tags", timeout=3) as r: tags=json.loads(r.read())
            names=[m.get("name","") for m in tags.get("models",[])]
            return self.send_json(200, {"ok":True,"model":MODEL,"installed":MODEL in names,"models":names}, origin)
        except Exception as e:
            return self.send_json(503, {"ok":False,"model":MODEL,"error":"Ollama is not running or model is not available"}, origin)
    def do_POST(self):
        origin = self.headers.get("Origin")
        if not allowed(origin): return self.send_json(403, {"error":"Origin not allowed"})
        if self.path != "/api/chat": return self.send_json(404, {"error":"Not found"}, origin)
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length <= 0 or length > 2_000_000: return self.send_json(413, {"error":"Invalid request size"}, origin)
            payload=json.loads(self.rfile.read(length))
            payload["model"] = MODEL
            payload["stream"] = False
            req=Request(OLLAMA+"/api/chat", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}, method="POST")
            with urlopen(req, timeout=240) as r: data=json.loads(r.read())
            return self.send_json(200, data, origin)
        except HTTPError as e:
            return self.send_json(502, {"error":"Ollama request failed","status":e.code}, origin)
        except (URLError, TimeoutError):
            return self.send_json(503, {"error":"Ollama is not running. Start Ollama and download the model."}, origin)
        except Exception as e:
            return self.send_json(400, {"error":"Invalid request or local model error"}, origin)

if __name__ == "__main__":
    print(f"AITE local bridge listening only on http://{HOST}:{PORT}")
    print(f"Allowed website suffixes: {', '.join(ALLOWED_SUFFIXES)}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
