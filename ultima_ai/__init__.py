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
_agents = [
    {"id":"aurealis","name":"Aurealis","domain":"Orchestrierung & Wissen","persona":"Ruhig, präzise, strategisch. Koordiniert Aufgaben und erklärt Entscheidungen.","status":"active"},
    {"id":"aite","name":"AIte","domain":"Alltagsassistent & Dialog","persona":"Warm, empathisch, klar und lösungsorientiert.","status":"active"},
    {"id":"ionos","name":"IONOS-KI","domain":"Technologie & Entwicklung","persona":"Technisch gründlich, strukturiert, testgetrieben.","status":"planned"},
    {"id":"quantum","name":"Quantum Intelligence","domain":"Forschung & Simulation","persona":"Wissenschaftlich, unterscheidet belegte Physik von Hypothesen und Fiktion.","status":"planned"},
    {"id":"neuroforge","name":"NeuroForge","domain":"Daten & Lernsysteme","persona":"Analytisch, datenschutzbewusst, experimentell.","status":"planned"},
    {"id":"cosmican","name":"Cosmican Muse","domain":"Kreativität & Geschichten","persona":"Poetisch, bildhaft, spirituell-warm; bewahrt den Kanon der Ate-Rea-Welt.","status":"planned"},
    {"id":"guardian","name":"QuantumShield","domain":"Sicherheit & Governance","persona":"Konservativ, prüft Risiken, Rechte und Nachvollziehbarkeit.","status":"planned"},
    {"id":"studio","name":"Creative Studio","domain":"Bild, Video & Design","persona":"Kreativ, visuell denkend, achtet auf Markenidentität.","status":"planned"},
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
    {"id":"mobile","name":"Mobile Companion","stage":"planned","detail":"Installierbare Web-App und spätere native Clients."},
]
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

@bp.get("/api/status")
def status():
    configured = bool(os.getenv("OPENAI_API_KEY"))
    return jsonify(service="ULTIMA AI", version="0.1.0", status="operational", model_provider="configured" if configured else "not_configured", chat_ready=configured, agents=len(_agents), capabilities=len(_capabilities), autonomy="permission_gated", note="No shell, payment, account, publishing or destructive actions are exposed.")

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
    ], guardrails=["Keine Geheimnisse in Git","Keine unkontrollierte Shell-Ausführung","Keine Zahlungen, Kontenänderungen oder Massenveröffentlichungen","Bestehende KI-Persönlichkeiten und Projektgrenzen erhalten"])

@bp.post("/api/chat")
def chat():
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
    agent = next((a for a in _agents if a["id"] == agent_id), _agents[0])
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify(error="KI-Modell noch nicht verbunden. Hinterlege OPENAI_API_KEY und optional OPENAI_BASE_URL sowie OPENAI_MODEL als geschützte Render-Environment-Variablen.", code="provider_not_configured"), 503
    endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    payload = {"model":os.getenv("OPENAI_MODEL","gpt-4o-mini"),"messages":[
        {"role":"system","content":"Du bist "+agent["name"]+". Rolle: "+agent["persona"]+" Arbeite transparent. Erfinde keine ausgeführten Aktionen. Frage nach Freigabe vor externen, destruktiven, finanziellen oder sicherheitskritischen Handlungen. Unterscheide Fakten, Annahmen und Ideen."},
        {"role":"user","content":message}
    ],"temperature":0.6}
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode())
        answer = result["choices"][0]["message"]["content"]
        return jsonify(agent=agent["name"], answer=answer, model=result.get("model",payload["model"]))
    except urllib.error.HTTPError as exc:
        return jsonify(error="Der KI-Anbieter hat die Anfrage abgelehnt oder ist nicht erreichbar.", provider_status=exc.code), 502
    except Exception:
        return jsonify(error="KI-Anbieter derzeit nicht erreichbar. Bitte Konfiguration und Logs prüfen."), 502
