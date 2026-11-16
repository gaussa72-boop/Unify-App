import os
from flask import Flask, send_from_directory, jsonify, Response
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
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    nav = """
    <a href="/cosmican/" style="display:inline-block;margin-left:18px;padding:8px 12px;border:1px solid #65dce0;border-radius:9px;color:#65dce0;text-decoration:none;letter-spacing:.04em;font-size:12px">COSMICAN LUX SYNDICATE ↗</a>
    """
    html = html.replace("</header>", nav + "</header>", 1)
    section = """
    <section style="margin:18px 0;padding:18px;border:1px solid #65dce055;border-radius:15px;background:#101d2d">
      <div style="color:#65dce0;font-size:11px;letter-spacing:.18em">COMMUNITY · NEU IM NETZWERK</div>
      <h2 style="margin:8px 0">Cosmican Lux Syndicate</h2>
      <p style="color:#9caac0">Das neue Blog- und Beitragsarchiv mit manuellem Import aus der privaten Facebook-Gruppe.</p>
      <a href="/cosmican/" style="display:inline-block;padding:10px 14px;border-radius:8px;background:#e4c477;color:#111827;text-decoration:none;font-weight:700">Blog öffnen ↗</a>
    </section>
    """
    html = html.replace('<h2>Projektübersicht</h2>', section + '<h2>Projektübersicht</h2>', 1)
    return Response(html, mimetype="text/html")

@app.get("/account/")
def account_home():
    return send_from_directory(ROOT / "account", "index.html")

@app.get("/admin/")
def admin_home():
    return send_from_directory(ROOT / "admin", "index.html")

@app.get("/cosmican/")
def cosmican_home():
    return send_from_directory(ROOT / "cosmican", "index.html")

@app.get("/cosmican/<path:filename>")
def cosmican_assets(filename):
    return send_from_directory(ROOT / "cosmican", filename)

@app.get("/profile-system")
def profile_system_info():
    return jsonify(
        status="rollout-planned",
        service="ULTIMA Central Identity",
        note="The current membership API still uses separate site-scoped member accounts. Shared single sign-on must be implemented and migrated before this endpoint can report active."
    ), 202

@app.get("/autokrypt/")
def autokrypt_home():
    return send_from_directory(ROOT / "autokrypt", "index.html")

@app.get("/autokrypt/<path:filename>")
def autokrypt_assets(filename):
    return send_from_directory(ROOT / "autokrypt", filename)

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
    return jsonify(status="ok", service="ultima-central", mode="portfolio-launcher", cosmican="available", identity="not-configured", admin="locked-pending-sso"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
