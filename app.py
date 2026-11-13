import os, json
from datetime import datetime, timezone
from flask import Flask, request, redirect, url_for, session, render_template_string, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

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
<div class="grid"><section class="panel"><h2>Dein Profil</h2><p>{{user.email}}</p><p>Rolle: <b>{{user.role}}</b></p><form method="post" action="/logout"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><button>Abmelden</button></form></section>
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

@app.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok", database="connected"), 200
    except Exception:
        return jsonify(status="degraded", database="unavailable"), 503

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
