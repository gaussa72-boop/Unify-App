import os
from flask import Flask, send_from_directory, jsonify
from pathlib import Path

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)

@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Cache-Control", "no-store" if response.mimetype == "application/json" else "public, max-age=300")
    return response

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.get("/manifest.webmanifest")
def manifest():
    return send_from_directory(ROOT, "manifest.webmanifest")

@app.get("/sw.js")
def service_worker():
    response = send_from_directory(ROOT, "sw.js")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.get("/icon.svg")
def icon():
    return send_from_directory(ROOT, "icon.svg")

@app.get("/health")
def health():
    return jsonify(status="ok", service="ultima-central", mode="portfolio-launcher"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
