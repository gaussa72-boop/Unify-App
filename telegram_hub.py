"""ULTIMA Telegram hub: navigation and role-gated links; sensitive operations remain in authenticated admin web pages."""
import json, os, urllib.request, hmac, html
from flask import Blueprint, request, jsonify

bp = Blueprint("ultima_telegram", __name__)
_WEBHOOK_REGISTERED = False
_WEBHOOK_ERROR = ""
API_BASE = os.environ.get("ULTIMA_MEMBERSHIP_API_URL", "https://ultima-membership-api.onrender.com").rstrip("/")
PORTAL = os.environ.get("ULTIMA_PORTAL_URL", "https://ultima-unify-45ne.onrender.com/")
APPLY = API_BASE + "/membership-apply"
NETWORK = os.environ.get("ULTIMA_NETWORK_URL", "https://aurealis-network.onrender.com/")
SUPPORT_URL = os.environ.get("ULTIMA_SUPPORT_URL", "https://t.me/Ari_phenex")
SUPPORT_NAME = os.environ.get("ULTIMA_SUPPORT_NAME", "Arian · @Ari_phenex")

SITES = [
 ("Astralis Game Engine","https://astralis-game-engine.onrender.com/"),
 ("Aurealis OMNIA","https://aurealis-omnia.onrender.com/"),
 ("Aurealis OMNIA Alliance","https://aurealis-omnia-alliance-ai.onrender.com/"),
 ("Aurealis Infinity","https://aurealis-infinity.onrender.com/"),
 ("Aurealis Shopping AI","https://aurealis-shopping-ai.onrender.com/"),
 ("Aurealis Creative AI Studio","https://aurelis-creative-ai-studio.onrender.com/"),
 ("Aurealis Cyber Shield","https://aurealis-cyber-shield.onrender.com/"),
 ("Aurelis Investment","https://aurelis-investment.onrender.com/"),
 ("Ate Rea Exchange","https://ate-rea-exchange.onrender.com/"),
 ("Ate Rea Vermächtnis","https://ate-rea-vermachtnis.onrender.com/"),
 ("Ate Rea CharacterVerse","https://ate-rea-characterverse.onrender.com/"),
 ("Meta Wissenschaftsforum","https://meta-wissenschaftsforum.onrender.com/"),
 ("NovaTube","https://novatube-a10l.onrender.com/"),
 ("Quantum AI","https://quantum-ai-zeah.onrender.com/"),
 ("Quantum AI One","https://quantum-ai-renewed.onrender.com/"),
 ("Quantum AI Ultra Pro V2","https://quantum-ki-ultra-pro-v2.onrender.com/"),
 ("Quantum AI Ultra Pro V2 Renewed","https://quantum-ki-ultra-pro-v2-renewed.onrender.com/"),
 ("Quantum AI Chat","https://quantumai-chat.onrender.com/"),
 ("Quantum Mirror Wonderland","https://quantum-mirror-wonderland.onrender.com/"),
 ("Quantum Mirror Dark Wonderland","https://quantum-mirror-dark-wonderland-ejc3.onrender.com/"),
 ("Quantum Super Intelligence","https://quantum-super-intelligence.onrender.com/"),
 ("Quantum Singularity","https://quantum-singularity.onrender.com/"),
 ("Quantum KI CAT Chat","https://quantum-ki-cat-chat.onrender.com/"),
 ("AI Quantumlight","https://ai-quantumlight.onrender.com/"),
 ("Quantenformel","https://quantenformel.onrender.com/"),
 ("IONOS AI","https://ionos-ai.onrender.com/"),
 ("IONOS-KI","https://ionos-ki.onrender.com/"),
 ("IONOS-7","https://ionos-7.onrender.com/"),
 ("IONOS-7 MasterCat Portal","https://ionos-7-gauss-portal.onrender.com/"),
 ("IONOS-8","https://ionos-8.onrender.com/"),
 ("NeuroForge 2035","https://neuroforge-2035.onrender.com/"),
 ("NeuroForge Gauss 2035","https://neuroforge-gaussa-2035.onrender.com/"),
 ("NeuroForge Systems 2035","https://neuroforge-systems-2035.onrender.com/"),
 ("Lichtkrieger Dark Mirror Realms","https://lichtkrieger-dark-mirror-realms.onrender.com/"),
 ("Lichtkrieger Cloud Gaming","https://lichtkrieger-cloud-gaming.onrender.com/"),
 ("The Lord Agent Network","https://the-lord-agent-network.onrender.com/"),
 ("Rea Signature","https://rea-signature.onrender.com/"),
 ("Technologisierte Einheit","https://technologisierte-einheit.onrender.com/"),
 ("Zenmachanik Rea","https://zenmachanik-rea.onrender.com/"),
 ("ULTIMA Central","https://ultima-central-45ne.onrender.com/"),
 ("ULTIMA Unify Account Hub","https://ultima-unify-45ne.onrender.com/"),
 ("ULTIMA OS Workspace","https://ultima-os-workspace.onrender.com/"),
 ("ULTIMA Sun Singularity","https://ultima-sun-singularity.onrender.com/"),
 ("ULTIMA Media Impact Hub","https://ultima-media-impact-hub.onrender.com/"),
 ("ULTIMA Membership API","https://ultima-membership-api.onrender.com/"),
 ("Aurealis Network","https://aurealis-network.onrender.com/"),
]

SHOPS = [
 ("DropShift Store","https://dropshift-store.onrender.com/"),
 ("Aktiv Lyca","https://aktiv-lyca-rnmc.onrender.com/"),
 ("Webshop Parfum · ATG","https://webshop-parfum-90dl.onrender.com/"),
 ("BullRun Apparel","https://bullrun-apparel.onrender.com/"),
 ("Sneaker Store","https://sneaker-store-bow5.onrender.com/"),
 ("Rothshild · Royal Palace","https://royal-palace-4r57.onrender.com/"),
 ("Rothshild · Business Real Estate","https://business-real-estate-membership-wswk.onrender.com/"),
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
 with urllib.request.urlopen(req,timeout=12) as response:
  result=json.loads(response.read().decode())
  if not result.get("ok"): raise RuntimeError(result.get("description","Telegram API error"))
  return result

def _ids(key):
 return {x.strip() for x in os.environ.get(key,"").split(",") if x.strip()}

def _role(user_id, username=None):
 value=str(user_id or "")
 usernames={x.strip().lstrip("@").casefold() for x in os.environ.get("ULTIMA_TELEGRAM_SUPERADMIN_USERNAMES","").split(",") if x.strip()}
 if value in _ids("ULTIMA_TELEGRAM_SUPERADMIN_IDS") or (username or "").lstrip("@").casefold() in usernames: return "superadmin"
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
  [{"text":"🛟 Support kontaktieren · Arian","url":SUPPORT_URL}],
  [{"text":"🎓 Mentor kontaktieren","url":SUPPORT_URL}],
  [{"text":"📝 Zentralen Website-Zugang beantragen","url":PORTAL.rstrip("/")+"/register"}],
  [{"text":"💳 Mitgliedschaft beantragen","url":APPLY}],
  [{"text":"⏱ 1 Tag KI & Programme testen","url":PORTAL}],
  [{"text":"👤 ULTIMA Profil & Konto","url":PORTAL}],
  [{"text":"🔄 Update Matrix","url":PORTAL.rstrip("/")+"/update-matrix/"}],
 ]
 if role in {"mentor","admin","superadmin"}: rows.append([{"text":"🎓 Mentor-Bereich","url":API_BASE+"/admin/mentors"}])
 if role in {"admin","superadmin"}:
  rows.append([{"text":"🛠 Verwaltungszentrale","url":API_BASE+"/admin"}])
  rows.append([{"text":"🔐 Zugangsanträge freigeben","url":PORTAL.rstrip("/")+"/admin/applications/"}])
  rows.append([{"text":"🧩 Einzelne Websites verwalten","callback_data":"site_admins"}])
  rows.append([{"text":"🛍 Einzelne Webshops verwalten","callback_data":"shop_admins"}])
 if role=="superadmin":
  rows.append([{"text":"🧾 Commerce · Bestellungen & Rechnungen","url":PORTAL.rstrip("/")+"/admin/commerce/"}])
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
 rows=[]
 lines=[]
 for entry in entries:
  if len(entry)==3:
   name,description,url=entry
  else:
   name,url=entry
   description="Website öffnen"
  safe_name=html.escape(str(name))
  safe_desc=html.escape(str(description))
  safe_url=html.escape(str(url),quote=True)
  rows.append([{"text":str(name)[:48]+" ↗","url":url}])
  lines.append('• <a href="'+safe_url+'">'+safe_name+'</a> — '+safe_desc)
 rows.append([{"text":"⬅ Hauptmenü","callback_data":"home"}])
 _api("sendMessage",{"chat_id":chat_id,"text":title+"\n\n"+"\n".join(lines),"parse_mode":"HTML","disable_web_page_preview":True,"reply_markup":{"inline_keyboard":rows}})

def _register_webhook_once():
 global _WEBHOOK_REGISTERED
 if _WEBHOOK_REGISTERED: return
 if not _token():
  print("ULTIMA Telegram setup blocked: TELEGRAM_BOT_TOKEN is missing")
  return
 base=os.environ.get("TELEGRAM_PUBLIC_URL","").strip().rstrip("/")
 secret=os.environ.get("TELEGRAM_WEBHOOK_SECRET","").strip()
 if not base or not secret:
  print("ULTIMA Telegram setup incomplete: TELEGRAM_PUBLIC_URL="+str(bool(base))+", TELEGRAM_WEBHOOK_SECRET="+str(bool(secret)))
  return
 try:
  _api("setWebhook",{"url":base+"/telegram/webhook","secret_token":secret,"allowed_updates":["message","callback_query"],"drop_pending_updates":False})
  _api("setMyDescription",{"description":"ULTIMA Central verbindet deine KI-Systeme, digitalen Projekte, Websites, Game-Engines und Webshops. Entdecke Aurealis, Quantum AI, NeuroForge, IONOS-KI, Ate Rea und weitere Anwendungen. Nutze Testzugänge, beantrage Mitgliedschaft, kontaktiere Mentoren und verwalte dein Profil. Shops bieten Produktübersichten und führen zum jeweiligen Checkout. Humanitäre Hilfe und Community findest du ebenfalls im Menü."})
  _api("setMyShortDescription",{"short_description":"ULTIMA: KI-Systeme, Websites, Games, Shops, Community, Testzugänge und Mitgliedschaft."})
  _api("setMyCommands",{"commands":[
   {"command":"start","description":"ULTIMA Hauptmenü öffnen"},
   {"command":"menu","description":"Hauptmenü anzeigen"},
   {"command":"ais","description":"KI-Systeme anzeigen"},
   {"command":"sites","description":"Websites und Programme"},
   {"command":"shops","description":"Webshops öffnen"},
   {"command":"games","description":"Games und Engines"},
   {"command":"register","description":"Zentralen Zugang beantragen"},
   {"command":"mentor","description":"Mentor kontaktieren"},
   {"command":"support","description":"ULTIMA Support kontaktieren"},
   {"command":"donate","description":"Humanitäre Hilfe"},
   {"command":"id","description":"Eigene Telegram-ID anzeigen"},
   {"command":"status","description":"Bot-Status anzeigen"},\n    {"command":"commerce","description":"Bestellungen und Rechnungen · Superadmin"},
    {"command":"publicbot","description":"Status des Besucherbots · Superadmin"},
   {"command":"help","description":"Hilfe anzeigen"}
  ]})
  _api("setChatMenuButton",{"menu_button":{"type":"web_app","text":"Aurealis Network","web_app":{"url":NETWORK}}})
  _WEBHOOK_REGISTERED=True
  print("ULTIMA Telegram setup successful: webhook, bot description, commands and Mini App menu configured")
 except Exception as exc:
  _WEBHOOK_ERROR=type(exc).__name__+": "+str(exc)[:240]
  print("ULTIMA Telegram setup failed: "+_WEBHOOK_ERROR)
  return

@bp.before_app_request
def register_webhook_on_first_request():
 _register_webhook_once()
 _register_public_webhook_once()

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
  role=_role(user_id,(message.get("from") or {}).get("username"))
  command=(text.split()[0].split("@")[0].lower() if text.startswith("/") else "")
  if chat_id and command in ("/start","/menu","/help"):
   _send(chat_id,"✨ WILLKOMMEN BEI ULTIMA CENTRAL ✨\n\nDein Zugang zu einem vernetzten Universum aus künstlicher Intelligenz, digitalen Diensten, kreativen Welten und Handel.\n\n🧠 KI-LABORE\nAurealis OMNIA · Creative AI Studio · Quantum AI Ultra Pro · Quantum AI One · NeuroForge · IONOS-KI · AI Quantumlight · Ate Rea CharacterVerse und weitere KI-Projekte.\n\n🌐 WEBSITES & PROGRAMME\nEntdecke unsere Plattformen, Forschungsprojekte, digitalen Werkzeuge und das Aurealis Network.\n\n🎮 GAMES & GAME-ENGINES\nInteraktive Spielwelten, Game-Projekte und Entwicklungsumgebungen.\n\n🛍 WEBSHOPS\nLyca · ATG Parfum · BullRun Apparel · Sneaker · DropShift und weitere Shops. Produktkataloge und Bestellungen werden im jeweiligen Shop abgewickelt.\n\n⭐ MITGLIEDSCHAFT & TESTZUGANG\nBeantrage deinen zentralen Zugang. Testmöglichkeiten und Freischaltungen richten sich nach deiner Berechtigung.\n\n💬 COMMUNITY & MENTOREN\nEntdecke das Netzwerk, kontaktiere Mentoren und finde die humanitäre Spendeninitiative.\n\nDeine erkannte Rolle: "+role+". Wähle jetzt einen Bereich:",_menu(role))
  elif chat_id and command=="/id":
   _send(chat_id,"Deine Telegram-ID: "+str(user_id)+"\nSende diese Nummer nur direkt an den Superadministrator, wenn du eine Rolle beantragst.")
  elif chat_id and command=="/ais":
   _directory(chat_id,"KI-SYSTEME",[
    ("Aurealis OMNIA","Kreative KI und zentraler Assistent","https://aurealis-omnia.onrender.com/"),
    ("Aurealis Creative AI Studio","Kreativwerkzeuge und Content-Studio","https://aurelis-creative-ai-studio.onrender.com/"),
    ("Quantum AI Ultra Pro","KI-Plattform und Werkzeuge","https://quantum-ki-ultra-pro-v2.onrender.com/"),
    ("Quantum AI One","KI-Assistent und Chat","https://quantum-ai-renewed.onrender.com/"),
    ("NeuroForge","Innovations- und KI-Systeme","https://neuroforge-2035.onrender.com/"),
    ("IONOS-KI","KI-Plattform","https://ionos-ki.onrender.com/"),
    ("AI Quantumlight","Quantumlight-Projekt","https://ai-quantumlight.onrender.com/"),
    ("Aurealis Shopping AI","Shopping-Assistent","https://aurealis-shopping-ai.onrender.com/"),
    ("Ate Rea CharacterVerse","Charakter-KI und Avatar-Studio","https://ate-rea-characterverse.onrender.com/")
   ],role)
  elif chat_id and command=="/games":
   _directory(chat_id,"GAMES & GAME-ENGINES",[("Astralis Game Engine","Game-Engine und Spielprojekte","https://astralis-game-engine.onrender.com/"),("Quantum Mirror Wonderland","Interaktive Spielwelt","https://quantum-mirror-wonderland.onrender.com/"),("Lichtkrieger Cloud Gaming","Cloud-Gaming-Projekt","https://lichtkrieger-cloud-gaming.onrender.com/"),("The Lord Agent Network","Agenten- und Spielnetzwerk","https://the-lord-agent-network.onrender.com/")],role)
  elif chat_id and command=="/sites":
   _directory(chat_id,"WEBSITES & PROGRAMME",SITES,role)
  elif chat_id and command=="/shops":
   _directory(chat_id,"WEBSHOPS",[
    ("DropShift Store","Produkte und Dropshipping-Shop","https://dropshift-store.onrender.com/"),
    ("Aktiv Lyca","SIM- und Mobilfunkprodukte","https://aktiv-lyca-rnmc.onrender.com/"),
    ("ATG Parfum","Parfumkollektion","https://webshop-parfum-90dl.onrender.com/"),
    ("BullRun Apparel","Streetwear und Apparel","https://bullrun-apparel.onrender.com/"),
    ("Sneaker Store","Sneaker-Kollektion","https://sneaker-store-bow5.onrender.com/"),
    ("Rothshild Royal Palace","Royal Shop und Mitgliedschaft","https://royal-palace-4r57.onrender.com/"),
    ("Rothshild Business Real Estate","Business- und Immobilienportal","https://business-real-estate-membership-wswk.onrender.com/")
   ],role)
  elif chat_id and command=="/games":
   _directory(chat_id,"GAMES & GAME-ENGINES",[
    ("Astralis Game Engine","Game-Engine und Spielprojekte","https://astralis-game-engine.onrender.com/"),
    ("Quantum Mirror Wonderland","Spielwelt und interaktive Erlebnisse","https://quantum-mirror-wonderland.onrender.com/"),
    ("Lichtkrieger Cloud Gaming","Cloud-Gaming-Projekt","https://lichtkrieger-cloud-gaming.onrender.com/"),
    ("The Lord Agent Network","Agenten- und Spielnetzwerk","https://the-lord-agent-network.onrender.com/")
   ],role)
  elif chat_id and command=="/register":
   _send(chat_id,"Zentralen Website-Zugang beantragen:",{"inline_keyboard":[[{"text":"Zugang beantragen ↗","url":PORTAL.rstrip("/")+"/register"}],[{"text":"⬅ Hauptmenü","callback_data":"home"}]]})
  elif chat_id and command in ("/mentor","/support"):
   _send(chat_id,"🛟 ULTIMA SUPPORT\n\nDein Supportkontakt: "+SUPPORT_NAME+". Tippe auf den Button, um den Telegram-Chat zu öffnen. Teile dort keine Passwörter, Bot-Tokens oder privaten Wallet-Schlüssel.",{"inline_keyboard":[[{"text":"Support-Chat öffnen ↗","url":SUPPORT_URL}],[{"text":"⬅ Hauptmenü","callback_data":"home"}]]})
  elif chat_id and command=="/donate":
   _send(chat_id,"Humanitäre Spendenaktion: Informationen und Kontakt. Eine Zahlungsannahme wird erst aktiviert, wenn Empfänger und Zahlungsweg verifiziert sind.",{"inline_keyboard":[[{"text":"Spendenaktion ansehen ↗","url":NETWORK.rstrip("/")+"/#donate"}]]})
  elif chat_id and command=="/status":
   _send(chat_id,"ULTIMA Bot\nRolle: "+role+"\nMini App: "+NETWORK+"\nWebhook: "+("aktiv" if _WEBHOOK_REGISTERED else "noch nicht bestätigt"))
  elif chat_id and command=="/commerce" and role=="superadmin":
   _send(chat_id,"🧾 ULTIMA Commerce Control\nBestellungen, Checkout-Statistik und Rechnungen zentral verwalten:",{"inline_keyboard":[[{"text":"Commerce & Rechnungen öffnen ↗","url":PORTAL.rstrip("/")+"/admin/commerce/"}],[{"text":"⬅ Hauptmenü","callback_data":"home"}]]})
  elif chat_id and command=="/publicbot" and role in {"admin","superadmin"}:
   try:
    me=_public_api("getMe",{}).get("result",{})
    wh=_public_api("getWebhookInfo",{}).get("result",{})
    _send(chat_id,"Besucherbot: @"+str(me.get("username","unbekannt"))+"\nWebhook: "+str(wh.get("url","nicht gesetzt"))+"\nWartende Updates: "+str(wh.get("pending_update_count",0)))
   except Exception as exc:
    _send(chat_id,"Besucherbot noch nicht betriebsbereit: "+str(exc)[:180])
  elif chat_id:
   _send(chat_id,"Nutze /menu, /ais, /sites, /shops, /games, /register, /mentor, /support, /donate, /id oder /status.",_menu(role))
 elif callback:
  user_id=(callback.get("from") or {}).get("id")
  role=_role(user_id,(callback.get("from") or {}).get("username"))
  try: _api("answerCallbackQuery",{"callback_query_id":callback.get("id","")})
  except Exception: pass
  chat_id=(callback.get("message") or {}).get("chat",{}).get("id")
  data=callback.get("data","")
  if not chat_id: return jsonify(ok=True)
  if data=="ais":
   _directory(chat_id,"KI-SYSTEME · BESCHREIBUNGEN",[
    ("Aurealis OMNIA","Kreative KI und zentraler Assistent","https://aurealis-omnia.onrender.com/"),
    ("Aurealis Creative AI Studio","Kreativwerkzeuge und Content-Studio","https://aurelis-creative-ai-studio.onrender.com/"),
    ("Quantum AI Ultra Pro","KI-Plattform und Werkzeuge","https://quantum-ki-ultra-pro-v2.onrender.com/"),
    ("Quantum AI One","KI-Assistent und Chat","https://quantum-ai-renewed.onrender.com/"),
    ("NeuroForge","Innovations- und KI-Systeme","https://neuroforge-2035.onrender.com/"),
    ("IONOS-KI","KI-Plattform","https://ionos-ki.onrender.com/"),
    ("AI Quantumlight","Quantumlight-Projekt","https://ai-quantumlight.onrender.com/"),
    ("Aurealis Shopping AI","Shopping-Assistent","https://aurealis-shopping-ai.onrender.com/"),
    ("Ate Rea CharacterVerse","Charakter-KI und Avatar-Studio","https://ate-rea-characterverse.onrender.com/")
   ],role)
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
  elif data=="support":
   _send(chat_id,"🛟 ULTIMA SUPPORT\n\nDirekter Kontakt: "+SUPPORT_NAME+". Öffne den Chat über den Button. Bitte sende niemals Passwörter, Bot-Tokens oder private Wallet-Schlüssel.",{"inline_keyboard":[[{"text":"Support-Chat öffnen ↗","url":SUPPORT_URL}],[{"text":"⬅ Hauptmenü","callback_data":"home"}]]})
  elif data=="home": _send(chat_id,"ULTIMA Central · Hauptmenü",_menu(role))
 return jsonify(ok=True)



# Separate public-facing bot. It deliberately has no role lookup and no admin callbacks.
_PUBLIC_BOT_REGISTERED = False
_PUBLIC_BOT_ERROR = ""
PUBLIC_SUPPORT_URL = os.environ.get("ULTIMA_PUBLIC_SUPPORT_URL", "https://t.me/Ari_phenex")
PUBLIC_BOT_TOKEN_ENV = "ULTIMA_PUBLIC_BOT_TOKEN"
PUBLIC_BOT_SECRET_ENV = "ULTIMA_PUBLIC_BOT_WEBHOOK_SECRET"

def _public_token():
 return os.environ.get(PUBLIC_BOT_TOKEN_ENV, "").strip()

def _public_api(method, payload):
 token = _public_token()
 if not token: raise RuntimeError(PUBLIC_BOT_TOKEN_ENV + " fehlt")
 req = urllib.request.Request(
  "https://api.telegram.org/bot" + token + "/" + method,
  data=json.dumps(payload).encode(),
  headers={"Content-Type":"application/json"},
  method="POST"
 )
 with urllib.request.urlopen(req, timeout=12) as response:
  result = json.loads(response.read().decode())
  if not result.get("ok"): raise RuntimeError(result.get("description", "Telegram API error"))
  return result

def _public_send(chat_id, message, markup=None):
 payload={"chat_id":chat_id,"text":message,"disable_web_page_preview":True}
 if markup: payload["reply_markup"]=markup
 _public_api("sendMessage",payload)

def _public_home_markup():
 return {"inline_keyboard":[
  [{"text":"🧠 KI-Systeme","callback_data":"pub_ais"},{"text":"🌐 Websites","callback_data":"pub_sites"}],
  [{"text":"🎮 Games & Engines","callback_data":"pub_games"},{"text":"🛍 Webshops","callback_data":"pub_shops"}],
  [{"text":"🚀 Aurealis Network · Mini App","web_app":{"url":NETWORK}}],
  [{"text":"📝 Zugang beantragen","url":PORTAL.rstrip("/")+"/register"}],
  [{"text":"⭐ Mitgliedschaft & Testzugang","url":APPLY}],
  [{"text":"♡ Humanitäre Spendenaktion","url":NETWORK.rstrip("/")+"/#donate"}],
  [{"text":"🛟 Support · Arian Phenex","url":PUBLIC_SUPPORT_URL}],
 ]}

def _public_directory(chat_id, title, entries):
 rows=[]
 lines=[]
 for entry in entries:
  if len(entry)==3:
   name,description,url=entry
  else:
   name,url=entry
   description="Website öffnen"
  safe_name=html.escape(str(name))
  safe_desc=html.escape(str(description))
  safe_url=html.escape(str(url),quote=True)
  rows.append([{"text":str(name)[:48]+" ↗","url":url}])
  lines.append('• <a href="'+safe_url+'">'+safe_name+'</a> — '+safe_desc)
 rows.append([{"text":"⬅ Hauptmenü","callback_data":"pub_home"}])
 _public_api("sendMessage",{"chat_id":chat_id,"text":title+"\n\n"+"\n".join(lines),"parse_mode":"HTML","disable_web_page_preview":True,"reply_markup":{"inline_keyboard":rows}})

def _register_public_webhook_once():
 global _PUBLIC_BOT_REGISTERED, _PUBLIC_BOT_ERROR
 if _PUBLIC_BOT_REGISTERED: return
 token=_public_token()
 secret=os.environ.get(PUBLIC_BOT_SECRET_ENV,"").strip()
 base=os.environ.get("TELEGRAM_PUBLIC_URL","").strip().rstrip("/")
 if not token or not secret or not base:
  return
 try:
  _public_api("setWebhook",{"url":base+"/telegram/public-webhook","secret_token":secret,"allowed_updates":["message","callback_query"],"drop_pending_updates":False})
  _public_api("setMyDescription",{"description":"Willkommen bei ULTIMA: Entdecke KI-Systeme, Websites, Games, Webshops und das Aurealis Network. Beantrage einen Zugang, informiere dich über Mitgliedschaften und Testmöglichkeiten oder kontaktiere unseren Support Arian Phenex. Dieser Bot bietet ausschließlich Funktionen für Besucher und Mitglieder."})
  _public_api("setMyShortDescription",{"short_description":"ULTIMA entdecken: KI, Websites, Games, Shops, Community und Support."})
  _public_api("setMyCommands",{"commands":[
   {"command":"start","description":"Willkommen und Hauptmenü"},
   {"command":"menu","description":"Hauptmenü öffnen"},
   {"command":"ais","description":"KI-Systeme entdecken"},
   {"command":"sites","description":"Websites und Programme"},
   {"command":"games","description":"Games und Game-Engines"},
   {"command":"shops","description":"Webshops öffnen"},
   {"command":"register","description":"Zugang beantragen"},
   {"command":"support","description":"Support Arian Phenex"},
   {"command":"donate","description":"Humanitäre Spendenaktion"},
   {"command":"help","description":"Hilfe und Funktionen"}
  ]})
  _public_api("setChatMenuButton",{"menu_button":{"type":"web_app","text":"Aurealis Network","web_app":{"url":NETWORK}}})
  _PUBLIC_BOT_REGISTERED=True
  print("ULTIMA public Telegram bot registered")
 except Exception as exc:
  _PUBLIC_BOT_ERROR=type(exc).__name__+": "+str(exc)[:200]
  print("ULTIMA public Telegram setup failed: "+_PUBLIC_BOT_ERROR)

@bp.post("/telegram/public-webhook")
def telegram_public_webhook():
 expected=os.environ.get(PUBLIC_BOT_SECRET_ENV,"").strip()
 supplied=request.headers.get("X-Telegram-Bot-Api-Secret-Token","")
 if not expected or not supplied or not hmac.compare_digest(expected,supplied):
  return jsonify(ok=False),403
 update=request.get_json(silent=True) or {}
 message=update.get("message") or {}
 callback=update.get("callback_query") or {}
 if message:
  chat_id=(message.get("chat") or {}).get("id")
  text=(message.get("text") or "").strip()
  command=(text.split()[0].split("@")[0].lower() if text.startswith("/") else "")
  if not chat_id: return jsonify(ok=True)
  if command in ("/start","/menu","/help",""):
   _public_send(chat_id,"✨ WILLKOMMEN BEI ULTIMA ✨\n\nEntdecke ein vernetztes Angebot aus künstlicher Intelligenz, digitalen Plattformen, Games und Webshops.\n\n🧠 KI-SYSTEME\nAurealis, Quantum AI, NeuroForge, IONOS-KI, AI Quantumlight und weitere Projekte.\n\n🌐 WEBSITES & PROGRAMME\nDigitale Dienste, kreative Werkzeuge und Forschungsprojekte.\n\n🎮 GAMES\nSpielwelten und Game-Engines.\n\n🛍 WEBSHOPS\nLyca, ATG Parfum, BullRun, Sneaker, DropShift und weitere Shops.\n\n⭐ ZUGANG & TESTS\nZugang beantragen und verfügbare Testmöglichkeiten entdecken.\n\n🛟 SUPPORT\nArian Phenex hilft bei Fragen. Dieser Bot enthält bewusst keine Admin- oder Verwaltungsfunktionen.",_public_home_markup())
  elif command=="/ais":
   _public_directory(chat_id,"🧠 KI-SYSTEME",[
    ("Aurealis OMNIA","Zentrale KI und kreative Assistenz","https://aurealis-omnia.onrender.com/"),
    ("Aurealis Creative AI Studio","Kreativwerkzeuge und Content","https://aurelis-creative-ai-studio.onrender.com/"),
    ("Quantum AI Ultra Pro","KI-Plattform","https://quantum-ki-ultra-pro-v2.onrender.com/"),
    ("Quantum AI One","KI-Assistent","https://quantum-ai-renewed.onrender.com/"),
    ("NeuroForge","KI- und Innovationssysteme","https://neuroforge-2035.onrender.com/"),
    ("IONOS-KI","KI-Plattform","https://ionos-ki.onrender.com/"),
    ("AI Quantumlight","Quantumlight-Projekt","https://ai-quantumlight.onrender.com/"),
    ("Ate Rea CharacterVerse","Charakter-KI","https://ate-rea-characterverse.onrender.com/")
   ])
  elif command=="/sites": _public_directory(chat_id,"🌐 WEBSITES & PROGRAMME",SITES)
  elif command=="/games":
   _public_directory(chat_id,"🎮 GAMES & GAME-ENGINES",[
    ("Astralis Game Engine","Entwicklungsumgebung und Spiele","https://astralis-game-engine.onrender.com/"),
    ("Quantum Mirror Wonderland","Interaktive Spielwelt","https://quantum-mirror-wonderland.onrender.com/"),
    ("Lichtkrieger Cloud Gaming","Cloud Gaming","https://lichtkrieger-cloud-gaming.onrender.com/"),
    ("The Lord Agent Network","Agenten- und Spielnetzwerk","https://the-lord-agent-network.onrender.com/")
   ])
  elif command=="/shops": _public_directory(chat_id,"🛍 WEBSHOPS",SHOPS)
  elif command=="/register":
   _public_send(chat_id,"Zugang zu ULTIMA beantragen:",{"inline_keyboard":[[{"text":"Zugang beantragen ↗","url":PORTAL.rstrip("/")+"/register"}],[{"text":"⬅ Hauptmenü","callback_data":"pub_home"}]]})
  elif command in ("/support","/mentor"):
   _public_send(chat_id,"🛟 SUPPORT · ARIAN PHENEX\n\nÖffne den Telegram-Chat mit Arian Phenex. Bitte sende niemals Passwörter, Bot-Tokens oder private Wallet-Schlüssel.",{"inline_keyboard":[[{"text":"Arian Phenex kontaktieren ↗","url":PUBLIC_SUPPORT_URL}],[{"text":"⬅ Hauptmenü","callback_data":"pub_home"}]]})
  elif command=="/donate":
   _public_send(chat_id,"♡ HUMANITÄRE SPENDENAKTION\n\nInformationen zur Initiative findest du im Aurealis Network. Zahlungswege werden dort transparent ausgewiesen.",{"inline_keyboard":[[{"text":"Spendenaktion ansehen ↗","url":NETWORK.rstrip("/")+"/#donate"}],[{"text":"⬅ Hauptmenü","callback_data":"pub_home"}]]})
  else:
   _public_send(chat_id,"Nutze /menu, /ais, /sites, /games, /shops, /register, /support oder /donate.",_public_home_markup())
 elif callback:
  try: _public_api("answerCallbackQuery",{"callback_query_id":callback.get("id","")})
  except Exception: pass
  chat_id=(callback.get("message") or {}).get("chat",{}).get("id")
  data=callback.get("data","")
  if chat_id:
   if data=="pub_home": _public_send(chat_id,"ULTIMA · Besucher-Hauptmenü",_public_home_markup())
   elif data=="pub_ais":
    _public_directory(chat_id,"🧠 KI-SYSTEME",[
     ("Aurealis OMNIA","Zentrale KI und kreative Assistenz","https://aurealis-omnia.onrender.com/"),
     ("Aurealis Creative AI Studio","Kreativwerkzeuge und Content","https://aurelis-creative-ai-studio.onrender.com/"),
     ("Quantum AI Ultra Pro","KI-Plattform","https://quantum-ki-ultra-pro-v2.onrender.com/"),
     ("Quantum AI One","KI-Assistent","https://quantum-ai-renewed.onrender.com/"),
     ("NeuroForge","KI- und Innovationssysteme","https://neuroforge-2035.onrender.com/"),
     ("IONOS-KI","KI-Plattform","https://ionos-ki.onrender.com/"),
     ("AI Quantumlight","Quantumlight-Projekt","https://ai-quantumlight.onrender.com/"),
     ("Ate Rea CharacterVerse","Charakter-KI","https://ate-rea-characterverse.onrender.com/")
    ])
   elif data=="pub_sites": _public_directory(chat_id,"🌐 WEBSITES & PROGRAMME",SITES)
   elif data=="pub_games":
    _public_directory(chat_id,"🎮 GAMES & GAME-ENGINES",[
     ("Astralis Game Engine","Entwicklungsumgebung und Spiele","https://astralis-game-engine.onrender.com/"),
     ("Quantum Mirror Wonderland","Interaktive Spielwelt","https://quantum-mirror-wonderland.onrender.com/"),
     ("Lichtkrieger Cloud Gaming","Cloud Gaming","https://lichtkrieger-cloud-gaming.onrender.com/"),
     ("The Lord Agent Network","Agenten- und Spielnetzwerk","https://the-lord-agent-network.onrender.com/")
    ])
   elif data=="pub_shops": _public_directory(chat_id,"🛍 WEBSHOPS",SHOPS)
 return jsonify(ok=True)

@bp.get("/telegram/status")
def telegram_status():
 _register_webhook_once()
 configured=bool(_token() and os.environ.get("TELEGRAM_WEBHOOK_SECRET") and os.environ.get("TELEGRAM_PUBLIC_URL"))
 api_ok=False
 remote_username=""
 remote_webhook=""
 pending_updates=None
 remote_error=""
 if _token():
  try:
   me=_api("getMe",{}).get("result",{})
   wh=_api("getWebhookInfo",{}).get("result",{})
   api_ok=bool(me.get("id"))
   remote_username=me.get("username","")
   remote_webhook=wh.get("url","")
   pending_updates=wh.get("pending_update_count",0)
   if wh.get("last_error_message"): remote_error=wh.get("last_error_message")
  except Exception as exc:
   remote_error=type(exc).__name__+": "+str(exc)[:200]
 return jsonify(bot="ULTIMA Central",username=remote_username or "Ultima_Unify_Bot",token_configured=bool(_token()),telegram_api_ok=api_ok,webhook_configured=bool(remote_webhook),webhook_url=remote_webhook,pending_updates=pending_updates,remote_error=remote_error,webhook_error=_WEBHOOK_ERROR,ready=configured and api_ok and bool(remote_webhook) and remote_webhook.endswith("/telegram/webhook"),configured_roles={"superadmin":bool(_ids("ULTIMA_TELEGRAM_SUPERADMIN_IDS")) or bool(os.environ.get("ULTIMA_TELEGRAM_SUPERADMIN_USERNAMES","ari_phenex")),"admin":bool(_ids("ULTIMA_TELEGRAM_ADMIN_IDS")),"mentor":bool(_ids("ULTIMA_TELEGRAM_MENTOR_IDS"))},membership_application=APPLY,network=NETWORK,mentor_contact=SUPPORT_URL,support_contact=SUPPORT_URL),200
