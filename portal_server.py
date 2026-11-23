import os
from flask import Flask, send_from_directory, jsonify, Response, redirect
from pathlib import Path

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)

from ultima_ai import bp as ultima_ai_bp
app.register_blueprint(ultima_ai_bp)

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
    <a href="/ultima-ai/" style="display:inline-block;margin-left:10px;padding:8px 12px;border:1px solid #e4c477;border-radius:9px;color:#e4c477;text-decoration:none;letter-spacing:.04em;font-size:12px">ULTIMA AI ↗</a>\n    <a href="https://ate-rea-characterverse.onrender.com/creator.html" style="display:inline-block;margin-left:10px;padding:8px 12px;border:1px solid #65dce0;border-radius:9px;color:#65dce0;text-decoration:none;letter-spacing:.04em;font-size:12px">AI CHARACTER CREATOR ↗</a>\n    <a href="https://aurealis-omnia.onrender.com/" style="display:inline-block;margin-left:10px;padding:8px 12px;border:1px solid #e4c477;border-radius:9px;color:#e4c477;text-decoration:none;letter-spacing:.04em;font-size:12px">AUREALIS OMNIA ↗</a>
    <a href="/cosmican/" style="display:inline-block;margin-left:18px;padding:8px 12px;border:1px solid #65dce0;border-radius:9px;color:#65dce0;text-decoration:none;letter-spacing:.04em;font-size:12px">COSMICAN LUX SYNDICATE ↗</a>
    <a href="https://ultima-membership-api.onrender.com/portal" style="display:inline-block;margin-left:10px;padding:8px 12px;border:1px solid #e4c477;border-radius:9px;color:#e4c477;text-decoration:none;letter-spacing:.04em;font-size:12px">ULTIMA KONTO & WEBSITE-STUDIO ↗</a>
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
    html = html.replace("</main>", "\n    <section id=\"ultima-community-sites\" style=\"margin:18px 0;padding:20px;border:1px solid #65dce055;border-radius:15px;background:#101d2d\">\n      <div style=\"color:#65dce0;font-size:11px;letter-spacing:.18em\">ULTIMA COMMUNITY · PUBLIC DIRECTORY</div>\n      <h2 style=\"margin:8px 0\">Websites aus dem Netzwerk</h2>\n      <p style=\"color:#9caac0\">Entdecke öffentliche Projekte von Mitgliedern. Registrierte Nutzer können ihre eigenen Websites eintragen, bearbeiten und veröffentlichen.</p>\n      <div id=\"ultima-community-projects\" style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px\"><p style=\"color:#9caac0\">Öffentliche Websites werden geladen …</p></div>\n      <a href=\"https://ultima-membership-api.onrender.com/portal\" style=\"display:inline-block;margin-top:14px;padding:10px 14px;border-radius:8px;background:#e4c477;color:#111827;text-decoration:none;font-weight:700\">Website eintragen / Profil öffnen ↗</a>\n    </section>\n" + "</main>", 1)
    html = html.replace("</body>", """<script>
(async()=>{const root=document.getElementById('ultima-community-projects');if(!root)return;try{const r=await fetch('https://ultima-membership-api.onrender.com/api/global/public-projects');const d=await r.json();root.innerHTML=(d.projects||[]).map(p=>'<article style="padding:14px;border:1px solid #334761;border-radius:12px;background:#0b1524"><b>'+String(p.name).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))+'</b><p style="color:#9caac0">'+String(p.description||'').replace(/[&<>"']/g,'')+'</p><small>'+String(p.category||'Website')+'</small><p><a rel="noopener noreferrer" target="_blank" href="'+p.url+'">Website öffnen ↗</a></p></article>').join('')||'<p style="color:#9caac0">Noch keine öffentlichen Websites.</p>'}catch(e){root.textContent='Das öffentliche Verzeichnis ist gerade nicht erreichbar.'}})();
</script></body>""", 1)
    return Response(html, mimetype="text/html")

@app.get("/account/")
def account_home():
    return redirect("https://ultima-membership-api.onrender.com/portal", code=302)

@app.get("/admin/")
def admin_home():
    return send_from_directory(ROOT / "admin", "index.html")

@app.get("/ai-studios/")
def ai_studios_home():
    return send_from_directory(ROOT / "ai-studios", "index.html")

@app.get("/cosmican/")
def cosmican_home():
    return send_from_directory(ROOT / "cosmican", "index.html")

@app.get("/cosmican/<path:filename>")
def cosmican_assets(filename):
    return send_from_directory(ROOT / "cosmican", filename)

@app.get("/profile-system")
def profile_system_info():
    return jsonify(
        status="enabled",
        service="ULTIMA Central Identity",
        note="Central ULTIMA identity and user-owned website registry are enabled on the membership API. Existing site-scoped member accounts remain separate until each site adopts the global identity widget."
    ), 202

@app.get("/autokrypt/")
def autokrypt_home():
    return send_from_directory(ROOT / "autokrypt", "index.html")

@app.get("/autokrypt/<path:filename>")
def autokrypt_assets(filename):
    return send_from_directory(ROOT / "autokrypt", filename)

@app.get("/data/<path:filename>")
def project_data(filename):
    return send_from_directory(ROOT / "data", filename)

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

@app.get("/updates/")
def updates_home():
    return send_from_directory(ROOT / "updates", "index.html")

@app.get("/updates/<path:filename>")
def updates_assets(filename):
    return send_from_directory(ROOT / "updates", filename)

@app.get("/health")
def health():
    return jsonify(status="ok", service="ultima-central", mode="portfolio-launcher", cosmican="available", identity="global-identity-api", website_registry="public", admin="separate-secure-control-center"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
