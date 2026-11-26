"""ULTIMA Telegram hub webhook. Read-only navigation until payment/admin APIs are explicitly wired."""
import json
import os
import urllib.request
import hmac
from flask import Blueprint, request, jsonify

bp = Blueprint("ultima_telegram", __name__)
_WEBHOOK_REGISTERED = False

SITES = [
    ("ULTIMA Central", "Zentrales Konto, Projektübersicht und Verwaltungsportal.", "https://ultima-unify-45ne.onrender.com/"),
    ("AUREALIS OMNIA", "AUREALIS-KI, Wallet- und Mining-Projekt.", "https://aurealis-omnia.onrender.com/"),
    ("Ate Rea CharacterVerse", "Charaktere, KI-Avatare und kreative Ate-Rea-Welt.", "https://ate-rea-characterverse.onrender.com/"),
    ("Quantum KI Ultra Pro", "KI-Plattform und Assistentenprojekt.", "https://quantum-ki-ultra-pro-v2.onrender.com/"),
    ("BullRun Apparel", "BullRun Apparel Webshop.", "https://bullrun-apparel.onrender.com/"),
    ("The Lord Agent Network", "Agenten- und KI-Netzwerk.", "https://the-lord-agent-network.onrender.com/"),
    ("IONOS-7", "IONOS KI-Portal.", "https://ionos-7-gauss-portal.onrender.com/"),
    ("Neuroforge", "Neuroforge Systems.", "https://neuroforge-2035.onrender.com/"),
    ("Quantum Mirror", "Dark Wonderland-Spiel- und Erlebniswelt.", "https://quantum-mirror-dark-wonderland-ejc3.onrender.com/"),
]
SHOPS = [("Lyca", "Lyca-Webshop und Support"), ("Rothshild", "Rothshild-Shop und Community"), ("Parfum", "Parfum-Webshop")]

def _token():
    return os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()

def _api(method, payload):
    token = _token()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt")
    req = urllib.request.Request(
        "https://api.telegram.org/bot" + token + "/" + method,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))

def _menu():
    return {"inline_keyboard": [
        [{"text": "🌐 Websites & Programme", "callback_data": "sites"}],
        [{"text": "⭐ Premium & Kombi-Abos", "callback_data": "premium"}, {"text": "👤 Profil & Verwaltung", "callback_data": "profile"}],
        [{"text": "🛍 Webshops", "callback_data": "shops"}, {"text": "💛 Spenden", "callback_data": "donate"}],
        [{"text": "🔄 Update Matrix", "callback_data": "updates"}],
    ]}

def _send(chat_id, text, markup=None):
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    if markup:
        payload["reply_markup"] = markup
    _api("sendMessage", payload)

def _register_webhook_once():
    global _WEBHOOK_REGISTERED
    if _WEBHOOK_REGISTERED or not _token():
        return
    base = os.environ.get("TELEGRAM_PUBLIC_URL", "").strip().rstrip("/")
    secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "").strip()
    if not base or not secret:
        return
    try:
        _api("setWebhook", {"url": base + "/telegram/webhook", "secret_token": secret, "allowed_updates": ["message", "callback_query"], "drop_pending_updates": False})
        _WEBHOOK_REGISTERED = True
    except Exception:
        return

@bp.before_app_request
def register_webhook_on_first_request():
    _register_webhook_once()

@bp.post("/telegram/webhook")
def telegram_webhook():
    expected = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "").strip()
    supplied = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not expected or not supplied or not hmac.compare_digest(expected, supplied):
        return jsonify(ok=False), 403
    update = request.get_json(silent=True) or {}
    message = update.get("message") or {}
    callback = update.get("callback_query") or {}
    if message:
        chat_id = (message.get("chat") or {}).get("id")
        text = (message.get("text") or "").strip()
        if chat_id and (text == "/start" or text.startswith("/start ") or text in ("/menu", "/help")):
            _send(chat_id, "Willkommen bei ULTIMA Central. Wähle einen Bereich:", _menu())
        elif chat_id:
            _send(chat_id, "Bitte nutze die Menü-Buttons.", _menu())
    elif callback:
        try:
            _api("answerCallbackQuery", {"callback_query_id": callback.get("id", "")})
        except Exception:
            pass
        chat_id = (callback.get("message") or {}).get("chat", {}).get("id")
        data = callback.get("data", "")
        if not chat_id:
            return jsonify(ok=True)
        if data == "sites":
            rows = [[{"text": n, "url": u}] for n,d,u in SITES]
            rows.append([{"text": "⬅ Hauptmenü", "callback_data": "home"}])
            _send(chat_id, "WEBSITES & PROGRAMME\n\n" + "\n".join("• " + n + " — " + d for n,d,u in SITES), {"inline_keyboard": rows})
        elif data == "shops":
            rows = [[{"text": n + " · Link folgt", "callback_data": "shop_pending"}] for n,d in SHOPS]
            rows += [[{"text": "BullRun Apparel ↗", "url": "https://bullrun-apparel.onrender.com/"}], [{"text": "⬅ Hauptmenü", "callback_data": "home"}]]
            _send(chat_id, "WEBSHOPS\n\nLyca-, Rothshild- und Parfum-Zieladressen werden nach Verifikation ergänzt. BullRun ist direkt erreichbar.", {"inline_keyboard": rows})
        elif data == "premium":
            _send(chat_id, "PREMIUM & KOMBI-ABOS\n\nEinzelabos, Kombi-Pakete, Laufzeiten und Vertragsdetails sind vorgesehen. Zahlung und Vertragsbuchung sind noch nicht aktiviert.", _menu())
        elif data == "profile":
            _send(chat_id, "PROFIL & VERWALTUNG\n\nZentrale Konto- und Profilverwaltung:", {"inline_keyboard": [[{"text": "ULTIMA Konto öffnen ↗", "url": "https://ultima-unify-45ne.onrender.com/"}], [{"text": "⬅ Hauptmenü", "callback_data": "home"}]]})
        elif data == "donate":
            _send(chat_id, "SPENDEN & FIRMENSTART\n\nZahlungen werden erst nach Prüfung der Wallet, Empfängerinformationen und transparenten 20-%-Aufteilung freigeschaltet. Der Bot nimmt derzeit keine Spenden an.", _menu())
        elif data == "updates":
            _send(chat_id, "UPDATE MATRIX\n\nProjektstatus, Versionshistorie, KI-Vorschläge und Freigabestatus:", {"inline_keyboard": [[{"text": "ULTIMA Update Matrix ↗", "url": "https://ultima-unify-45ne.onrender.com/update-matrix/"}], [{"text": "⬅ Hauptmenü", "callback_data": "home"}]]})
        elif data == "home":
            _send(chat_id, "ULTIMA Central · Hauptmenü", _menu())
        elif data == "shop_pending":
            _send(chat_id, "Der Shop-Link wird ergänzt, sobald die offizielle Zieladresse geprüft wurde.", _menu())
    return jsonify(ok=True)

@bp.get("/telegram/status")
def telegram_status():
    configured = bool(_token() and os.environ.get("TELEGRAM_WEBHOOK_SECRET") and os.environ.get("TELEGRAM_PUBLIC_URL"))
    return jsonify(bot="ULTIMA Central", username="Ultima_Unify_Bot", token_configured=bool(_token()), webhook_configured=_WEBHOOK_REGISTERED, ready=configured and _WEBHOOK_REGISTERED), 200
