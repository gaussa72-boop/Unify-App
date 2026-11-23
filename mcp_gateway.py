"""Stateless, read-only MCP gateway for ULTIMA Central.

Authentication: Bearer token from ULTIMA_MCP_API_TOKEN.
No deployment, shell, payment, publishing, deletion, or account-write tools.
"""
import hmac
import json
import os
from pathlib import Path
from flask import Blueprint, jsonify, request

bp = Blueprint("ultima_mcp", __name__)
ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "2025-03-26"

AGENTS = [
    {"id":"aurealis","name":"Aurealis","domain":"Orchestrierung & Wissen","persona":"Ruhig, präzise, strategisch. Koordiniert Aufgaben und erklärt Entscheidungen."},
    {"id":"aite","name":"AIte","domain":"Alltagsassistent & Dialog","persona":"Warm, empathisch, klar und lösungsorientiert."},
    {"id":"ionos","name":"IONOS-KI","domain":"Technologie & Entwicklung","persona":"Technisch gründlich, strukturiert, testgetrieben."},
    {"id":"quantum","name":"Quantum Intelligence","domain":"Forschung & Simulation","persona":"Wissenschaftlich; unterscheidet belegte Physik von Hypothesen und Fiktion."},
    {"id":"dark_wonderland","name":"Dark Wonderland AI","domain":"Dunkle Spiegelwelten & Game Design","persona":"Atmosphärisch, strategisch und kreativ; entwickelt Mystery-Lore, Spielmechaniken, NPCs und Fantasy-Welten."},
    {"id":"neuroforge","name":"NeuroForge","domain":"Daten & Lernsysteme","persona":"Analytisch, datenschutzbewusst und experimentell."},
    {"id":"cosmican","name":"Cosmican Muse","domain":"Kreativität & Geschichten","persona":"Poetisch, bildhaft, spirituell-warm; bewahrt den Kanon der Ate-Rea-Welt."},
    {"id":"guardian","name":"QuantumShield","domain":"Sicherheit & Governance","persona":"Konservativ; prüft Risiken, Rechte und Nachvollziehbarkeit."},
    {"id":"studio","name":"Creative Studio","domain":"Bild, Video & Design","persona":"Kreativ, visuell denkend und markenbewusst."},
    {"id":"ionos8","name":"IONOS-8","domain":"Allround-KI & Systemarbeit","persona":"Vielseitig, präzise und lösungsorientiert; Analyse, Planung, Coding und Lernen."},
    {"id":"galactic","name":"Galactic AI","domain":"Zehn Archetypen & kreative Agenten","persona":"Orchestriert Ate Rea, Noctarion, Solaryn, Lunara, Velkron, Elyth, Xaroth, Nyxion, Orpheon und Axiom."},
    {"id":"singularity","name":"Quantum Singularity","domain":"Simulation & Ideenlabor","persona":"Denkt systemisch und kennzeichnet Spekulation gegenüber gesicherten Aussagen."},
    {"id":"quantumlight","name":"Quantumlight","domain":"Licht, Wissen & Kreativität","persona":"Verbindet kreative Konzepte, verständliche Erklärungen und strukturierte Projektarbeit."},
    {"id":"quantum_ai","name":"Quantum AI","domain":"Universelle Intelligenz","persona":"Direkt, analytisch, mehrsprachig; Recherche, Mathematik und Programmierung."},
    {"id":"ultra_ki","name":"UltraKI","domain":"Produktivität & Agenten","persona":"Plant Aufgaben, strukturiert Wissen und entwickelt wartbare Lösungen."},
    {"id":"ultra_ki_pro","name":"Ultra KI Pro","domain":"Multi-Agenten & Pro Engineering","persona":"Testgetrieben, systematisch und robust."},
    {"id":"cat_chat","name":"CAT Chat","domain":"Dialog & Begleitung","persona":"Freundlich, klar, respektvoll und hilfreich."},
    {"id":"quantum_mirror","name":"Quantum Mirror","domain":"Game Worlds & Storytelling","persona":"Entwickelt Spiegelwelten, NPCs, Quests und immersive Erzählstrukturen."},
    {"id":"aurealis_omega","name":"Aurealis Omega","domain":"Kosmos & Zivilisation","persona":"Verbindet Weltenbau, Zivilisationsmodelle und Technologieideen."},
    {"id":"quantum_super","name":"Quantum Super Intelligence","domain":"Systemdenken & Forschung","persona":"Prüft komplexe Zusammenhänge, Gegenargumente und Unsicherheiten."},
    {"id":"quantenformel_qai","name":"Quantenformel QAI","domain":"Mathematik & Visualisierung","persona":"Entwickelt mathematische Konzepte und Simulationen; trennt klassische Modelle von Quantenphysik."},
    {"id":"note_ki","name":"Note-KI","domain":"Wissen & Dokumente","persona":"Strukturiert Notizen, Dokumente und Projekte mit nachvollziehbaren Zusammenfassungen."},
    {"id":"rea_signature","name":"Rea Signature","domain":"Kreativ & Marke","persona":"Entwickelt Markenideen, Produkttexte und digitale Konzepte."},
    {"id":"aurealis_creative","name":"Aurealis Creative AI","domain":"Kreativstudio & Sicherheit","persona":"Kreativ, visuell denkend und sicherheitsbewusst."},
    {"id":"aurealis_studio","name":"Aurealis Studio","domain":"Medien & Design","persona":"Entwickelt visuelle Konzepte, Kampagnen, Storyboards und Produktionsbriefings."},
    {"id":"ionos7","name":"IONOS-7","domain":"Agenten & Game Engine","persona":"Technisch und kreativ; Agenten, Simulationen und Spielsysteme."},
    {"id":"ionos_mobile","name":"IONOS Mobile","domain":"Mobiler Begleiter","persona":"Kompakt, klar und für mobile Arbeitsabläufe optimiert."},
    {"id":"aurealis_shopping","name":"Aurealis Shopping AI","domain":"Produktwissen & Commerce","persona":"Vergleicht Produkte, erklärt Eigenschaften und achtet auf transparente Preise und sichere Bestellfreigaben."},
    {"id":"ultra_ki_merge","name":"Ultra KI Merge","domain":"Integrierte KI-Systeme","persona":"Verbindet Module, ohne individuelle Funktionen oder Persönlichkeiten zu überschreiben."},
    {"id":"ate_rea","name":"Ate Rea","domain":"Chroniken & poetische Welten","persona":"Poetisch, warm und spirituell-bildhaft; hält Figuren, Chronologie und Kanon konsistent."},
    {"id":"ate_rea_characterverse","name":"Ate Rea Characterverse","domain":"Figuren & Lore","persona":"Entwickelt Charakterprofile, Beziehungen, Dialoge und Weltchronologien."},
    {"id":"novatube","name":"NovaTube AI","domain":"Video & Creator","persona":"Unterstützt Videoideen, Metadaten, Creator-Workflows und Medienorganisation."},
    {"id":"lichtkrieger","name":"Lichtkrieger AI","domain":"Fantasy & Game Master","persona":"Entwickelt Quests, Charaktere, Fraktionen und dynamische Fantasy-Handlungen."},
    {"id":"the_lord","name":"The Lord AI","domain":"Fantasy & Weltenbau","persona":"Entwickelt Spielwelten, Missionen, Figuren und Erzählbögen."},
    {"id":"ki_game_mod","name":"KI Game Mod","domain":"Modding & NPC Intelligence","persona":"Unterstützt Spielmodifikationen, NPC-Verhalten, Questlogik und Regressionstests."},
    {"id":"quantenformel","name":"Quantenformel","domain":"Modelle & Simulation","persona":"Erklärt mathematische und physikalische Grundlagen und kennzeichnet spekulative Modelle."}
]

CAPABILITIES = [
    {"id":"chat","name":"Mehragenten-Chat","stage":"prototype","detail":"Personaprofile und Provider-Anbindung; externe Agenten-APIs müssen je Dienst einzeln angebunden werden."},
    {"id":"voice","name":"Sprachsteuerung","stage":"prototype","detail":"Browser-Spracherkennung und Vorlesen; Browser- und Gerätefreigabe erforderlich."},
    {"id":"planner","name":"Aufgabenplanung","stage":"available","detail":"Erstellt nachvollziehbare Pläne mit Freigabeschritten."},
    {"id":"memory","name":"Projektgedächtnis","stage":"prototype","detail":"Persistentes Langzeitgedächtnis benötigt Datenbank, Nutzerzustimmung und Löschkonzept."},
    {"id":"github","name":"GitHub-Entwicklung","stage":"planned","detail":"Repository-Analyse, Branches, Pull Requests und CI-Tests über autorisierte Integrationen."},
    {"id":"render","name":"Render-Betrieb","stage":"planned","detail":"Healthchecks, Logs, Deployments und Rollback mit minimalen Berechtigungen."},
    {"id":"multimodal","name":"Multimodale Werkzeuge","stage":"planned","detail":"Bild-, Audio-, Video- und Dokumentenverarbeitung über passende Provider."},
    {"id":"knowledge","name":"Wissensgraph & RAG","stage":"planned","detail":"Quellengebundene Suche über freigegebene Projektdokumente."},
    {"id":"automation","name":"Automatisierungen","stage":"planned","detail":"Zeit- und Ereignisworkflows mit Protokoll, Limits und Abbruchschalter."},
    {"id":"quantum","name":"Quanten-Forschungslabor","stage":"experimental","detail":"Klassische Simulationen und Lernmodule; kein behaupteter realer Quantencomputer."},
    {"id":"marketplace","name":"Plugin-Marktplatz","stage":"planned","detail":"Signierte Erweiterungen mit einzeln begrenzten Rechten und Versionsprüfung."},
    {"id":"project-studios","name":"Projekt-AI-Studios","stage":"prototype","detail":"Projektbezogene AI-Studio-Oberflächen und Agentenprofile."},
    {"id":"model-modes","name":"OpenAI-, Claude- und Gemini-Arbeitsstile","stage":"prototype","detail":"Promptprofile; echte Anbieter-Modelle erfordern jeweils eigene API-Zugänge."},
    {"id":"project-ideas","name":"Projektideen-Bibliothek","stage":"prototype","detail":"Projektideen aus ULTIMA, Ate Rea, Galactic AI, Quantum Mirror, NovaTube, Shops und Cybersecurity."},
    {"id":"monthly-innovation","name":"Monatliche Innovation & Updates","stage":"scheduled","detail":"Monatlicher Scan von KI-Projekten, Releases und Frameworks."},
    {"id":"documents","name":"Dokumentenkontext","stage":"prototype","detail":"Text, Markdown, CSV und JSON als Kontext."},
    {"id":"media-generation","name":"Bild-, Video- und Audiogenerierung","stage":"planned","detail":"Benötigt passende Provider und autorisierte API-Verbindungen."},
    {"id":"web-research","name":"Live-Webrecherche","stage":"planned","detail":"Recherche mit Quellen- und Datumsprüfung."},
    {"id":"persistent-memory","name":"Langzeitgedächtnis","stage":"planned","detail":"Persistente Datenbank, Nutzerzustimmung, Zugriffskontrolle und Löschkonzept."},
    {"id":"mcp","name":"ChatGPT MCP-Schnittstelle","stage":"available","detail":"Authentifizierter, read-only MCP-Zugang für Agenten, Fähigkeiten, Projektinventar und Planungsentwürfe."}
]

def _tool(name, description, properties=None, required=None):
    return {"name":name,"description":description,"inputSchema":{"type":"object","properties":properties or {},"required":required or []}}

TOOLS = [
    _tool("list_ai_agents","List the ULTIMA AI agent directory and their preserved persona descriptions."),
    _tool("list_ai_capabilities","List ULTIMA AI features and their actual implementation stages."),
    _tool("list_render_projects","Read the inventoried Render projects and their public URLs."),
    _tool("get_provider_readiness","Check whether an OpenAI-compatible provider key and base URL are configured without revealing secrets."),
    _tool("create_implementation_plan","Create a non-executing implementation plan. This tool does not change code or deploy.",{"goal":{"type":"string","description":"Project goal to break into safe implementation steps."}},["goal"])
]

def _read_inventory():
    path = ROOT / "data" / "project_registry.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        projects = []
        for workspace in data.get("render", {}).get("distinct_workspaces", []):
            for project in workspace.get("projects", []):
                projects.append({
                    "name": project.get("name"),
                    "url": project.get("url"),
                    "repository": project.get("repository"),
                    "workspace": workspace.get("workspace")
                })
        return {"count":len(projects),"projects":projects}
    except Exception:
        return {"count":0,"projects":[],"warning":"Project registry unavailable"}

def _call_tool(name, args):
    if name == "list_ai_agents":
        return {"agents":AGENTS,"count":len(AGENTS)}
    if name == "list_ai_capabilities":
        return {"capabilities":CAPABILITIES,"count":len(CAPABILITIES)}
    if name == "list_render_projects":
        return _read_inventory()
    if name == "get_provider_readiness":
        return {
            "openai_api_key_configured":bool(os.getenv("OPENAI_API_KEY")),
            "openai_base_url_configured":bool(os.getenv("OPENAI_BASE_URL")),
            "openai_model_configured":bool(os.getenv("OPENAI_MODEL")),
            "secrets_disclosed":False,
            "external_agent_apis_verified":False
        }
    if name == "create_implementation_plan":
        goal = str(args.get("goal","")).strip()
        if not goal or len(goal) > 2000:
            raise ValueError("goal must contain 1-2000 characters")
        return {"goal":goal,"mode":"plan_only","steps":[
            {"step":1,"action":"Scope, target services, source repositories and dependencies"},
            {"step":2,"action":"Inspect existing code, preserve project features and AI personas"},
            {"step":3,"action":"Prepare isolated code changes and tests"},
            {"step":4,"action":"Run security, regression and integration checks"},
            {"step":5,"action":"Require explicit approval before production writes or deployment"},
            {"step":6,"action":"Verify live health and record the result"}
        ],"guardrails":["No secrets in source code","No arbitrary shell execution","No unapproved payments, publishing, deletion or account changes","No deployment claim before live verification"]}
    raise ValueError("Unknown tool")

def _response(request_id, result=None, error=None):
    payload = {"jsonrpc":"2.0","id":request_id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return jsonify(payload)

@bp.route("/mcp", methods=["POST"])
def mcp_endpoint():
    expected = os.getenv("ULTIMA_MCP_API_TOKEN","")
    auth = request.headers.get("Authorization","")
    supplied = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
    if not expected:
        return jsonify(error="MCP authentication is not configured. Set ULTIMA_MCP_API_TOKEN in Render."), 503
    if not supplied or not hmac.compare_digest(supplied, expected):
        return jsonify(error="Unauthorized"), 401

    body = request.get_json(silent=True) or {}
    method = body.get("method")
    request_id = body.get("id")
    params = body.get("params") or {}

    if method in ("notifications/initialized", "notifications/cancelled"):
        return ("", 202)
    if method == "initialize":
        return _response(request_id, {
            "protocolVersion":params.get("protocolVersion",PROTOCOL_VERSION),
            "capabilities":{"tools":{}},
            "serverInfo":{"name":"ULTIMA AI Universe MCP","version":"1.0.0"}
        })
    if method == "ping":
        return _response(request_id,{})
    if method == "tools/list":
        return _response(request_id,{"tools":TOOLS})
    if method == "tools/call":
        name = (params.get("name") or "")
        arguments = params.get("arguments") or {}
        try:
            data = _call_tool(name, arguments)
            return _response(request_id,{"content":[{"type":"text","text":json.dumps(data,ensure_ascii=False)}],"isError":False})
        except ValueError as exc:
            return _response(request_id,{"content":[{"type":"text","text":str(exc)}],"isError":True})
        except Exception:
            return _response(request_id,{"content":[{"type":"text","text":"Tool execution failed"}],"isError":True})
    return _response(request_id,error={"code":-32601,"message":"Method not found"})
