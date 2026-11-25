"""Persistent task, approval and inter-agent message store for ULTIMA.

Use ULTIMA_AGENT_DATABASE_URL (PostgreSQL) in production. SQLite is a local
fallback for development; ephemeral Render filesystems are not durable.
"""
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone


def _connect():
    dsn = (os.getenv("ULTIMA_AGENT_DATABASE_URL") or os.getenv("DATABASE_URL") or "").strip()
    if dsn.startswith(("postgres://", "postgresql://")):
        import psycopg
        return psycopg.connect(dsn), "postgres"
    path = os.getenv("ULTIMA_AGENT_DB", "/tmp/ultima-agent-network.sqlite3")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    return sqlite3.connect(path), "sqlite"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _execute(conn, dialect, sql, params=()):
    return conn.execute(sql.replace("?", "%s") if dialect == "postgres" else sql, params)


def init_store():
    conn, dialect = _connect()
    try:
        _execute(conn, dialect, """CREATE TABLE IF NOT EXISTS agent_tasks (
            id TEXT PRIMARY KEY, goal TEXT NOT NULL, status TEXT NOT NULL,
            result_json TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        )""")
        _execute(conn, dialect, """CREATE TABLE IF NOT EXISTS agent_approvals (
            id TEXT PRIMARY KEY, task_id TEXT, action TEXT NOT NULL, details_json TEXT NOT NULL,
            status TEXT NOT NULL, decision_note TEXT NOT NULL, created_at TEXT NOT NULL,
            decided_at TEXT NOT NULL
        )""")
        _execute(conn, dialect, """CREATE TABLE IF NOT EXISTS agent_messages (
            id TEXT PRIMARY KEY, sender TEXT NOT NULL, recipient TEXT NOT NULL,
            task_id TEXT, payload_json TEXT NOT NULL, created_at TEXT NOT NULL
        )""")
        conn.commit()
    finally:
        conn.close()


def persistent_storage():
    dsn = (os.getenv("ULTIMA_AGENT_DATABASE_URL") or os.getenv("DATABASE_URL") or "").strip()
    return dsn.startswith(("postgres://", "postgresql://"))


def create_task(goal, result):
    init_store()
    conn, dialect = _connect()
    task_id, now = str(uuid.uuid4()), _now()
    try:
        _execute(conn, dialect, "INSERT INTO agent_tasks VALUES (?, ?, ?, ?, ?, ?)",
                 (task_id, goal, "completed_analysis", json.dumps(result, ensure_ascii=False), now, now))
        conn.commit()
        return {"id": task_id, "goal": goal, "status": "completed_analysis", "result": result,
                "created_at": now, "updated_at": now}
    finally:
        conn.close()


def list_tasks(limit=30):
    init_store()
    conn, dialect = _connect()
    try:
        cur = _execute(conn, dialect, "SELECT id, goal, status, result_json, created_at, updated_at FROM agent_tasks ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [{"id": r[0], "goal": r[1], "status": r[2], "result": json.loads(r[3]),
                 "created_at": r[4], "updated_at": r[5]} for r in rows]
    finally:
        conn.close()


def create_approval(task_id, action, details):
    init_store()
    conn, dialect = _connect()
    approval_id, now = str(uuid.uuid4()), _now()
    try:
        _execute(conn, dialect, "INSERT INTO agent_approvals VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (approval_id, task_id, action, json.dumps(details, ensure_ascii=False),
                  "pending", "", now, ""))
        conn.commit()
        return {"id": approval_id, "task_id": task_id, "action": action, "details": details,
                "status": "pending", "created_at": now}
    finally:
        conn.close()


def list_approvals(limit=50):
    init_store()
    conn, dialect = _connect()
    try:
        cur = _execute(conn, dialect, "SELECT id, task_id, action, details_json, status, decision_note, created_at, decided_at FROM agent_approvals ORDER BY created_at DESC LIMIT ?", (limit,))
        return [{"id": r[0], "task_id": r[1], "action": r[2], "details": json.loads(r[3]),
                 "status": r[4], "decision_note": r[5], "created_at": r[6], "decided_at": r[7]}
                for r in cur.fetchall()]
    finally:
        conn.close()


def decide_approval(approval_id, decision, note=""):
    if decision not in ("approved", "rejected"):
        raise ValueError("decision_must_be_approved_or_rejected")
    init_store()
    conn, dialect = _connect()
    now = _now()
    try:
        cur = _execute(conn, dialect,
            "UPDATE agent_approvals SET status = ?, decision_note = ?, decided_at = ? WHERE id = ? AND status = 'pending'",
            (decision, str(note)[:1000], now, approval_id))
        conn.commit()
        return cur.rowcount == 1
    finally:
        conn.close()


def add_message(sender, recipient, payload, task_id=None):
    init_store()
    conn, dialect = _connect()
    message_id, now = str(uuid.uuid4()), _now()
    try:
        _execute(conn, dialect, "INSERT INTO agent_messages VALUES (?, ?, ?, ?, ?, ?)",
                 (message_id, sender, recipient, task_id, json.dumps(payload, ensure_ascii=False), now))
        conn.commit()
        return {"id": message_id, "sender": sender, "recipient": recipient,
                "task_id": task_id, "payload": payload, "created_at": now}
    finally:
        conn.close()


def list_messages(recipient, limit=50):
    init_store()
    conn, dialect = _connect()
    try:
        cur = _execute(conn, dialect,
            "SELECT id, sender, recipient, task_id, payload_json, created_at FROM agent_messages WHERE recipient = ? ORDER BY created_at DESC LIMIT ?",
            (recipient, limit))
        return [{"id": r[0], "sender": r[1], "recipient": r[2], "task_id": r[3],
                 "payload": json.loads(r[4]), "created_at": r[5]} for r in cur.fetchall()]
    finally:
        conn.close()
