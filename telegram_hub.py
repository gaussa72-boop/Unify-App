"""ULTIMA Telegram hub: navigation and role-gated links; sensitive operations remain in authenticated admin web pages."""
import json, os, urllib.request, hmac
from flask import Blueprint, request, jsonify

bp = Blueprint("ultima_telegram", __name__)
_WEBHOOK_REGISTERED = False
API_BASE = os.environ.get("ULTIMA_MEMBERSHIP_API_URL", "https://ultima-membership-api.onrender.com").rstrip("/")
PORTAL = os.environ.get("ULTIMA_PORTAL_URL", "https://ultima-unify-45ne.onrender.com/")
APPLY = API_BASE + "/membership-apply"
NETWORK = os.environ.get("ULTIMA_NETWORK_URL", "https://ultima-unify-45ne.onrender.com/network/")

SITES = [
 ("Astralis Omega", "https://astralis-omega.onrender.com/"),
 ("NovaTube", "https://novatube-a10l.onrender.com/"),
 ("Ate Rea Vermächtnis", "https://ate-rea-vermachtnis.onrender.com/"),
 ("Quantum.AI", "https://quantum-ai-zeah.onrender.com/"),
 ("KI Game Mod", "https://ki-game-mod.onrender.com/"),
 ("Note-KI", "https://note-ki.onrender.com/"),
 ("iPad App IONOS-7", "https://ipad-app-ionos-7.onrender.com/"),
 ("Galactic AI V3", "https://galactic-ai-v3.onrender.com/"),
 ("Quantum Super Intelligence", "https://quantum-super-intelligence.onrender.com/"),
 ("IONOS-8", "https://ionos-8.onrender.com/"),
 ("Quantum KI CAT Chat", "https://quantum-ki-cat-chat.onrender.com/"),
 ("AI Quantumlight", "https://ai-quantumlight.onrender.com/"),
 ("Quantenformel", "https://quantenformel.onrender.com/"),
 ("Quantum Singularity", "https://quantum-singularity.onrender.com/"),
 ("IONOS AI", "https://ionos-ai.onrender.com/"),
 ("Rea Signature", "https://rea-signature.onrender.com/"),
 ("Quantum AI-One", "https://quantum-ai-renewed.onrender.com/"),
 ("Quantum KI Ultra Pro V2 (Renewed)", "https://quantum-ki-ultra-pro-v2-renewed.onrender.com/"),
 ("Quantum Mirror Wonderland", "https://quantum-mirror-wonderland.onrender.com/"),
 ("IONOS-KI", "https://ionos-ki.onrender.com/"),
 ("IONOS-7", "https://ionos-7.onrender.com/"),
 ("UltraKI.AI", "https://ultraki-ai.onrender.com/"),
 ("Ultra KI V2", "https://ultra-ki-v2.onrender.com/"),
 ("Quantum KI Ultra Pro V2", "https://quantum-ki-ultra-pro-v2.onrender.com/"),
 ("QuantumAI Chat", "https://quantumai-chat.onrender.com/"),
 ("Trinity Trading", "https://trinity-trading-k03l.onrender.com/"),
 ("LICHTKRIEGER Cloud Gaming", "https://lichtkrieger-cloud-gaming.onrender.com/"),
 ("NeuroForge Systems", "https://neuroforge-2035.onrender.com/"),
 ("Aurelis Creative AI Studio", "https://aurelis-creative-ai-studio.onrender.com/"),
 ("Ate Rea CharacterVerse", "https://ate-rea-characterverse.onrender.com/"),
 ("IONOS-7 MasterCat Portal", "https://ionos-7-gauss-portal.onrender.com/"),
 ("NeuroForge Systems", "https://neuroforge-gaussa-2035.onrender.com/"),
 ("Galactic AI", "https://galactic-ai-v3-app.onrender.com/"),
]
SHOPS = [
 ("DropShift Store", "https://dropshift-store.onrender.com/"),
 ("BullRun Apparel", "https://bullrun-apparel.onrender.com/"),
 ("Aktiv Lyca", "https://aktiv-lyca-rgds.onrender.com/"),
 ("Sneaker Store", "https://sneaker-store-bow5.onrender.com/"),
 ("Webshop Parfum", "https://webshop-parfum-90dl.onrender.com/"),
 ("Aktiv Lyca", "https://aktiv-lyca-rnmc.onrender.com/"),
 ("Rothshild · Royal Palace", "https://royal-palace-4r57.onrender.com/"),
 ("Rothshild · Business Real Estate", "https://business-real-estate-membership-wswk.onrender.com/"),
]
SITE_ADMIN_LINKS = [
 ("Astralis Omega", "astralis-omega"),
 ("NovaTube", "novatube"),
 ("Ate Rea Vermächtnis", "ate-rea-vermachtnis"),
 ("DropShift Store", "dropshift-store"),
 ("Quantum.AI", "quantum-ai"),
 ("KI Game Mod", "ki-game-mod"),
 ("Note-KI", "note-ki"),
 ("iPad App IONOS-7", "ipad-app-ionos-7"),
 ("Galactic AI V3", "galactic-ai-v3"),
 ("Quantum Super Intelligence", "quantum-super-intelligence"),
 ("IONOS-8", "ionos-8"),
 ("Quantum KI CAT Chat", "quantum-ki-cat-chat"),
 ("AI Quantumlight", "ai-quantumlight"),
 ("Quantenformel", "quantenformel"),
 ("Quantum Singularity", "quantum-singularity"),
 ("IONOS AI", "ionos-ai"),
 ("Rea Signature", "rea-signature"),
 ("Quantum AI-One", "quantum-ai-one"),
 ("Quantum KI Ultra Pro V2 (Renewed)", "quantum-ki-ultra-pro-v2-renewed"),
 ("BullRun Apparel", "bullrun-apparel"),
 ("Quantum Mirror Wonderland", "quantum-mirror-wonderland"),
 ("IONOS-KI", "ionos-ki"),
 ("IONOS-7", "ionos-7"),
 ("UltraKI.AI", "ultraki-ai"),
 ("Ultra KI V2", "ultra-ki-v2"),
 ("Quantum KI Ultra Pro V2", "quantum-ki-ultra-pro-v2"),
 ("QuantumAI Chat", "quantumai-chat"),
 ("Trinity Trading", "trinity-trading"),
 ("Aktiv Lyca", "aktiv-lyca-rgds"),
 ("Sneaker Store", "sneaker-store"),
 ("Webshop Parfum", "webshop-parfum"),
 ("Aktiv Lyca", "aktiv-lyca-rnmc"),
 ("Rothshild · Royal Palace", "royal-palace-4r57"),
 ("Rothshild · Business Real Estate", "business-real-estate-membership"),
 ("LICHTKRIEGER Cloud Gaming", "lichtkrieger"),
 ("ULTIMA Central Public Portal", "ultima-central-portal"),
 ("ULTIMA Unify Account Hub", "ultima-unify-portal"),
 ("NeuroForge Systems", "neuroforge"),
 ("Aurelis Creative AI Studio", "aurelis-creative-ai-studio"),
 ("Ate Rea CharacterVerse", "ate-rea-characterverse"),
 ("IONOS-7 MasterCat Portal", "ionos-7-gauss-portal"),
 ("NeuroForge Systems", "neuroforge-gaussa-2035"),
 ("Galactic AI", "galactic-ai-v3-app"),
]
SHOP_ADMIN_LINKS = [
 ("DropShift Store", "dropshift-store"),
 ("BullRun Apparel", "bullrun-apparel"),
 ("Aktiv Lyca", "aktiv-lyca-rgds"),
 ("Sneaker Store", "sneaker-store"),
 ("Webshop Parfum", "webshop-parfum"),
 ("Aktiv Lyca", "aktiv-lyca-rnmc"),
 ("Rothshild · Royal Palace", "royal-palace-4r57"),
 ("Rothshild · Business Real Estate", "business-real-estate-membership"),
]

def _token():
 return os.environ.get("TELEGRAM_BOT_TOKEN","").strip()

def _api(method,payload):
 token=_token()
 if not token: raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt")
 req=urllib.request.Request("https://api.telegram.org/bot"+token+"/"+method,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
 with urllib.request.urlopen(req,timeout=12) as response: return json.loads(response.read().decode())

def _ids(key):
 return {x.strip() for x in os.environ.get(key,"").split(",") if x.strip()}

def _role(user_id):
 value=str(user_id or "")
 if value in _ids("ULTIMA_TELEGRAM_SUPERADMIN_IDS"): return "superadmin"
 if value in _ids("ULTIMA_TELEGRAM_ADMIN_IDS"): return "admin"
 if value in _ids("ULTIMA_TELEGRAM_MENTOR_IDS"): return "mentor"
 return "member"

def _menu(role):
 rows=[
  [{"text":"🧠 KI-Systeme","callback_data":"ais"}],
  [{"text":"🌐 Websites & Programme","callback_data":"sites"}],
  [{"text":"🎮 Games & Game-Engines","callback_data":"games"}],
  [{"text":"🛍 Webshops","callback_data":"shops"}],
  [{"text":"🌌 Aurealis Network · Mini App","web_app":{"url":NETWORK}}],
  [{"text":"♡ Humanitäre Spendenaktion","url":NETWORK.rstrip("/")+"/#donate"}],
  [{"text":"💬 Mentor kontaktieren · Arian_Phenex","url":"https://t.me/Arian_Phenex"}],
  [{"text":"📝 Mitgliedschaft beantragen","url":APPLY}],
  [{"text":"⏱ 1 Tag KI & Programme testen","url":PORTAL}],
  [{"text":"👤 ULTIMA Profil & Konto","url":PORTAL}],
  [{"text":"🔄 Update Matrix","url":PORTAL.rstrip("/")+"/update-matrix/"}],
 ]
 if role in {"mentor","admin","superadmin"}: rows.append([{"text":"🎓 Mentor-Bereich","url":API_BASE+"/admin/mentors"}])
 if role in {"admin","superadmin"}:
  rows.append([{"text":"🛠 Verwaltungszentrale","url":API_BASE+"/admin"}])
  rows.append([{"text":"🧩 Einzelne Websites verwalten","callback_data":"site_admins"}])
  rows.append([{"text":"🛍 Einzelne Webshops verwalten","callback_data":"shop_admins"}])
 if role=="superadmin":
  rows.extend([
   [{"text":"🛡 Cyber Shield","url":API_BASE+"/cyber-shield"}],
   [{"text":"📋 Mitgliedschaftsanträge","url":API_BASE+"/admin/memberships"}],
   [{"text":"🎉 Feiertags-Testtage","url":API_BASE+"/admin/holiday-access"}],
   [{"text":"⭐ Premium-Verwaltung","url":API_BASE+"/admin/premium"}],
  ])
 return {"inline_keyboard":rows}

def _send(chat_id,message,markup=None):
 payload={"chat_id":chat_id,"text":message,"disable_web_page_preview":True}
 if markup: payload["reply_markup"]=markup
 _api("sendMessage",payload)

def _directory(chat_id,title,entries,role):
 rows=[[{"text":name[:55]+" ↗","url":url}] for name,url in entries]
 rows.append([{"text":"⬅ Hauptmenü","callback_data":"home"}])
 _send(chat_id,title+"\n\n"+"\n".join("• "+name for name,url in entries),{"inline_keyboard":rows})

def _register_webhook_once():
 global _WEBHOOK_REGISTERED
 if _WEBHOOK_REGISTERED or not _token(): return
 base=os.environ.get("TELEGRAM_PUBLIC_URL","").strip().rstrip("/")
 secret=os.environ.get("TELEGRAM_WEBHOOK_SECRET","").strip()
 if not base or not secret: return
 try:
  _api("setWebhook",{"url":base+"/telegram/webhook","secret_token":secret,"allowed_updates":["message","callback_query"],"drop_pending_updates":False})
  _WEBHOOK_REGISTERED=True
 except Exception: return

@bp.before_app_request
def register_webhook_on_first_request(): _register_webhook_once()

@bp.post("/telegram/webhook")
def telegram_webhook():
 expected=os.environ.get("TELEGRAM_WEBHOOK_SECRET","").strip()
 supplied=request.headers.get("X-Telegram-Bot-Api-Secret-Token","")
 if not expected or not supplied or not hmac.compare_digest(expected,supplied): return jsonify(ok=False),403
 update=request.get_json(silent=True) or {}
 message=update.get("message") or {}
 callback=update.get("callback_query") or {}
 if message:
  chat_id=(message.get("chat") or {}).get("id")
  user_id=(message.get("from") or {}).get("id")
  text=(message.get("text") or "").strip()
  role=_role(user_id)
  if chat_id and (text=="/start" or text.startswith("/start ") or text in ("/menu","/help")):
   _send(chat_id,"Willkommen bei ULTIMA Central. Deine Rolle: "+role+". Wähle einen Bereich:",_menu(role))
  elif chat_id and text=="/id":
   _send(chat_id,"Deine Telegram-ID: "+str(user_id)+"\nNur direkt an den Betreiber senden, wenn du freigeschaltet werden sollst.")
  elif chat_id: _send(chat_id,"Bitte nutze die Menü-Buttons oder /menu.",_menu(role))
 elif callback:
  user_id=(callback.get("from") or {}).get("id")
  role=_role(user_id)
  try: _api("answerCallbackQuery",{"callback_query_id":callback.get("id","")})
  except Exception: pass
  chat_id=(callback.get("message") or {}).get("chat",{}).get("id")
  data=callback.get("data","")
  if not chat_id: return jsonify(ok=True)
  if data=="ais":
   _directory(chat_id,"KI-SYSTEME",[("Aurealis OMNIA","https://aurealis-omnia.onrender.com/"),("Aurealis Creative AI","https://aurelis-creative-ai-studio.onrender.com/"),("Quantum.AI","https://quantum-ai-zeah.onrender.com/"),("Quantum KI Ultra Pro","https://quantum-ki-ultra-pro-v2.onrender.com/"),("NeuroForge","https://neuroforge-2035.onrender.com/"),("IONOS-KI","https://ionos-ki.onrender.com/"),("Ate Rea CharacterVerse","https://ate-rea-characterverse.onrender.com/")],role)
  elif data=="sites": _directory(chat_id,"WEBSITES & PROGRAMME",SITES,role)
  elif data=="games":
   _directory(chat_id,"GAMES & GAME-ENGINES",[("Quantum Mirror Wonderland","https://quantum-mirror-wonderland.onrender.com/"),("LICHTKRIEGER Cloud Gaming","https://lichtkrieger-cloud-gaming.onrender.com/"),("KI Game Mod","https://ki-game-mod.onrender.com/"),("Astralis Omega","https://astralis-omega.onrender.com/")],role)
  elif data=="shops": _directory(chat_id,"WEBSHOPS · ZENTRALE SHOP-ÜBERSICHT",SHOPS,role)
  elif data=="site_admins" and role in {"admin","superadmin"}:
   entries=[(name,API_BASE+"/admin/site/"+slug) for name,slug in SITE_ADMIN_LINKS]
   _directory(chat_id,"WEBSITE-VERWALTUNG · ADMIN LOGIN ERFORDERLICH",entries,role)
  elif data=="shop_admins" and role in {"admin","superadmin"}:
   entries=[(name,API_BASE+"/admin/site/"+slug) for name,slug in SHOP_ADMIN_LINKS]
   _directory(chat_id,"WEBSHOP-VERWALTUNG · ADMIN LOGIN ERFORDERLICH",entries,role)
  elif data=="home": _send(chat_id,"ULTIMA Central · Hauptmenü",_menu(role))
 return jsonify(ok=True)

@bp.get("/telegram/status")
def telegram_status():
 configured=bool(_token() and os.environ.get("TELEGRAM_WEBHOOK_SECRET") and os.environ.get("TELEGRAM_PUBLIC_URL"))
 return jsonify(bot="ULTIMA Central",username="Ultima_Unify_Bot",token_configured=bool(_token()),webhook_configured=_WEBHOOK_REGISTERED,ready=configured and _WEBHOOK_REGISTERED,configured_roles={"superadmin":bool(_ids("ULTIMA_TELEGRAM_SUPERADMIN_IDS")),"admin":bool(_ids("ULTIMA_TELEGRAM_ADMIN_IDS")),"mentor":bool(_ids("ULTIMA_TELEGRAM_MENTOR_IDS"))},membership_application=APPLY,network=NETWORK,mentor_contact="https://t.me/Arian_Phenex"),200
