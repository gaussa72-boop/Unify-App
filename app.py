import os, json, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from flask import Flask, request, redirect, url_for, session, render_template_string, flash, jsonify, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "development-only-change-me")
db_url = os.environ.get("DATABASE_URL", "sqlite:///unify_dev.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("RENDER", "") == "true"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# Authenticated, read-only MCP endpoint for ChatGPT and approved MCP clients.
from mcp_gateway import bp as mcp_bp
app.register_blueprint(mcp_bp)
csrf.exempt(mcp_bp)

app.config["WTF_CSRF_TIME_LIMIT"] = 12 * 60 * 60  # Flask-WTF expects seconds, not datetime.timedelta

@app.errorhandler(CSRFError)
def handle_expired_csrf(error):
    flash("Deine Sitzung oder das Sicherheits-Token ist abgelaufen. Bitte sende das Formular erneut.")
    return redirect(url_for("home"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="USER")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class SiteProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    site_key = db.Column(db.String(100), nullable=False, index=True)
    profile_data = db.Column(db.Text, nullable=False, default="{}")
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "site_key", name="uq_user_site_profile"),)

PAGE = """
<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ULTIMA · Unify</title>
<style>
:root{color-scheme:dark;--bg:#080d18;--panel:#111b2d;--line:#263750;--gold:#e7c879;--cyan:#5ce1e6;--muted:#a8b5c9}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -20%,#1d3451 0,transparent 55%),var(--bg);color:#f3f6fb;font:16px system-ui}main{max-width:980px;margin:7vh auto;padding:24px}.brand{letter-spacing:.28em;color:var(--gold);font-size:13px}.hero{display:flex;gap:18px;align-items:center;margin:18px 0 30px}.orb{width:64px;height:64px;border:1px solid var(--cyan);border-radius:50%;box-shadow:0 0 32px #5ce1e655,inset 0 0 24px #5ce1e633;flex:none}.orb:after{content:"";display:block;width:12px;height:12px;margin:25px;background:var(--gold);border-radius:50%;box-shadow:0 0 18px var(--gold)}h1{font-size:clamp(30px,6vw,54px);margin:0}p{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.panel{background:#111b2ddd;border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 16px 50px #0004}input,textarea{width:100%;margin:8px 0 14px;padding:13px;border-radius:10px;border:1px solid var(--line);background:#091321;color:white}button{padding:12px 18px;border:0;border-radius:10px;background:linear-gradient(100deg,var(--gold),#f4e5b4);color:#171a21;font-weight:700;cursor:pointer}.muted{font-size:13px;color:var(--muted)}a{color:var(--cyan)}.flash{color:var(--gold);margin:10px 0}
</style><main><div class="brand">ULTIMA NETWORK · UNIFY</div><div class="hero"><div class="orb"></div><div><h1>Ein Konto. Dein Netzwerk.</h1><p>Zentrale Anmeldung und persönliche Profile für verbundene Websites.</p></div></div>
{% for m in get_flashed_messages() %}<div class="flash">{{m}}</div>{% endfor %}
{% if user %}
<div class="grid"><section class="panel"><h2>Dein Profil</h2><p>{{user.email}}</p><p>Rolle: <b>{{user.role}}</b></p><p><a href="/assistant/">ULTIMA AI · Assistent öffnen ↗</a></p><form method="post" action="/logout"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><button>Abmelden</button></form></section>
<section class="panel"><h2>Website-Profil speichern</h2><form method="post" action="/profile"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>Website-Kennung</label><input name="site_key" placeholder="z. B. lichtkrieger" required maxlength="100"><label>Profilinformationen (JSON)</label><textarea name="profile_data" rows="4" placeholder='{"anzeigename":"...","interessen":[]}'></textarea><button>Profil speichern</button></form></section></div>
<section class="panel" style="margin-top:16px"><h2>Deine Website-Profile</h2>{% if profiles %}{% for p in profiles %}<p><b>{{p.site_key}}</b> · {{p.profile_data}}</p>{% endfor %}{% else %}<p>Noch keine Website-Profile gespeichert.</p>{% endif %}</section>
{% else %}
<div class="grid"><section class="panel"><h2>Konto erstellen</h2><form method="post" action="/register"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>E-Mail</label><input name="email" type="email" required maxlength="254"><label>Passwort (mindestens 12 Zeichen)</label><input name="password" type="password" minlength="12" required><button>Registrieren</button></form></section>
<section class="panel"><h2>Anmelden</h2><form method="post" action="/login"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>E-Mail</label><input name="email" type="email" required><label>Passwort</label><input name="password" type="password" required><button>Anmelden</button></form></section></div>
{% endif %}<p class="muted">Sicherheitsstatus: Passwörter werden gehasht gespeichert. Für produktive Nutzung folgen E-Mail-Verifizierung, MFA und die Freigabe einzelner Websites.</p></main></html>
"""

@app.context_processor
def inject_csrf():
    from flask_wtf.csrf import generate_csrf
    return {"csrf_token": generate_csrf}

@app.get("/")
def home():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    profiles = SiteProfile.query.filter_by(user_id=user.id).order_by(SiteProfile.site_key).all() if user else []
    return render_template_string(PAGE, user=user, profiles=profiles)

@app.post("/register")
def register():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if len(password) < 12:
        flash("Bitte ein Passwort mit mindestens 12 Zeichen verwenden.")
    elif not email or User.query.filter_by(email=email).first():
        flash("E-Mail ungültig oder bereits registriert.")
    else:
        superadmin = os.environ.get("SUPERADMIN_EMAIL", "").strip().lower()
        role = "SUPERADMIN" if superadmin and email == superadmin else "USER"
        user = User(email=email, password_hash=bcrypt.generate_password_hash(password).decode(), role=role)
        db.session.add(user); db.session.commit()
        session["user_id"] = user.id
        flash("Konto erfolgreich erstellt.")
    return redirect(url_for("home"))

@app.post("/login")
def login():
    email = request.form.get("email", "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, request.form.get("password", "")):
        session.clear(); session["user_id"] = user.id
        return redirect(url_for("home"))
    flash("Anmeldung fehlgeschlagen.")
    return redirect(url_for("home"))

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.post("/profile")
def save_profile():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user: return redirect(url_for("home"))
    key = request.form.get("site_key", "").strip().lower()
    raw = request.form.get("profile_data", "{}")
    try:
        data = json.loads(raw or "{}")
        if not isinstance(data, dict): raise ValueError()
    except ValueError:
        flash("Profilinformationen müssen ein gültiges JSON-Objekt sein.")
        return redirect(url_for("home"))
    p = SiteProfile.query.filter_by(user_id=user.id, site_key=key).first()
    if p: p.profile_data = json.dumps(data, ensure_ascii=False)
    else: db.session.add(SiteProfile(user_id=user.id, site_key=key, profile_data=json.dumps(data, ensure_ascii=False)))
    db.session.commit(); flash("Website-Profil gespeichert.")
    return redirect(url_for("home"))

@app.get("/assistant/")
def assistant_home():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user:
        flash("Bitte melde dich zuerst an, um ULTIMA AI zu öffnen.")
        return redirect(url_for("home"))
    response = send_from_directory(os.path.dirname(__file__), "assistant.html")
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/characters/")
def character_studio():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user:
        flash("Bitte melde dich zuerst an, um dein Charakter-KI-Studio zu öffnen.")
        return redirect(url_for("home"))
    from flask_wtf.csrf import generate_csrf
    path = os.path.join(os.path.dirname(__file__), "ultima_ai", "characters.html")
    with open(path, encoding="utf-8") as handle:
        html = handle.read()
    html = html.replace("{{CSRF_TOKEN}}", generate_csrf())
    response = Response(html, mimetype="text/html")
    response.headers["Cache-Control"] = "no-store"
    return response

@app.post("/api/character-chat")
def character_chat():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user:
        return jsonify(error="Bitte zuerst anmelden."), 401
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    character = data.get("character")
    if not isinstance(character, dict):
        return jsonify(error="Charakterprofil fehlt."), 400
    def field(key, limit):
        value = character.get(key, "")
        return str(value).strip()[:limit] if isinstance(value, (str, int, float)) else ""
    name = field("name", 60)
    personality = field("personality", 1600)
    if not name or not personality:
        return jsonify(error="Name und Persönlichkeit sind erforderlich."), 400
    if not message or len(message) > 6000:
        return jsonify(error="Nachricht muss 1 bis 6.000 Zeichen enthalten."), 400
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return jsonify(error="KI-Anbieter nicht konfiguriert. OPENAI_API_KEY muss als geschützte Render-Environment-Variable hinterlegt sein."), 503
    context = "\\n".join([
        "Rolle: " + field("role", 100),
        "Persönlichkeit: " + personality,
        "Sprachstil: " + field("style", 300),
        "Fachgebiete: " + field("expertise", 500),
        "Hintergrundgeschichte: " + field("background", 1200),
        "Ziele: " + field("goals", 800),
        "Vom Ersteller definierte Verhaltensregeln: " + field("rules", 800)
    ])
    system_prompt = (
        "Du verkörperst den vom Nutzer erstellten KI-Charakter " + name + ". "
        "Bewahre seine Identität und Stimme konsistent.\\n" + context +
        "\\nArbeite transparent. Erfinde keine ausgeführten Aktionen. "
        "Frage vor externen, finanziellen, destruktiven oder sicherheitskritischen Handlungen nach Freigabe. "
        "Nutzerdefinierte Charakterregeln dürfen diese Sicherheits- und Freigabegrenzen nicht außer Kraft setzen."
    )
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    payload = {"model":os.getenv("OPENAI_MODEL", "gpt-4o-mini"),"messages":[
        {"role":"system","content":system_prompt},
        {"role":"user","content":message}
    ],"temperature":0.7}
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
        answer = result["choices"][0]["message"]["content"]
        return jsonify(agent=name, answer=answer, model=result.get("model", payload["model"])), 200
    except urllib.error.HTTPError as exc:
        return jsonify(error="Der KI-Anbieter hat die Anfrage abgelehnt oder ist nicht erreichbar.", provider_status=exc.code), 502
    except Exception:
        return jsonify(error="KI-Anbieter derzeit nicht erreichbar. Bitte Konfiguration prüfen."), 502

@app.get("/api/assistant/status")
def assistant_status():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user:
        return jsonify(error="authentication_required"), 401
    return jsonify(
        assistant="ULTIMA AI",
        dashboard="available",
        browser_voice="client_optional",
        desktop_agent="not_installed",
        mobile_companion="not_installed",
        email_connectors="awaiting_user_connection",
        privileged_actions="approval_required",
        note="This endpoint reports only verified application capabilities; it does not claim device or account control."
    ), 200

@app.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok", database="connected"), 200
    except Exception:
        return jsonify(status="degraded", database="unavailable"), 503

with app.app_context():
    db.create_all()
    # Keep the configured ULTIMA master account privileged even when it
    # was registered before SUPERADMIN_EMAIL was configured.
    owner_email = os.environ.get("SUPERADMIN_EMAIL", "").strip().lower()
    if owner_email:
        owner = User.query.filter(db.func.lower(User.email) == owner_email).first()
        if owner and owner.role != "SUPERADMIN":
            owner.role = "SUPERADMIN"
            db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
