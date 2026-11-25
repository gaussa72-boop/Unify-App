import os, secrets, hashlib, smtplib
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from flask import request, redirect, url_for, flash, render_template_string
from sqlalchemy import text

PAGE = r'''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ULTIMA · Passwort wiederherstellen</title><style>body{margin:0;background:#080d18;color:#f3f6fb;font:16px system-ui;display:grid;min-height:100vh;place-items:center}.panel{width:min(460px,calc(100% - 40px));background:#111b2d;border:1px solid #263750;border-radius:18px;padding:28px;box-sizing:border-box}h1{color:#e7c879}input{width:100%;box-sizing:border-box;margin:10px 0 18px;padding:14px;border-radius:10px;background:#091321;border:1px solid #263750;color:white}button{padding:12px 18px;border:0;border-radius:10px;background:#e7c879;font-weight:700}a{color:#5ce1e6}.muted{color:#a8b5c9;font-size:13px}.flash{color:#e7c879}</style><section class="panel"><h1>Passwort wiederherstellen</h1>{% for m in get_flashed_messages() %}<p class="flash">{{m}}</p>{% endfor %}{% if mode == 'request' %}<p>Gib die E-Mail-Adresse deines ULTIMA-Kontos ein. Wenn das Konto existiert, senden wir einen zeitlich begrenzten Link.</p><form method="post"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>E-Mail-Adresse</label><input name="email" type="email" autocomplete="email" required><button>Wiederherstellungslink senden</button></form>{% else %}<form method="post"><input type="hidden" name="csrf_token" value="{{csrf_token()}}"><label>Neues Passwort (mindestens 12 Zeichen)</label><input name="password" type="password" minlength="12" autocomplete="new-password" required><label>Passwort wiederholen</label><input name="confirm" type="password" minlength="12" autocomplete="new-password" required><button>Passwort ändern</button></form>{% endif %}<p class="muted"><a href="/">Zurück zur Anmeldung</a></p></section></html>'''

def register_auth_recovery(app, db, User, bcrypt):
    class PasswordReset(db.Model):
        __tablename__ = "password_reset_token"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
        token_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
        expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
        used_at = db.Column(db.DateTime(timezone=True), nullable=True)
        created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def send_reset_email(user, token):
        host = os.environ.get("SMTP_HOST", "").strip()
        sender = os.environ.get("SMTP_FROM", "").strip()
        if not host or not sender:
            app.logger.error("Password reset email unavailable: SMTP_HOST or SMTP_FROM missing")
            return False
        port = int(os.environ.get("SMTP_PORT", "587"))
        username = os.environ.get("SMTP_USERNAME", "")
        password = os.environ.get("SMTP_PASSWORD", "")
        use_ssl = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"
        base = os.environ.get("PUBLIC_BASE_URL", request.url_root.rstrip("/"))
        link = base.rstrip("/") + url_for("reset_password", token=token)
        msg = EmailMessage()
        msg["Subject"] = "ULTIMA – Passwort zurücksetzen"
        msg["From"] = sender
        msg["To"] = user.email
        msg.set_content("Du hast das Zurücksetzen deines ULTIMA-Passworts angefordert.\n\nÖffne innerhalb von 30 Minuten diesen Link:\n" + link + "\n\nWenn du das nicht angefordert hast, ignoriere diese E-Mail.")
        try:
            if use_ssl:
                with smtplib.SMTP_SSL(host, port, timeout=15) as server:
                    if username: server.login(username, password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(host, port, timeout=15) as server:
                    server.ehlo(); server.starttls(); server.ehlo()
                    if username: server.login(username, password)
                    server.send_message(msg)
            return True
        except Exception:
            app.logger.exception("Password reset email delivery failed")
            return False

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            user = User.query.filter(db.func.lower(User.email) == email).first() if email else None
            if user:
                now = datetime.now(timezone.utc)
                PasswordReset.query.filter_by(user_id=user.id, used_at=None).update({"used_at": now})
                token = secrets.token_urlsafe(32)
                record = PasswordReset(user_id=user.id, token_hash=hashlib.sha256(token.encode()).hexdigest(), expires_at=now + timedelta(minutes=30))
                db.session.add(record); db.session.commit()
                if not send_reset_email(user, token):
                    db.session.delete(record); db.session.commit()
                    flash("Der E-Mail-Versand ist noch nicht konfiguriert. Bitte später erneut versuchen.")
                    return render_template_string(PAGE, mode="request")
            flash("Wenn ein Konto zu dieser Adresse gehört, wurde ein Wiederherstellungslink versendet.")
            return redirect(url_for("home"))
        return render_template_string(PAGE, mode="request")

    @app.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token):
        digest = hashlib.sha256(token.encode()).hexdigest()
        record = PasswordReset.query.filter_by(token_hash=digest, used_at=None).first()
        now = datetime.now(timezone.utc)
        expires = record.expires_at if record else None
        if not record or (expires.replace(tzinfo=timezone.utc) if expires and expires.tzinfo is None else expires) <= now:
            flash("Der Link ist ungültig oder abgelaufen. Bitte fordere einen neuen an.")
            return redirect(url_for("forgot_password"))
        if request.method == "POST":
            password = request.form.get("password", "")
            if len(password) < 12 or password != request.form.get("confirm", ""):
                flash("Passwörter müssen übereinstimmen und mindestens 12 Zeichen lang sein.")
                return render_template_string(PAGE, mode="reset")
            user = db.session.get(User, record.user_id)
            if not user:
                flash("Konto nicht gefunden."); return redirect(url_for("forgot_password"))
            user.password_hash = bcrypt.generate_password_hash(password).decode()
            record.used_at = now
            PasswordReset.query.filter(PasswordReset.user_id == user.id, PasswordReset.id != record.id, PasswordReset.used_at == None).update({"used_at": now})
            db.session.commit()
            flash("Passwort erfolgreich geändert. Du kannst dich jetzt anmelden.")
            return redirect(url_for("home"))
        return render_template_string(PAGE, mode="reset")
