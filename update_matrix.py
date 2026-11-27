"""ULTIMA Update Matrix: isolated, proposal-first update orchestration.

This module never executes generated code, never edits agent personas, and never
deploys automatically. It creates reviewable proposals for explicitly opted-in
agents. A human owner must approve and deploy each target service separately.
"""
from __future__ import annotations
import hashlib, hmac, json, os, sqlite3, time, urllib.request, urllib.error
from pathlib import Path
from flask import Blueprint, jsonify, request, session

bp = Blueprint("update_matrix", __name__)
ROOT = Path(__file__).resolve().parent
AGENTS_FILE = ROOT / "update_matrix_agents.json"
DB_PATH = Path(os.getenv("UPDATE_MATRIX_DB_PATH", "/tmp/ultima_update_matrix.sqlite3"))

def _agents():
    return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))

def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS proposals (
        id TEXT PRIMARY KEY, agent_id TEXT NOT NULL, target TEXT NOT NULL,
        title TEXT NOT NULL, summary TEXT NOT NULL, patch TEXT NOT NULL,
        tests TEXT NOT NULL, risk TEXT NOT NULL, status TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )""")
    conn.commit()
    return conn

def _authorized():
    expected = os.getenv("ULTIMA_UPDATE_MATRIX_TOKEN", "").strip()
    supplied = request.headers.get("Authorization", "")
    token = supplied[7:].strip() if supplied.startswith("Bearer ") else ""
    return bool(expected and token and hmac.compare_digest(expected, token))

@bp.before_request
def protect_matrix_api():
    if request.path.startswith("/api/update-matrix/") and not _authorized():
        return jsonify(error="update_matrix_auth_required"), 401

@bp.get("/api/update-matrix/status")
def status():
    agents = _agents()
    conn = _db()
    try:
        rows = conn.execute("SELECT status, COUNT(*) AS n FROM proposals GROUP BY status").fetchall()
    finally:
        conn.close()
    return jsonify(
        service="ULTIMA Update Matrix",
        mode="proposal_first",
        autonomous_code_deployment=False,
        llm_configured=bool(os.getenv("UPDATE_MATRIX_LLM_API_URL") and os.getenv("UPDATE_MATRIX_LLM_API_KEY")),
        agent_count=len(agents),
        opted_in_agents=[a["id"] for a in agents if a.get("enabled") is True],
        proposal_counts={r["status"]: r["n"] for r in rows},
        note="Generierte Vorschläge werden niemals selbstständig ausgeführt oder deployed."
    )

@bp.get("/api/update-matrix/agents")
def agents():
    return jsonify(agents=[
        {k:v for k,v in a.items() if k not in ("private_context",)}
        for a in _agents()
    ])

@bp.post("/api/update-matrix/proposals/generate")
def generate_proposal():
    body = request.get_json(silent=True) or {}
    agent_id = str(body.get("agent_id", "")).strip()
    task = str(body.get("task", "")).strip()[:4000]
    registry = {a["id"]:a for a in _agents()}
    agent = registry.get(agent_id)
    if not agent or not agent.get("enabled"):
        return jsonify(error="agent_not_enabled_or_unknown"), 404
    if not task:
        return jsonify(error="task_required"), 400
    api_url = os.getenv("UPDATE_MATRIX_LLM_API_URL", "").strip()
    api_key = os.getenv("UPDATE_MATRIX_LLM_API_KEY", "").strip()
    model = os.getenv("UPDATE_MATRIX_LLM_MODEL", "gpt-4.1-mini")
    if not api_url or not api_key:
        return jsonify(error="llm_provider_not_configured",
                       required_environment=["UPDATE_MATRIX_LLM_API_URL","UPDATE_MATRIX_LLM_API_KEY"],
                       message="Agent ist registriert; für KI-generierte Vorschläge fehlt noch die freigegebene Modell-API-Konfiguration."), 503
    policy_path = ROOT / "GAUSS72_GLOBAL_OPERATING_RULES.md"
    try:
        global_policy = policy_path.read_text(encoding="utf-8")[:24000]
    except OSError:
        global_policy = "Global operating rules unavailable: preserve target persona, never request or expose secrets, require human review, and do not perform financial or destructive actions."
    system = (
        "You are a scoped software-maintenance proposal agent for the gaussa72-boop / ULTIMA network. "
        "Apply the following global operating rules as mandatory constraints. The target-specific "
        "agent persona and system instructions remain authoritative for that target and must never "
        "be overwritten. Do not request secrets. Do not propose financial transfers, wallet signing, "
        "mining payout activation, destructive changes, or cross-service persona edits. "
        "Return ONLY JSON with keys title, summary, patch, tests, risk. patch must be a reviewable "
        "unified diff or concise file-change proposal, never an executable command. Mark unknown facts "
        "as unknown. Target: " + agent["target"] + ". Persona: " + agent["persona"] +
        "\\n\\nGLOBAL OPERATING RULES:\\n" + global_policy
    )
    payload = json.dumps({"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":task}],"temperature":0.2}).encode()
    req = urllib.request.Request(api_url, data=payload, headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        raw = data["choices"][0]["message"]["content"]
        if raw.startswith("```"):
            raw = raw.split("\n",1)[1].rsplit("```",1)[0]
        result = json.loads(raw)
        for key in ("title","summary","patch","tests","risk"):
            if not isinstance(result.get(key), str) or not result[key].strip():
                raise ValueError("missing_"+key)
    except (urllib.error.URLError, KeyError, ValueError, TypeError, json.JSONDecodeError):
        return jsonify(error="proposal_generation_failed", message="Der KI-Anbieter lieferte keine gültige, prüfbare Antwort."), 502
    proposal_id = hashlib.sha256((agent_id+str(time.time_ns())+result["title"]).encode()).hexdigest()[:20]
    conn = _db()
    try:
        conn.execute("INSERT INTO proposals VALUES (?,?,?,?,?,?,?,?,?,?)",
          (proposal_id,agent_id,agent["target"],result["title"][:180],result["summary"][:4000],
           result["patch"][:30000],result["tests"][:8000],result["risk"][:2000],"pending_review",int(time.time())))
        conn.commit()
    finally:
        conn.close()
    return jsonify(id=proposal_id,agent_id=agent_id,target=agent["target"],status="pending_review",
                   proposal=result,requires_human_review=True), 201

@bp.get("/api/update-matrix/proposals")
def list_proposals():
    conn = _db()
    try:
        rows = conn.execute("SELECT * FROM proposals ORDER BY created_at DESC LIMIT 100").fetchall()
    finally:
        conn.close()
    return jsonify(proposals=[dict(r) for r in rows])

@bp.post("/api/update-matrix/proposals/<proposal_id>/approve")
def approve_proposal(proposal_id):
    conn = _db()
    try:
        row = conn.execute("SELECT id,status FROM proposals WHERE id=?",(proposal_id,)).fetchone()
        if not row:
            return jsonify(error="proposal_not_found"), 404
        if row["status"] != "pending_review":
            return jsonify(error="proposal_not_pending_review",status=row["status"]), 409
        conn.execute("UPDATE proposals SET status='approved_for_manual_deployment' WHERE id=?",(proposal_id,))
        conn.commit()
    finally:
        conn.close()
    return jsonify(id=proposal_id,status="approved_for_manual_deployment",
                   note="Freigabe dokumentiert. Es wurde kein Code ausgeführt und kein Deployment gestartet."), 200
