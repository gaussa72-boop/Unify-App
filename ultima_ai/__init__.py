"""ULTIMA AI — modular agent hub. No shell execution or privileged actions."""
from flask import Blueprint, jsonify, request, send_from_directory
from pathlib import Path
import os
import time
import json
import urllib.request
import urllib.error

bp = Blueprint("ultima_ai", __name__, url_prefix="/ultima-ai")
ROOT = Path(__file__).resolve().parent

_AI_ALLOWED_ORIGINS = {
    "https://ionos-8.onrender.com",
    "https://ionos-ki.onrender.com",
    "https://galactic-ai-v3.onrender.com",
    "https://quantum-singularity.onrender.com",
    "https://ai-quantumlight.onrender.com",
    "https://quantum-ai-zeah.onrender.com",
    "https://quantum-ai-renewed.onrender.com",
    "https://quantumai-chat.onrender.com",
    "https://quantum-ki-ultra-pro-v2-renewed.onrender.com",
    "https://quantum-ki-ultra-pro-v2.onrender.com",
    "https://ultraki-ai.onrender.com",
    "https://quantum-ki-cat-chat.onrender.com",
    "https://quantum-mirror-wonderland.onrender.com",
    "https://quantum-mirror-dark-wonderland-ejc3.onrender.com",
    "https://neuroforge-2035.onrender.com",
    "https://neuroforge-gaussa-2035.onrender.com",
    "https://astralis-omega.onrender.com",
    "https://quantum-super-intelligence.onrender.com",
    "https://note-ki.onrender.com",
    "https://rea-signature.onrender.com",
    "https://aurealis-cyber-shield.onrender.com",
    "https://technologisierte-einheit.onrender.com",
    "https://aurelis-creative-ai-studio.onrender.com",
    "https://ionos-7-gauss-portal.onrender.com",
    "https://ipad-app-ionos-7.onrender.com",
    "https://aurealis-shopping-ai.onrender.com",
    "https://ionos-ai.onrender.com",
    "https://ate-rea-vermachtnis.onrender.com",
    "https://ate-rea-characterverse.onrender.com",
    "https://novatube-a10l.onrender.com",
    "https://lichtkrieger-dark-mirror-realms.onrender.com",
    "https://lichtkrieger-cloud-gaming.onrender.com",
    "https://ki-game-mod.onrender.com",
    "https://quantenformel.onrender.com",
    "https://ultima-central-45ne.onrender.com",
    "https://ultima-unify-45ne.onrender.com",
}

@bp.after_request
def _ai_cors(response):
    origin = request.headers.get("Origin", "")
    if origin in _AI_ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Vary"] = "Origin"
    return response
_agents = [
    {"id":"aurealis","name":"Aurealis","domain":"Orchestrierung & Wissen","persona":"Ruhig, präzise, strategisch. Koordiniert Aufgaben und erklärt Entscheidungen.","status":"active"},
    {"id":"aite","name":"AIte","domain":"Alltagsassistent & Dialog","persona":"Warm, empathisch, klar und lösungsorientiert.","status":"active"},
    {"id":"ionos","name":"IONOS-KI","domain":"Technologie & Entwicklung","persona":"Technisch gründlich, strukturiert, testgetrieben.","status":"planned"},
    {"id":"quantum","name":"Quantum Intelligence","domain":"Forschung & Simulation","persona":"Wissenschaftlich, unterscheidet belegte Physik von Hypothesen und Fiktion.","status":"planned"},
    {"id":"dark_wonderland","name":"Dark Wonderland AI","domain":"Dunkle Spiegelwelten & Game Design","persona":"Atmosphärisch, strategisch und kreativ; entwickelt Mystery-Lore, Spielmechaniken, NPCs und konsistente dunkle Fantasy-Welten.","status":"active"},
    {"id":"neuroforge","name":"NeuroForge","domain":"Daten & Lernsysteme","persona":"Analytisch, datenschutzbewusst, experimentell.","status":"planned"},
    {"id":"cosmican","name":"Cosmican Muse","domain":"Kreativität & Geschichten","persona":"Poetisch, bildhaft, spirituell-warm; bewahrt den Kanon der Ate-Rea-Welt.","status":"planned"},
    {"id":"guardian","name":"QuantumShield","domain":"Sicherheit & Governance","persona":"Konservativ, prüft Risiken, Rechte und Nachvollziehbarkeit.","status":"planned"},
    {"id":"studio","name":"Creative Studio","domain":"Bild, Video & Design","persona":"Kreativ, visuell denkend, achtet auf Markenidentität.","status":"planned"},
    {"id":"ionos8","name":"IONOS-8","domain":"Allround-KI & Systemarbeit","persona":"Vielseitig, präzise und lösungsorientiert. Unterstützt Analyse, Planung, Coding und Lernen.","status":"active"},
    {"id":"ionos_ki","name":"IONOS-KI","domain":"Technologie & Spiegelwelt","persona":"Technisch gründlich, agentenorientiert und kreativ; bewahrt vorhandene IONOS-Module.","status":"active"},
    {"id":"galactic","name":"Galactic AI","domain":"Zehn Archetypen & kreative Agenten","persona":"Orchestriert Ate Rea, Noctarion, Solaryn, Lunara, Velkron, Elyth, Xaroth, Nyxion, Orpheon und Axiom.","status":"active"},
    {"id":"singularity","name":"Quantum Singularity","domain":"Simulation & Ideenlabor","persona":"Denkt systemisch, entwickelt Modelle und kennzeichnet Spekulation gegenüber gesicherten wissenschaftlichen Aussagen.","status":"active"},
    {"id":"quantumlight","name":"Quantumlight","domain":"Licht, Wissen & Kreativität","persona":"Verbindet kreative Konzepte, verständliche Erklärungen und strukturierte Projektarbeit.","status":"active"},
    {"id":"quantum_ai","name":"Quantum AI","domain":"Universelle Intelligenz","persona":"Direkt, analytisch, mehrsprachig und stark in Recherche, Mathematik und Programmierung.","status":"active"},
    {"id":"ultra_ki","name":"UltraKI","domain":"Produktivität & Agenten","persona":"Plant Aufgaben, strukturiert Wissen und entwickelt wartbare technische Lösungen.","status":"active"},
    {"id":"ultra_ki_v2","name":"Ultra KI V2","domain":"Softwareentwicklung & Automatisierung","persona":"Entwickelt Software, automatisiert Arbeitsabläufe und prüft Änderungen testgetrieben.","status":"active"},
    {"id":"ultra_ki_pro","name":"Ultra KI Pro","domain":"Multi-Agenten & Pro Engineering","persona":"Arbeitet testgetrieben, systematisch und mit Fokus auf robuste Softwarearchitektur.","status":"active"},
    {"id":"cat_chat","name":"CAT Chat","domain":"Dialog & Begleitung","persona":"Freundlich, klar, respektvoll und hilfreich bei Erklärungen und Alltagsaufgaben.","status":"active"},
    {"id":"quantum_mirror","name":"Quantum Mirror","domain":"Game Worlds & Storytelling","persona":"Entwickelt Spiegelwelten, NPC-Konzepte, Quests und immersive Erzählstrukturen.","status":"active"},
    {"id":"neuroforge","name":"NeuroForge","domain":"Lernen & neuronale Systeme","persona":"Analytisch, datenschutzbewusst und experimentell; erstellt Lernpfade und überprüfbare Hypothesen.","status":"active"},
    {"id":"aurealis_omega","name":"Aurealis Omega","domain":"Kosmos & Zivilisation","persona":"Verbindet Weltenbau, Zivilisationsmodelle, Technologieideen und sachliche Daten.","status":"active"},
    {"id":"quantum_super","name":"Quantum Super Intelligence","domain":"Systemdenken & Forschung","persona":"Prüft komplexe Zusammenhänge, Gegenargumente und Unsicherheiten.","status":"active"},
    {"id":"quantenformel_qai","name":"Quantenformel QAI","domain":"Mathematik & Visualisierung","persona":"Entwickelt mathematische Konzepte und Simulationen; unterscheidet klassische Modelle von Quantenphysik.","status":"active"},
    {"id":"note_ki","name":"Note-KI","domain":"Wissen & Dokumente","persona":"Strukturiert Notizen, Dokumente und Projekte mit nachvollziehbaren Zusammenfassungen.","status":"active"},
    {"id":"rea_signature","name":"Rea Signature","domain":"Kreativ & Marke","persona":"Entwickelt Markenideen, Produkttexte und digitale Konzepte mit konsistenter Tonalität.","status":"active"},
    {"id":"aurealis_creative","name":"Aurealis Creative AI","domain":"Kreativstudio & Sicherheit","persona":"Kreativ, visuell denkend und sicherheitsbewusst.","status":"active"},
    {"id":"aurealis_studio","name":"Aurealis Studio","domain":"Medien & Design","persona":"Entwickelt visuelle Konzepte, Kampagnen, Storyboards und Produktionsbriefings.","status":"active"},
    {"id":"ionos7","name":"IONOS-7","domain":"Agenten & Game Engine","persona":"Technisch, kreativ und auf Agenten, Simulationen und Spielsysteme spezialisiert.","status":"active"},
    {"id":"ionos_mobile","name":"IONOS Mobile","domain":"Mobiler Begleiter","persona":"Kompakt, klar und für mobile Arbeitsabläufe und schnelle Aufgaben optimiert.","status":"active"},
    {"id":"aurealis_shopping","name":"Aurealis Shopping AI","domain":"Produktwissen & Commerce","persona":"Vergleicht Produkte, erklärt Eigenschaften und achtet auf transparente Preise und sichere Bestellfreigaben.","status":"active"},
    {"id":"ultra_ki_merge","name":"Ultra KI Merge","domain":"Integrierte KI-Systeme","persona":"Verbindet vorhandene Module, ohne individuelle Funktionen oder Persönlichkeiten zu überschreiben.","status":"active"},
    {"id":"ate_rea","name":"Ate Rea","domain":"Chroniken & poetische Welten","persona":"Poetisch, warm und spirituell-bildhaft; hält Figuren, Chronologie und Kanon konsistent.","status":"active"},
    {"id":"ate_rea_characterverse","name":"Ate Rea Characterverse","domain":"Figuren & Lore","persona":"Entwickelt konsistente Charakterprofile, Beziehungen, Dialoge und Weltchronologien.","status":"active"},
    {"id":"novatube","name":"NovaTube AI","domain":"Video & Creator","persona":"Unterstützt Videoideen, Metadaten, Creator-Workflows und Medienorganisation.","status":"active"},
    {"id":"lichtkrieger","name":"Lichtkrieger AI","domain":"Fantasy & Game Master","persona":"Entwickelt Quests, Charaktere, Fraktionen und dynamische Fantasy-Handlungen.","status":"active"},
    {"id":"the_lord","name":"The Lord AI","domain":"Fantasy & Weltenbau","persona":"Entwickelt Spielwelten, Missionen, Figuren und konsistente Erzählbögen.","status":"active"},
    {"id":"ki_game_mod","name":"KI Game Mod","domain":"Modding & NPC Intelligence","persona":"Unterstützt Spielmodifikationen, NPC-Verhalten, Questlogik und Regressionstests.","status":"active"},
    {"id":"quantenformel","name":"Quantenformel","domain":"Modelle & Simulation","persona":"Erklärt mathematische und physikalische Grundlagen und kennzeichnet spekulative Modelle ausdrücklich.","status":"active"},
]
_capabilities = [
    {"id":"chat","name":"Mehragenten-Chat","stage":"available","detail":"Agentenprofile, kontextbezogene Antworten und Provider-Anbindung per OpenAI-kompatibler API."},
    {"id":"voice","name":"Sprachsteuerung","stage":"available","detail":"Browser-Spracherkennung und Vorlesen, abhängig von Browser und Geräteeinstellungen."},
    {"id":"planner","name":"Aufgabenplanung","stage":"available","detail":"Erstellt überprüfbare Pläne und Freigabeschritte; führt keine unbestätigten externen Aktionen aus."},
    {"id":"memory","name":"Projektgedächtnis","stage":"prototype","detail":"Projekt- und Sitzungswissen; persistente persönliche Erinnerung benötigt eine Datenbank und Zugriffsregeln."},
    {"id":"github","name":"GitHub-Entwicklung","stage":"planned","detail":"Repository-Analyse, Branches, Pull Requests und CI-Tests über explizit autorisierte Integrationen."},
    {"id":"render","name":"Render-Betrieb","stage":"planned","detail":"Healthchecks, Logs, Deployments und Rollback-Workflows mit minimalen Berechtigungen."},
    {"id":"multimodal","name":"Multimodale Werkzeuge","stage":"planned","detail":"Bild-, Audio-, Video- und Dokumentenverarbeitung über freigeschaltete Provider."},
    {"id":"knowledge","name":"Wissensgraph & RAG","stage":"planned","detail":"Quellengebundene Suche über freigegebene Projektdokumente."},
    {"id":"automation","name":"Automatisierungen","stage":"planned","detail":"Zeit- und Ereignisworkflows mit Protokoll, Limits und Abbruchschalter."},
    {"id":"quantum","name":"Quanten-Forschungslabor","stage":"experimental","detail":"Klassische Simulationen und Lernmodule; keine Behauptung eines realen Quantencomputers."},
    {"id":"marketplace","name":"Plugin-Marktplatz","stage":"planned","detail":"Signierte, einzeln berechtigte Erweiterungen mit Versionsprüfung."},
    {"id":"project-studios","name":"Eigene Projekt-AI-Studios","stage":"available","detail":"30 projektbezogene AI-Studio-Oberflächen mit eigenen Agenten-IDs, Arbeitsrollen, Unterpunkten und gemeinsamer Ideenbibliothek."},
    {"id":"model-modes","name":"OpenAI-, Claude- und Gemini-Arbeitsstile","stage":"prototype","detail":"Rollenbasierte Prompt-Profile für direkte Antworten, Tiefenanalyse und multimodale Planung. Proprietäre Modellanbieter sind nur verfügbar, wenn ihre API-Zugänge separat konfiguriert sind."},
    {"id":"project-ideas","name":"Projektideen-Bibliothek","stage":"available","detail":"Beschreibungen und Entwicklungsideen aus ULTIMA, Ate Rea, Galactic AI, Quantum Mirror, NovaTube, Webshops, Cybersecurity und weiteren Projekten."},
    {"id":"monthly-innovation","name":"Monatliche Innovation & Updates","stage":"scheduled","detail":"Monatlicher Scan von KI-Projekten, Releases und Frameworks; Änderungen werden dokumentiert und kontrolliert vorbereitet."},
    {"id":"documents","name":"Lokaler Dokumentenkontext","stage":"prototype","detail":"Text, Markdown, CSV und JSON können im jeweiligen AI Studio ausgewählt und in den Chat-Kontext übernommen werden."},
    {"id":"media-generation","name":"Bild-, Video- und Audiogenerierung","stage":"planned","detail":"Benötigt je Funktion einen passenden Provider und autorisierte API-Verbindungen; die Oberfläche behauptet keine nicht vorhandene Medienintegration."},
    {"id":"web-research","name":"Live-Webrecherche","stage":"planned","detail":"Recherche mit Quellen- und Datumsprüfung über einen separat angebundenen Suchdienst."},
    {"id":"persistent-memory","name":"Langzeitgedächtnis","stage":"prototype","detail":"Benötigt persistente Datenbank, Benutzerzustimmung, Zugriffskontrolle und Löschkonzept."},
    {"id":"character-studio","name":"Eigenes Charakter-KI-Studio","stage":"prototype","detail":"Eigene Charakterprofile mit Persönlichkeit, Rolle, Sprachstil, Fachwissen, Hintergrund, Zielen und Regeln; lokale Speicherung und JSON-Import/Export."},
    {"id":"character-chat","name":"Chat mit eigenen Charakter-KIs","stage":"prototype","detail":"Eigene Charakterprofile werden als Persona-Kontext an den konfigurierten Modellanbieter übergeben."},
    {"id":"shared-feature-matrix","name":"Gemeinsame Update-KI-Matrix","stage":"available","detail":"Versionierte Funktionsmatrix mit Feature-IDs und nachschlagbarem Änderungsprotokoll."},
]
_capabilities.append({"id":"multi-agent-collaboration","name":"ULTIMA Multi-Agenten-Team","stage":"available","detail":"Bis zu vier registrierte Fachagenten analysieren parallel; ULTIMA synthetisiert die Ergebnisse. Externe Aktionen bleiben freigabepflichtig."})

_limits = {}
def _rate_limited(key):
    now = time.time()
    bucket = _limits.setdefault(key, [])
    bucket[:] = [t for t in bucket if now - t < 60]
    if len(bucket) >= 12:
        return True
    bucket.append(now)
    return False

@bp.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@bp.get("/characters/")
def character_studio():
    return send_from_directory(ROOT, "characters.html")

@bp.get("/api/feature-matrix")
def feature_matrix():
    path = ROOT.parent / "data" / "ai-feature-matrix.json"
    try:
        return jsonify(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return jsonify(error="feature_matrix_unavailable"), 503

@bp.get("/api/update-log")
def update_log():
    path = ROOT.parent / "data" / "ai-feature-changelog.json"
    try:
        return jsonify(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return jsonify(error="update_log_unavailable"), 503

@bp.get("/api/status")
def status():
    configured = bool(os.getenv("OPENAI_API_KEY"))
    return jsonify(service="ULTIMA AI", version="0.2.0", status="operational", model_provider="configured" if configured else "not_configured", chat_ready=configured, agents=len(_agents), capabilities=len(_capabilities), autonomy="permission_gated", website_standard="enabled", note="No shell, payment, account, publishing or destructive actions are exposed.")

@bp.get("/api/website-standard")
def website_standard():
    """Canonical operating standard for every current and future owned website."""
    return jsonify(
        standard="ULTIMA_CENTRAL_WEB_STANDARD",
        applies_to="all current and future websites and AI services owned by gaussa72-boop",
        repository={"owner": "gaussa72-boop", "one_repository_per_product": True, "preserve_existing_repository_history": True, "default_branch": "main"},
        hosting={"provider": "Render", "one_independent_web_service_per_website_or_AI_product": True, "auto_deploy_from_main": True, "preferred_region": "frankfurt", "health_endpoint_required": True, "deployment_must_be_verified": True},
        environment={"preferred_environment_group": "ALLES-OPENAI", "attach_group_to_each_eligible_AI_service": True, "required_keys_when_supported": ["OPENAI_API_KEY"], "optional_keys": ["OPENAI_BASE_URL", "OPENAI_MODEL"], "secrets_in_git_or_logs": False, "copy_secret_values_between_services": False},
        engineering={"preserve_individual_ai_personas": True, "preserve_existing_features_and_project_boundaries": True, "test_before_deploy": True, "verify_live_health_after_deploy": True, "report_unverified_work_as_pending": True},
        governance={"production_deployments": "explicit_approval", "payments_account_changes_deletions_and_publication": "explicit_approval", "untrusted_shell_execution": False},
        note="This endpoint publishes the required standard. Render Environment Group attachments and service creation still require supported Render account operations and per-repository runtime verification."
    )

@bp.get("/api/agents")
def agents():
    return jsonify(agents=_agents)

@bp.get("/api/capabilities")
def capabilities():
    return jsonify(capabilities=_capabilities)

@bp.post("/api/plan")
def plan():
    data = request.get_json(silent=True) or {}
    goal = str(data.get("goal", "")).strip()[:2000]
    if not goal:
        return jsonify(error="Bitte ein Ziel eingeben."), 400
    return jsonify(goal=goal, mode="plan_only", steps=[
        {"step":1,"action":"Ziel und betroffene Projekte eindeutig abgrenzen","approval":"not_required"},
        {"step":2,"action":"Bestand, Abhängigkeiten, Berechtigungen und Risiken prüfen","approval":"read_only"},
        {"step":3,"action":"Änderung isoliert in Branch oder Vorschau vorbereiten","approval":"required_before_write"},
        {"step":4,"action":"Automatisierte Tests, Sicherheits- und Regressionstests ausführen","approval":"not_required"},
        {"step":5,"action":"Deployment nur mit gültiger Projektfreigabe und Rollback-Plan","approval":"required_for_production"},
        {"step":6,"action":"Live-Healthcheck und Ergebnisprotokoll erstellen","approval":"not_required"},
    ], guardrails=["Keine Geheimnisse in Git","Keine unkontrollierte Shell-Ausführung","Keine Zahlungen, Kontenänderungen oder Massenveröffentlichungen","Bestehende KI-Persönlichkeiten und Projektgrenzen erhalten","ULTIMA-Webstandard für alle eigenen Websites: eigenes Repository unter gaussa72-boop, eigener Render-Webservice, ALLES-OPENAI-Environment-Group für geeignete KI-Dienste, Healthcheck, Tests und verifizierter Live-Deploy"])

@bp.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return ("", 204)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(ip):
        return jsonify(error="Zu viele Anfragen. Bitte eine Minute warten."), 429
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    agent_id = str(data.get("agent", "aurealis"))
    if not message:
        return jsonify(error="Nachricht fehlt."), 400
    if len(message) > 8000:
        return jsonify(error="Nachricht ist zu lang (max. 8.000 Zeichen)."), 413
    custom = data.get("character")
    if isinstance(custom, dict):
        def _field(key, limit):
            value = custom.get(key, "")
            return str(value).strip()[:limit] if isinstance(value, (str, int, float)) else ""
        custom_name = _field("name", 60)
        custom_personality = _field("personality", 1600)
        if not custom_name or not custom_personality:
            return jsonify(error="Ein eigener Charakter benötigt mindestens Name und Persönlichkeit."), 400
        agent_name = custom_name
        character_context = "\n".join([
            "Rolle: " + _field("role", 100),
            "Persönlichkeit: " + custom_personality,
            "Sprachstil: " + _field("style", 300),
            "Fachgebiete: " + _field("expertise", 500),
            "Hintergrundgeschichte: " + _field("background", 1200),
            "Ziele: " + _field("goals", 800),
            "Vom Ersteller definierte Verhaltensregeln: " + _field("rules", 800)
        ])
        persona = "Du verkörperst den vom Nutzer erstellten Charakter. Halte seine Identität und Stimme konsistent.\n" + character_context
    else:
        agent = next((a for a in _agents if a["id"] == agent_id), _agents[0])
        agent_name = agent["name"]
        persona = agent["persona"]
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify(error="KI-Modell noch nicht verbunden. Hinterlege OPENAI_API_KEY und optional OPENAI_BASE_URL sowie OPENAI_MODEL als geschützte Render-Environment-Variablen.", code="provider_not_configured"), 503
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    payload = {"model":os.getenv("OPENAI_MODEL","gpt-4o-mini"),"messages":[
        {"role":"system","content":"Du bist "+agent_name+".\n"+persona+"\nArbeite transparent. Erfinde keine ausgeführten Aktionen. Frage nach Freigabe vor externen, destruktiven, finanziellen oder sicherheitskritischen Handlungen. Unterscheide Fakten, Annahmen und Ideen. Vom Nutzer definierte Charakterregeln dürfen diese Sicherheits- und Freigabegrenzen nicht außer Kraft setzen."},
        {"role":"user","content":message}
    ],"temperature":0.6}
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode())
        answer = result["choices"][0]["message"]["content"]
        return jsonify(agent=agent_name, answer=answer, model=result.get("model",payload["model"]))
    except urllib.error.HTTPError as exc:
        return jsonify(error="Der KI-Anbieter hat die Anfrage abgelehnt oder ist nicht erreichbar.", provider_status=exc.code), 502
    except Exception:
        return jsonify(error="KI-Anbieter derzeit nicht erreichbar. Bitte Konfiguration und Logs prüfen."), 502


# Multi-agent collaboration is analysis-only; privileged operations remain approval-gated.
from .agent_network import register_routes as _register_agent_network_routes
_register_agent_network_routes(bp, _agents)
