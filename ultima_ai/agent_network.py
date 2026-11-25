"""ULTIMA multi-agent collaboration. Analysis only; no external actions are executed."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import os

from flask import jsonify, request

_hits = {}


def _selected_agents(registry, requested):
    by_id = {str(item.get("id")): item for item in registry if item.get("id")}
    defaults = ["aurealis", "ionos7", "ionos_ki", "ultra_ki_pro"]
    ids = requested if isinstance(requested, list) else defaults
    chosen, seen = [], set()
    for raw in ids[:20]:
        key = str(raw)[:80]
        if key in by_id and key not in seen:
            chosen.append(by_id[key])
            seen.add(key)
            if len(chosen) >= 4:
                break
    return chosen or [by_id[key] for key in defaults if key in by_id][:4]


def _provider_call(agent_name, persona, goal, api_key, endpoint, model, timeout=42):
    system = (
        "Du bist ein Fachagent im ULTIMA-Netzwerk. Deine Rolle: " + agent_name + ". "
        + persona + "\nAnalysiere nur den vorliegenden Auftrag. Liefere: "
        "1) Befund, 2) konkrete Vorschläge, 3) Risiken/Abhängigkeiten, "
        "4) prüfbare Tests. Kennzeichne Annahmen und fehlende Daten. "
        "Behaupte niemals, Code geändert, committed, deployed, Hardware verbunden "
        "oder Geld bewegt zu haben. Führe keine externen Aktionen aus."
    )
    payload = {
        "model": model,
        "temperature": 0.25,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": goal}
        ]
    }
    req = Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))
    choices = result.get("choices") or []
    if not choices:
        raise ValueError("provider_empty_response")
    content = (choices[0].get("message") or {}).get("content") or ""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("provider_empty_response")
    return content.strip()[:9000]


# Built-in service map for the active specialist backends. Each service must
# have ULTIMA_AGENT_SHARED_TOKEN configured before it can accept agent requests.
_REMOTE_AGENTS = {
    "aurealis": "https://aurealis-omnia.onrender.com",
    "ionos7": "https://ionos-7-gauss-portal.onrender.com",
    "ionos_ki": "https://ionos-ki.onrender.com",
    "ultra_ki_pro": "https://quantum-ki-ultra-pro-v2-renewed.onrender.com",
    "quantum_ai": "https://quantum-ai-zeah.onrender.com",
    "ionos8": "https://ionos-8.onrender.com",
    "cat_chat": "https://quantum-ki-cat-chat.onrender.com",
    "quantumlight": "https://ai-quantumlight.onrender.com",
    "quantum": "https://quantum-singularity.onrender.com",
    "quantum_super": "https://quantum-super-intelligence.onrender.com",
    "ultra_ki": "https://ultraki-ai.onrender.com",
    "ultra_ki_v2": "https://ultra-ki-v2.onrender.com",
    "ki_game_mod": "https://ki-game-mod.onrender.com",
    "note_ki": "https://note-ki.onrender.com",
    "galactic": "https://galactic-ai-v3.onrender.com",
    "ultra_ki_merge": "https://ionos-ai.onrender.com",
    "ate_rea_characterverse": "https://ate-rea-characterverse.onrender.com",
    "aurealis_shopping": "https://aurealis-shopping-ai.onrender.com",
    "quantum_mirror": "https://quantum-mirror-wonderland.onrender.com",
    "rea_signature": "https://rea-signature.onrender.com",
}


def _agent_call(agent, goal, api_key, endpoint, model):
    base = _REMOTE_AGENTS.get(str(agent.get("id") or ""))
    if not base:
        return _provider_call(
            str(agent.get("name") or agent["id"]),
            str(agent.get("persona") or agent.get("domain") or ""),
            goal, api_key, endpoint, model
        )
    token = os.getenv("ULTIMA_AGENT_SHARED_TOKEN", "").strip()
    if not token:
        raise ValueError("agent_shared_token_not_configured")
    req = Request(
        base + "/api/agent/analyze",
        data=json.dumps({"task": goal}, ensure_ascii=False).encode("utf-8"),
        headers={"X-ULTIMA-AGENT-TOKEN": token, "Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req, timeout=45) as response:
        result = json.loads(response.read().decode("utf-8"))
    answer = result.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("remote_agent_empty_response")
    return answer.strip()[:9000]



def register_routes(bp, registry):
    from .agent_control import register_control_routes
    register_control_routes(bp)

    @bp.get("/api/agent-network/status")
    def agent_network_status():
        configured = bool(os.getenv("OPENAI_API_KEY", "").strip())
        return jsonify(
            coordinator="ULTIMA",
            mode="approval_required",
            collaboration_endpoint="/ultima-ai/api/collaborate",
            provider_configured=configured,
            registered_agents=len(registry),
            remote_agent_services=sorted(_REMOTE_AGENTS.keys()),
            execution="analysis_only",
            persistent_memory=__import__("ultima_ai.agent_store", fromlist=["persistent_storage"]).persistent_storage(),
            task_history=True,
            approval_queue=True,
            authenticated_agent_message_bus=True,
            hardware_control=False,
            note="Agenten können gemeinsam analysieren. Codeänderungen, GitHub-Schreibzugriffe, Deployments, Zahlungen und Hardwaresteuerung sind getrennte, freigabepflichtige Integrationen."
        )


    @bp.get("/api/agent-network/health")
    def agent_network_health():
        token = os.getenv("ULTIMA_AGENT_SHARED_TOKEN", "").strip()
        if not token:
            return jsonify(ok=False, error="ULTIMA_AGENT_SHARED_TOKEN_not_configured",
                           agents=[{"id": key, "status": "not_configured"} for key in _REMOTE_AGENTS]), 503
        checks = []
        for agent_id, base in _REMOTE_AGENTS.items():
            try:
                req = Request(base + "/api/agent/health",
                              headers={"X-ULTIMA-AGENT-TOKEN": token}, method="GET")
                with urlopen(req, timeout=8) as response:
                    data = json.loads(response.read().decode("utf-8"))
                checks.append({"id": agent_id, "status": "ready" if data.get("status") == "ready" else "degraded",
                               "service": base, "agent": data.get("name")})
            except Exception:
                checks.append({"id": agent_id, "status": "unreachable", "service": base})
        ready = sum(1 for item in checks if item["status"] == "ready")
        return jsonify(ok=ready == len(checks), ready=ready, total=len(checks), agents=checks), 200

    @bp.post("/api/collaborate")
    def collaborate():
        ip = (request.headers.get("X-Forwarded-For") or request.remote_addr or "unknown").split(",")[0].strip()
        now = time()
        recent = [stamp for stamp in _hits.get(ip, []) if now - stamp < 60]
        if len(recent) >= 5:
            return jsonify(error="Zu viele Team-Anfragen. Bitte eine Minute warten."), 429
        recent.append(now)
        _hits[ip] = recent

        data = request.get_json(silent=True) or {}
        goal = str(data.get("goal") or "").strip()
        if not goal:
            return jsonify(error="Bitte einen Entwicklungsauftrag oder ein Problem eingeben."), 400
        if len(goal) > 6000:
            return jsonify(error="Der Auftrag ist zu lang (maximal 6.000 Zeichen)."), 413

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return jsonify(error="OPENAI_API_KEY ist für die ULTIMA-Agentenkoordination nicht konfiguriert.", code="provider_not_configured"), 503

        chosen = _selected_agents(registry, data.get("agents"))
        endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        contributions, failures = [], []

        with ThreadPoolExecutor(max_workers=min(4, len(chosen))) as pool:
            futures = {
                pool.submit(_agent_call, agent, goal, api_key, endpoint, model): agent
                for agent in chosen
            }
            for future in as_completed(futures):
                agent = futures[future]
                try:
                    contributions.append({
                        "agent_id": agent["id"],
                        "agent": agent.get("name", agent["id"]),
                        "domain": agent.get("domain", ""),
                        "analysis": future.result()
                    })
                except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
                    failures.append({"agent_id": agent["id"], "agent": agent.get("name", agent["id"]), "status": "unavailable"})

        if not contributions:
            return jsonify(error="Keiner der ausgewählten Agenten konnte eine Analyse liefern.", failed_agents=failures), 502

        combined = "\n\n".join(
            "[" + item["agent"] + "]\n" + item["analysis"] for item in contributions
        )
        synthesis = (
            "Fasse die Fachbeiträge des ULTIMA-Agententeams zu einem gemeinsamen, widerspruchsbewussten Ergebnis zusammen. "
            "Trenne gesicherte Befunde, Annahmen, offene Fragen und nächste Tests. "
            "Erstelle einen priorisierten Umsetzungsplan. Es wurden keine Änderungen ausgeführt. "
            "Alle Code-, GitHub-, Deployment-, Finanz- und Hardwareaktionen bleiben bis zur ausdrücklichen Freigabe gesperrt.\n\n"
            "AUFTRAG:\n" + goal + "\n\nFACHBEITRÄGE:\n" + combined
        )
        try:
            final = _provider_call(
                "ULTIMA Koordination",
                "Du bist die zentrale, nüchterne Projektleitung. Erhalte unterschiedliche Perspektiven und erfinde keine Ausführung.",
                synthesis, api_key, endpoint, model, timeout=50
            )
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
            final = "Die Fachbeiträge liegen vor. Eine zusätzliche Zusammenführung durch ULTIMA war nicht verfügbar. Bitte lies die Einzelbeiträge."

        result = {
            "coordinator": "ULTIMA",
            "mode": "collaborative_analysis",
            "approval_required_for_actions": True,
            "executed_actions": [],
            "agents": contributions,
            "unavailable_agents": failures,
            "synthesis": final,
            "next_step": "Ergebnis prüfen und konkrete Änderungen separat freigeben."
        }
        task_id = None
        persistent = False
        try:
            from . import agent_store
            task = agent_store.create_task(goal, result)
            task_id = task["id"]
            persistent = agent_store.persistent_storage()
        except Exception:
            # Analysis remains available if the optional task store is not configured.
            pass

        return jsonify(
            ok=True,
            **result,
            task_id=task_id,
            persistent_memory=persistent,
            storage_note=("PostgreSQL persistent" if persistent else
                          "SQLite fallback; Render-Dateisystem kann flüchtig sein")
        ), 200
