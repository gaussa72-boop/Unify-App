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

# ULTIMA Update Matrix: authenticated, proposal-only agent orchestration.
from update_matrix import bp as update_matrix_bp
app.register_blueprint(update_matrix_bp)
csrf.exempt(update_matrix_bp)

# ULTIMA Telegram Hub webhook (token is supplied later via Render environment variables).
from telegram_hub import bp as telegram_bp
app.register_blueprint(telegram_bp)
csrf.exempt(telegram_bp)

# Standalone Aurealis Network social site and Telegram Mini App.
from network_site import bp as network_bp
app.register_blueprint(network_bp)

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


class PremiumTrial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False, index=True)
    started_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    ends_at = db.Column(db.DateTime, nullable=False)

class PremiumPaymentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    amount_usd = db.Column(db.Numeric(10, 2), nullable=False, default=10)
    currency = db.Column(db.String(8), nullable=False, default="USD")
    network = db.Column(db.String(24), nullable=False, default="Bitcoin")
    txid = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(24), nullable=False, default="pending_review")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

def utc_aware(value):
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


class SiteProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    site_key = db.Column(db.String(100), nullable=False, index=True)
    profile_data = db.Column(db.Text, nullable=False, default="{}")
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "site_key", name="uq_user_site_profile"),)



class RegistrationApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(254), nullable=False, index=True)
    phone = db.Column(db.String(40), nullable=False)
    postal_address = db.Column(db.String(500), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_data = db.Column(db.Text, nullable=False, default="{}")
    status = db.Column(db.String(24), nullable=False, default="pending", index=True)
    decision_note = db.Column(db.String(1000), nullable=False, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.String(254), nullable=True)


PAGE = """
<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ULTIMA · Unify</title>
<style>
:root{color-scheme:dark;--bg:#080d18;--panel:#111b2d;--line:#263750;--gold:#e7c879;--cyan:#5ce1e6;--muted:#a8b5c9}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -20%,#754b2c 0,transparent 45%),radial-gradient(ellipse at 90% 40%,#3b261b 0,transparent 35%),linear-gradient(135deg,#080a12,#17121a 55%,#090c14);color:#f3e9d5;font:16px system-ui;position:relative;overflow-x:hidden}body:before,body:after{content:'⚙';position:fixed;z-index:-1;color:#c08b52;opacity:.13;font-size:420px;line-height:1;pointer-events:none;animation:gearspin 90s linear infinite}body:before{left:-120px;top:10vh}body:after{content:'⚙';right:-110px;bottom:-80px;font-size:360px;animation-direction:reverse}@keyframes gearspin{to{transform:rotate(360deg)}}main{max-width:980px;margin:7vh auto;padding:24px}.brand{letter-spacing:.28em;color:var(--gold);font-size:13px}.hero{display:flex;gap:18px;align-items:center;margin:18px 0 30px}.orb{width:64px;height:64px;border:1px solid var(--cyan);border-radius:50%;box-shadow:0 0 32px #5ce1e655,inset 0 0 24px #5ce1e633;flex:none}.orb:after{content:"";display:block;width:12px;height:12px;margin:25px;background:var(--gold);border-radius:50%;box-shadow:0 0 18px var(--gold)}h1{font-size:clamp(30px,6vw,54px);margin:0;color:#f4e8d3;text-shadow:0 3px 20px #c18b4a55}.brand{color:#e2bd7d}p{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.panel{background:linear-gradient(145deg,#241b18ed,#111622f2 65%,#17131a);border:1px solid #8c673e;border-radius:12px;padding:22px;box-shadow:0 18px 55px #0009,inset 0 1px #e4c18a22;position:relative}.panel:before{content:'✧';position:absolute;right:16px;top:10px;color:#d6ad6e88;font-size:20px}input,textarea{width:100%;margin:8px 0 14px;padding:13px;border-radius:10px;border:1px solid var(--line);background:#091321;color:white}button{padding:12px 18px;border:1px solid #c59a5b;border-radius:5px;background:linear-gradient(100deg,#9b6b3c,#ead09a);color:#17100b;font-weight:700;cursor:pointer;box-shadow:0 4px 14px #0005}.muted{font-size:13px;color:var(--muted)}a{color:var(--cyan)}.flash{color:var(--gold);margin:10px 0}
</style><main><div class="brand">ULTIMA NETWORK · UNIFY</div><div class="hero"><div class="orb"></div><div><h1>Ein Konto. Dein Netzwerk.</h1><p>Zentrale Anmeldung und persönliche Profile für verbundene Websites.</p></div></div>
{% for m in get_flashed_messages() %}<div class="flash">{{m}}</div>{% endfor %}
{% if user %}
<div class="grid"><section class="panel"><h2>Dein Profil</h2><p>{{user.email}}</p><p>Rolle: <b>{{user.role}}</b></p>{% if trial_active %}<p style="color:#8dd8b6">Premium-Testphase aktiv · kostenlos bis {{trial.ends_at.strftime("%d.%m.%Y")}}</p>{% elif trial_expired %}<p style="color:#e7c879">Premium-Testphase beendet · Zahlung erforderlich</p>{% endif %}<p><a href="/assistant/">ULTIMA AI · Assistent öffnen ↗</a></p><p><a href="/network/">ULTIMA Social · Community & Messenger ↗</a></p>
<p><a href="https://ate-rea-characterverse.onrender.com/avatar.html">3D Avatar-Singularität · CharakterVerse ↗</a></p>{% if user.role == "SUPERADMIN" and user.email|lower == "ariandomimate@gmail.com" %}<p><a href="/admin/applications/">Zugangsanträge verwalten ↗</a></p>{% endif %}<form method="post" action="/logout"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><button>Abmelden</button></form></section>
<section class="panel"><h2>Website-Profil speichern</h2><form method="post" action="/profile"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>Website-Kennung</label><input name="site_key" placeholder="z. B. lichtkrieger" required maxlength="100"><label>Profilinformationen (JSON)</label><textarea name="profile_data" rows="4" placeholder='{"anzeigename":"...","interessen":[]}'></textarea><button>Profil speichern</button></form></section></div>
<section class="panel" style="margin-top:16px"><h2>Deine Website-Profile</h2>{% if profiles %}{% for p in profiles %}<p><b>{{p.site_key}}</b> · {{p.profile_data}}</p>{% endfor %}{% else %}<p>Noch keine Website-Profile gespeichert.</p>{% endif %}</section>
{% else %}
<div class="grid"><section class="panel"><h2>Zugang beantragen</h2><p>Alle Zugänge zu verbundenen ULTIMA-Websites werden erst nach persönlicher Freigabe durch den Superadministrator aktiviert.</p><form method="post" action="/register"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>Vor- und Nachname</label><input name="full_name" required maxlength="160" autocomplete="name"><label>E-Mail-Adresse</label><input name="email" type="email" required maxlength="254" autocomplete="email"><label>Telefonnummer</label><input name="phone" type="tel" required maxlength="40" autocomplete="tel"><label>Vollständige Anschrift</label><input name="postal_address" required maxlength="500" autocomplete="street-address"><label>Passwort (mindestens 12 Zeichen)</label><input name="password" type="password" minlength="12" required autocomplete="new-password"><label>Profil: Interessen, Träume, Ziele und gewünschte Eigenschaften</label><textarea name="profile_data" rows="5" maxlength="5000" placeholder="Welche Interessen, Ziele, Träume und Profilmerkmale möchtest du hinterlegen?"></textarea><label><input type="checkbox" name="privacy_consent" value="yes" required style="width:auto"> Ich stimme der Verarbeitung meiner Angaben zur Zugangsprüfung zu. Die Angaben werden nur hierfür verwendet und nicht öffentlich angezeigt.</label><button>Zugang beantragen</button></form><p class="muted">Dein Konto wird erst nach Freigabe erstellt. Die Angaben werden nicht automatisch veröffentlicht.</p></section>
<section class="panel"><h2>Anmelden</h2><form method="post" action="/login"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><input type="hidden" name="next" value="{{request.args.get('next', '/')}}"><label>E-Mail</label><input name="email" type="email" required><label>Passwort</label><input name="password" type="password" required><button>Anmelden</button><p class="muted"><a href="/forgot-password">Passwort vergessen?</a></p></form></section></div>
{% endif %}<p class="muted">Sicherheitsstatus: Zugang nur nach manueller Freigabe. Passwörter werden ausschließlich gehasht gespeichert. Die Freigabe gilt zunächst für ULTIMA Unify; andere Websites müssen den zentralen Zugang zusätzlich technisch prüfen.</p>
{% if trial_expired %}
<div id="premium-modal" style="position:fixed;inset:0;background:#000b;z-index:99999;display:grid;place-items:center;padding:18px">
<section style="width:min(520px,100%);max-height:90vh;overflow:auto;background:#111b2d;border:1px solid #e7c879;border-radius:18px;padding:24px;box-shadow:0 20px 80px #000">
<h2 style="color:#e7c879">Deine kostenlose Premium-Zeit ist abgelaufen</h2>
<p>Für die KI-Premiumfunktionen wird eine Zahlung von <b>10 USD pro Monat</b> angefragt. Überweise über das Bitcoin-Netzwerk an diese Wallet:</p>
<div style="padding:12px;background:#091321;border:1px solid #263750;border-radius:10px;overflow-wrap:anywhere;font-weight:700">bc1q4q7lujkr8mcv9e7suet524uxjfwlaxm7aelq5y</div>
<p class="muted">Bitte prüfe vor dem Senden Netzwerk und Betrag. Der USD-Preis wird nicht automatisch in BTC umgerechnet. Sende niemals BTC an eine andere Adresse.</p>
<label for="premium-txid">Transaktions-ID (optional, falls bereits bezahlt)</label>
<input id="premium-txid" maxlength="128" placeholder="Bitcoin TXID">
<button type="button" id="premium-submit">Zahlungsanfrage senden</button>
<p id="premium-result" class="muted"></p>
{% if payment_pending %}<p style="color:#e7c879">Deine Zahlungsanfrage wartet auf manuelle Prüfung.</p>{% endif %}
</section></div>
<script>
document.getElementById('premium-submit').addEventListener('click',async()=>{
 const out=document.getElementById('premium-result'); const btn=document.getElementById('premium-submit');
 btn.disabled=true; out.textContent='Wird gespeichert …';
 try{
  const r=await fetch('/api/premium/payment-request',{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':'{{csrf_token()}}'},body:JSON.stringify({txid:document.getElementById('premium-txid').value})});
  const d=await r.json(); out.textContent=d.message||d.error||'Anfrage konnte nicht gespeichert werden.';
 }catch(e){out.textContent='Verbindung fehlgeschlagen. Bitte erneut versuchen.';}
 btn.disabled=false;
});
</script>
{% endif %}
</main></html>
"""

@app.after_request
def inject_network_launcher(response):
    # Make the central social network reachable from every HTML page served by ULTIMA.
    if response.mimetype == "text/html" and response.status_code == 200:
        try:
            body = response.get_data(as_text=True)
            if "</body>" in body:
                if "ultima-social-launcher" not in body:
                    body = body.replace("</body>", '<script src="/network-widget.js" defer></script></body>', 1)
                if 'href="/urheberrecht/"' not in body:
                    body = body.replace("</body>", '<footer style="padding:18px 24px;text-align:center;color:#b9ad9a;font:13px system-ui;border-top:1px solid #735637"><a href="/urheberrecht/" style="color:#e5bd79">✦ Königliches Urheberrechts-Zertifikat · © Adriano Luca Gauß</a></footer></body>', 1)
                if 'href="/impressum/"' not in body:
                    body = body.replace("</body>", '<footer style="padding:18px 24px;text-align:center;color:#b9ad9a;font:13px system-ui;border-top:1px solid #735637;display:flex;justify-content:center;gap:18px;flex-wrap:wrap"><a href="/impressum/" style="color:#e5bd79">Impressum · Projektbeschreibung · © Adriano Luca Gauß</a><a href="/premium-uebersicht/" style="color:#5ce1e6">KI-Premium-Übersicht · Preise & Laufzeiten</a></footer></body>', 1)
                response.set_data(body)
        except Exception:
            pass
    return response


@app.context_processor
def inject_csrf():
    from flask_wtf.csrf import generate_csrf
    return {"csrf_token": generate_csrf}

@app.get("/")
def home():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    profiles = SiteProfile.query.filter_by(user_id=user.id).order_by(SiteProfile.site_key).all() if user else []
    trial = PremiumTrial.query.filter_by(user_id=user.id).first() if user else None
    trial_active = bool(trial and utc_aware(trial.ends_at) > datetime.now(timezone.utc))
    payment_pending = bool(user and PremiumPaymentRequest.query.filter_by(user_id=user.id, status="pending_review").first())
    trial_expired = bool(user and trial and not trial_active)
    return render_template_string(PAGE, user=user, profiles=profiles, trial=trial, trial_active=trial_active, trial_expired=trial_expired, payment_pending=payment_pending)

@app.get("/register")
def registration_page():
    return render_template_string("""<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ULTIMA · Zugang beantragen</title><style>
    *{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% 0,#273d5a,#080d18 65%);color:#f4ead8;font:16px system-ui;display:grid;place-items:center;padding:20px}.card{width:min(680px,100%);background:#111b2d;border:1px solid #a27c4d;border-radius:18px;padding:clamp(20px,5vw,38px);box-shadow:0 24px 90px #0009}h1{color:#e7c879}p{color:#a8b5c9}label{display:block;margin-top:14px}input,textarea{width:100%;padding:13px;margin-top:6px;background:#091321;color:white;border:1px solid #40506b;border-radius:8px}button{margin-top:18px;padding:13px 20px;background:linear-gradient(100deg,#9b6b3c,#ead09a);border:0;border-radius:8px;font-weight:800}a{color:#5ce1e6}.hint{font-size:12px;line-height:1.6}
    </style><main class="card"><div style="letter-spacing:.2em;color:#e7c879">ULTIMA · CENTRAL ACCESS</div><h1>Persönlichen Zugang beantragen</h1><p>Ein Antrag für die verbundenen Websites und zukünftige Projekte. Die Freigabe erfolgt ausschließlich durch den Superadministrator.</p>
    <form method="post" action="/register"><input type="hidden" name="csrf_token" value="{{csrf_token()}}">
    <label>Vor- und Nachname<input name="full_name" required maxlength="160" autocomplete="name"></label>
    <label>E-Mail-Adresse<input name="email" type="email" required maxlength="254" autocomplete="email"></label>
    <label>Telefonnummer<input name="phone" type="tel" required maxlength="40" autocomplete="tel"></label>
    <label>Vollständige Anschrift<input name="postal_address" required maxlength="500" autocomplete="street-address"></label>
    <label>Passwort (mindestens 12 Zeichen)<input name="password" type="password" minlength="12" required autocomplete="new-password"></label>
    <label>Profilangaben: Interessen, Träume, Ziele und gewünschte Profileigenschaften<textarea name="profile_data" rows="5" maxlength="5000" placeholder="Beschreibe, welche Interessen, Träume, Ziele und Profileigenschaften du hinterlegen möchtest."></textarea></label>
    <label><input type="checkbox" name="privacy_consent" value="yes" required style="width:auto"> Ich stimme der Verarbeitung meiner Angaben zur Prüfung des Zugangs zu.</label>
    <button type="submit">Antrag zur persönlichen Freigabe senden</button></form>
    <p class="hint">Dein Konto wird erst nach deiner Freigabe durch den Superadministrator erstellt. Antragsdaten werden nicht öffentlich angezeigt. Weitere Informationen: <a href="/">Anmeldung und ULTIMA-Portal</a>.</p></main></html>""")

@app.post("/register")
def register():
    email = request.form.get("email", "").strip().lower()
    full_name = request.form.get("full_name", "").strip()[:160]
    phone = request.form.get("phone", "").strip()[:40]
    postal_address = request.form.get("postal_address", "").strip()[:500]
    password = request.form.get("password", "")
    profile = request.form.get("profile_data", "").strip()[:5000]
    if request.form.get("privacy_consent") != "yes":
        flash("Bitte bestätige, dass deine Angaben zur Zugangsprüfung verarbeitet werden dürfen.")
    elif not all([email, full_name, phone, postal_address]) or len(password) < 12:
        flash("Bitte alle Pflichtfelder ausfüllen und ein Passwort mit mindestens 12 Zeichen wählen.")
    elif User.query.filter_by(email=email).first() or RegistrationApplication.query.filter_by(email=email, status="pending").first():
        flash("Für diese E-Mail existiert bereits ein Konto oder ein offener Antrag.")
    else:
        application = RegistrationApplication(
            full_name=full_name, email=email, phone=phone, postal_address=postal_address,
            password_hash=bcrypt.generate_password_hash(password).decode(),
            profile_data=profile, status="pending"
        )
        db.session.add(application)
        db.session.commit()
        # Email delivery is attempted only when SMTP is explicitly configured.
        try:
            import smtplib
            from email.message import EmailMessage
            host = os.environ.get("SMTP_HOST", "")
            sender = os.environ.get("SMTP_FROM", "")
            if host and sender:
                msg = EmailMessage()
                msg["Subject"] = "Neuer ULTIMA-Zugangsantrag"
                msg["From"] = sender
                msg["To"] = os.environ.get("SUPERADMIN_EMAIL", "ariandomimate@gmail.com")
                msg.set_content(
                    "Neuer Antrag wartet auf Freigabe in /admin/applications/\n\n"
                    f"Name: {full_name}\nE-Mail: {email}\nTelefon: {phone}\nAdresse: {postal_address}\n"
                    f"Profilangaben: {profile}\nAntragsnummer: {application.id}"
                )
                with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=15) as smtp:
                    smtp.starttls()
                    smtp.login(os.environ.get("SMTP_USER", ""), os.environ.get("SMTP_PASSWORD", ""))
                    smtp.send_message(msg)
        except Exception:
            app.logger.exception("Registration notification email could not be delivered")
        flash("Dein Antrag wurde gespeichert und wartet auf die persönliche Freigabe. Du kannst dich noch nicht anmelden.")
    return redirect(url_for("home"))


def require_superadmin():
    current = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    configured_email = os.environ.get("SUPERADMIN_EMAIL", "ariandomimate@gmail.com").strip().lower()
    if not current or current.role != "SUPERADMIN" or current.email.lower() != configured_email:
        return None
    return current


@app.get("/admin/applications/")
def registration_applications():
    admin = require_superadmin()
    if not admin:
        return redirect(url_for("home"))
    rows = RegistrationApplication.query.order_by(RegistrationApplication.created_at.desc()).limit(200).all()
    return render_template_string("""<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ULTIMA · Zugangsanträge</title><style>
    body{background:#080d18;color:#f4ead8;font:15px system-ui;margin:0;padding:24px}main{max-width:1050px;margin:auto}article{background:#111b2d;border:1px solid #705b3a;border-radius:14px;padding:18px;margin:14px 0}input,textarea{width:100%;box-sizing:border-box;background:#091321;color:white;border:1px solid #40506b;padding:10px;margin:6px 0}button{padding:10px 16px;margin:6px 8px 0 0;background:#e7c879;border:0;border-radius:6px;font-weight:bold}.reject{background:#62414a;color:white}.muted{color:#a8b5c9}pre{white-space:pre-wrap;overflow-wrap:anywhere}
    </style><main><h1>ULTIMA · Zugangsanträge</h1><p class="muted">Angemeldet als {{admin.email}} · Nur du kannst Anträge freigeben.</p><p><a href="/" style="color:#5ce1e6">Zurück zum Portal</a></p>
    {% for a in rows %}<article><h2>#{{a.id}} · {{a.full_name}}</h2><p>Status: <b>{{a.status}}</b> · {{a.created_at.strftime("%d.%m.%Y %H:%M UTC")}}</p><p>E-Mail: {{a.email}}<br>Telefon: {{a.phone}}<br>Adresse: {{a.postal_address}}</p><h3>Profilangaben · Interessen · Träume · Ziele</h3><pre>{{a.profile_data}}</pre>{% if a.status == "pending" %}<form method="post" action="/admin/applications/{{a.id}}/decision"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>Notiz (optional)</label><input name="decision_note" maxlength="1000"><button name="decision" value="approve">Freigeben</button><button class="reject" name="decision" value="reject">Ablehnen</button></form>{% else %}<p class="muted">Entscheidung: {{a.decision_note}} · {{a.reviewed_by or ""}}</p>{% endif %}</article>{% else %}<p>Keine Anträge vorhanden.</p>{% endfor %}</main></html>""", rows=rows, admin=admin)


@app.post("/admin/applications/<int:application_id>/decision")
def decide_registration(application_id):
    admin = require_superadmin()
    if not admin:
        return jsonify(error="superadmin_required"), 403
    application = db.session.get(RegistrationApplication, application_id)
    if not application or application.status != "pending":
        flash("Antrag nicht gefunden oder bereits entschieden.")
        return redirect(url_for("registration_applications"))
    decision = request.form.get("decision")
    note = request.form.get("decision_note", "").strip()[:1000]
    if decision == "approve":
        if User.query.filter_by(email=application.email).first():
            flash("Für diese E-Mail existiert bereits ein Konto. Antrag nicht freigegeben.")
            return redirect(url_for("registration_applications"))
        user = User(email=application.email, password_hash=application.password_hash, role="USER")
        db.session.add(user)
        db.session.flush()
        now = datetime.now(timezone.utc)
        db.session.add(PremiumTrial(user_id=user.id, started_at=now, ends_at=now + timedelta(days=1)))
        application.status = "approved"
        application.decision_note = note or "Freigegeben"
    elif decision == "reject":
        application.status = "rejected"
        application.decision_note = note or "Abgelehnt"
    else:
        return jsonify(error="invalid_decision"), 400
    application.reviewed_at = datetime.now(timezone.utc)
    application.reviewed_by = admin.email
    db.session.commit()
    # Notify applicant only if SMTP is configured; do not claim delivery otherwise.
    try:
        import smtplib
        from email.message import EmailMessage
        host, sender = os.environ.get("SMTP_HOST", ""), os.environ.get("SMTP_FROM", "")
        if host and sender:
            msg = EmailMessage()
            msg["Subject"] = "Dein ULTIMA-Zugangsantrag: " + application.status
            msg["From"] = sender
            msg["To"] = application.email
            msg.set_content("Dein Antrag wurde " + ("freigegeben." if decision == "approve" else "abgelehnt.") + "\n" + note)
            with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=15) as smtp:
                smtp.starttls()
                smtp.login(os.environ.get("SMTP_USER", ""), os.environ.get("SMTP_PASSWORD", ""))
                smtp.send_message(msg)
    except Exception:
        app.logger.exception("Applicant notification email could not be delivered")
    flash("Antrag wurde " + ("freigegeben." if decision == "approve" else "abgelehnt."))
    return redirect(url_for("registration_applications"))


class AdminBootstrapUsed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(64), unique=True, nullable=False)
    used_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


@app.route("/admin-setup/<token>", methods=["GET", "POST"])
def admin_setup(token):
    import hashlib, hmac
    configured = os.environ.get("ULTIMA_ADMIN_SETUP_TOKEN", "")
    owner_email = os.environ.get("SUPERADMIN_EMAIL", "ariandomimate@gmail.com").strip().lower()
    digest = hashlib.sha256(token.encode()).hexdigest()
    valid = bool(configured and owner_email and hmac.compare_digest(token, configured))
    if valid and AdminBootstrapUsed.query.filter_by(token_hash=digest).first():
        valid = False
    if not valid:
        return "<h1>Setup-Link ungültig oder bereits verwendet.</h1>", 410
    owner = User.query.filter(db.func.lower(User.email) == owner_email).first()
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if len(password) < 12 or password != confirm:
            flash("Passwörter müssen übereinstimmen und mindestens 12 Zeichen lang sein.")
            return redirect(request.url)
        if owner is None:
            owner = User(email=owner_email, password_hash=bcrypt.generate_password_hash(password).decode(), role="SUPERADMIN")
            db.session.add(owner)
            db.session.flush()
            now = datetime.now(timezone.utc)
            db.session.add(PremiumTrial(user_id=owner.id, started_at=now, ends_at=now + timedelta(days=30)))
        else:
            owner.password_hash = bcrypt.generate_password_hash(password).decode()
            owner.role = "SUPERADMIN"
        db.session.add(AdminBootstrapUsed(token_hash=digest))
        db.session.commit()
        session.clear(); session["user_id"] = owner.id; session["role"] = "SUPERADMIN"
        flash("Superadmin-Zugang eingerichtet. Du bist angemeldet.")
        return redirect(url_for("home"))
    return render_template_string("""<!doctype html><html lang=de><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>ULTIMA · Admin Setup</title><style>body{background:radial-gradient(ellipse at top,#65452c,#090d17 70%);color:#f5e9d2;font:16px system-ui;display:grid;place-items:center;min-height:100vh}.panel{width:min(440px,92vw);padding:28px;background:#171b25;border:1px solid #b58a51;border-radius:12px}input{display:block;width:100%;box-sizing:border-box;margin:12px 0;padding:13px;background:#090f1a;color:white;border:1px solid #86643e;border-radius:5px}button{padding:12px 18px;background:#e7c879;border:0;border-radius:5px;font-weight:bold}</style><section class=panel><h1>ULTIMA · Superadmin einrichten</h1><p>Lege ein neues Passwort für {{owner_email}} fest. Falls das Konto noch nicht existiert, wird es dabei angelegt.</p>{% for m in get_flashed_messages() %}<p>{{m}}</p>{% endfor %}<form method=post><input type=hidden name=csrf_token value="{{csrf_token()}}"><label>Neues Passwort (mindestens 12 Zeichen)</label><input type=password name=password minlength=12 required autocomplete=new-password><label>Passwort wiederholen</label><input type=password name=confirm minlength=12 required autocomplete=new-password><button>Superadmin-Zugang aktivieren</button></form></section></html>""", owner_email=owner_email)

@app.get("/login")
def login_page():
    # Browser navigation to /login should display the central login page, not return 405.
    return redirect(url_for("home"))

@app.post("/login")
def login():
    email = request.form.get("email", "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, request.form.get("password", "")):
        session.clear(); session["user_id"] = user.id; session["role"] = user.role
        target = request.args.get("next") or request.form.get("next") or "/"
        if not target.startswith("/") or target.startswith("//"): target = "/"
        return redirect(target)
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

@app.get("/api/premium/status")
def premium_status():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user: return jsonify(error="authentication_required"), 401
    trial = PremiumTrial.query.filter_by(user_id=user.id).first()
    if not trial:
        return jsonify(premium=False, trial="not_eligible", message="Für dieses Konto wurde kein neuer 30-Tage-Testzeitraum registriert."), 200
    active = trial.ends_at > datetime.now(timezone.utc)
    pending = PremiumPaymentRequest.query.filter_by(user_id=user.id, status="pending_review").first()
    return jsonify(premium=active, trial="active" if active else "expired", ends_at=trial.ends_at.isoformat(), payment_pending=bool(pending)), 200

@app.post("/api/premium/payment-request")
def premium_payment_request():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user: return jsonify(error="authentication_required"), 401
    data = request.get_json(silent=True) or {}
    txid = str(data.get("txid", "")).strip()
    if len(txid) > 128: return jsonify(error="Ungültige TXID."), 400
    trial = PremiumTrial.query.filter_by(user_id=user.id).first()
    if not trial or trial.ends_at > datetime.now(timezone.utc):
        return jsonify(error="Die kostenlose Testphase ist noch aktiv oder nicht verfügbar."), 409
    existing = PremiumPaymentRequest.query.filter_by(user_id=user.id, status="pending_review").first()
    if existing: return jsonify(status="pending_review", message="Deine Zahlungsanfrage wartet bereits auf Prüfung."), 200
    payment = PremiumPaymentRequest(user_id=user.id, amount_usd=10, txid=txid or None, status="pending_review")
    db.session.add(payment); db.session.commit()
    return jsonify(status="pending_review", message="Zahlungsanfrage gespeichert. Premium wird erst nach manueller Prüfung freigeschaltet."), 201


@app.get("/update-matrix/")
def update_matrix_dashboard():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    if not user:
        return redirect(url_for("home"))
    if user.role != "SUPERADMIN":
        return jsonify(error="superadmin_required"), 403
    response = send_from_directory(os.path.dirname(__file__), "update-matrix.html")
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/render-console/")
def render_console():
    return send_from_directory(os.path.dirname(__file__), "render-console.html")

@app.get("/assistant/")
@app.get("/ultima-ai/")
@app.get("/ultima-ai", strict_slashes=False)
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
    context = "\n".join([
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
        "Bewahre seine Identität und Stimme konsistent.\n" + context +
        "\nArbeite transparent. Erfinde keine ausgeführten Aktionen. "
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

@app.get("/network-widget.js")
def network_widget():
    return send_from_directory(os.path.dirname(__file__), "network-widget.js", mimetype="application/javascript")

@app.get("/urheberrecht/")
@app.get("/urheberrecht", strict_slashes=False)
def royal_certificate():
    response = send_from_directory(os.path.dirname(__file__), "urheberrecht.html")
    response.headers["Cache-Control"] = "public, max-age=300"
    return response

@app.get("/impressum/")
@app.get("/impressum", strict_slashes=False)
def impressum():
    response = send_from_directory(os.path.dirname(__file__), "impressum.html")
    response.headers["Cache-Control"] = "public, max-age=300"
    return response

@app.get("/premium-uebersicht/")
@app.get("/premium-uebersicht", strict_slashes=False)
def premium_overview():
    response = send_from_directory(os.path.dirname(__file__), "premium-uebersicht.html")
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok", database="connected"), 200
    except Exception:
        return jsonify(status="degraded", database="unavailable"), 503

from network_social import register_social
register_social(app, db, User)

from auth_recovery import register_auth_recovery
register_auth_recovery(app, db, User, bcrypt)

with app.app_context():
    db.create_all()
    # Keep the configured ULTIMA master account privileged even when it
    # was registered before SUPERADMIN_EMAIL was configured.
    owner_email = os.environ.get("SUPERADMIN_EMAIL", "ariandomimate@gmail.com").strip().lower()
    if owner_email:
        owner = User.query.filter(db.func.lower(User.email) == owner_email).first()
        if owner and owner.role != "SUPERADMIN":
            owner.role = "SUPERADMIN"
            db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
