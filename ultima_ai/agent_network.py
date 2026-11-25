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
    defaults = ["aurealis", "ionos7", "neuroforge", "guardian"]
    ids = requested if isinstance(requested, list) else defaults
    chosen, seen = [], set()
    for raw in ids[:4]:
        key = str(raw)[:80]
        if key in by_id and key not in seen:
            chosen.append(by_id[key])
            seen.add(key)
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


def register_routes(bp, registry):
    @bp.get("/api/agent-network/status")
    def agent_network_status():
        configured = bool(os.getenv("OPENAI_API_KEY", "").strip())
        return jsonify(
            coordinator="ULTIMA",
            mode="approval_required",
            collaboration_endpoint="/ultima-ai/api/collaborate",
            provider_configured=configured,
            registered_agents=len(registry),
            execution="analysis_only",
            persistent_memory=False,
            hardware_control=False,
            note="Agenten können gemeinsam analysieren. Codeänderungen, GitHub-Schreibzugriffe, Deployments, Zahlungen und Hardwaresteuerung sind getrennte, freigabepflichtige Integrationen."
        )

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
                pool.submit(
                    _provider_call,
                    str(agent.get("name") or agent["id"]),
                    str(agent.get("persona") or agent.get("domain") or ""),
                    goal, api_key, endpoint, model
                ): agent for agent in chosen
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

        return jsonify(
            ok=True,
            coordinator="ULTIMA",
            mode="collaborative_analysis",
            approval_required_for_actions=True,
            executed_actions=[],
            persistent_memory=False,
            agents=contributions,
            unavailable_agents=failures,
            synthesis=final,
            next_step="Ergebnis prüfen und konkrete Änderungen separat freigeben."
        ), 200
