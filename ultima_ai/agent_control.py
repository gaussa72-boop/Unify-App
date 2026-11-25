"""ULTIMA approval-gated task history and agent message bus routes."""
import hmac
import os
from flask import jsonify, request
from . import agent_store


def register_control_routes(bp):
    def authorized():
        expected = os.getenv("ULTIMA_AGENT_ADMIN_TOKEN", "").strip()
        supplied = request.headers.get("X-ULTIMA-ADMIN-TOKEN", "").strip()
        return bool(expected and supplied and hmac.compare_digest(expected, supplied))

    @bp.get("/api/tasks")
    def agent_tasks():
        if not authorized():
            return jsonify(error="admin_authorization_required"), 401
        try:
            return jsonify(tasks=agent_store.list_tasks(), persistent=agent_store.persistent_storage())
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503

    @bp.get("/api/approvals")
    def agent_approvals():
        if not authorized():
            return jsonify(error="admin_authorization_required"), 401
        try:
            return jsonify(approvals=agent_store.list_approvals(), persistent=agent_store.persistent_storage())
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503

    @bp.post("/api/approvals")
    def agent_approval_create():
        if not authorized():
            return jsonify(error="admin_authorization_required"), 401
        data = request.get_json(silent=True) or {}
        action = str(data.get("action") or "").strip()[:120]
        details = data.get("details")
        if not action or not isinstance(details, dict):
            return jsonify(error="action_and_object_details_required"), 400
        if len(str(details)) > 12000:
            return jsonify(error="details_too_large"), 413
        try:
            approval = agent_store.create_approval(
                str(data.get("task_id") or "")[:80] or None, action, details
            )
            return jsonify(ok=True, approval=approval), 201
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503

    @bp.post("/api/approvals/<approval_id>/decision")
    def agent_approval_decision(approval_id):
        if not authorized():
            return jsonify(error="admin_authorization_required"), 401
        data = request.get_json(silent=True) or {}
        decision = str(data.get("decision", ""))
        note = str(data.get("note", ""))[:1000]
        try:
            changed = agent_store.decide_approval(approval_id, decision, note)
        except ValueError:
            return jsonify(error="decision_must_be_approved_or_rejected"), 400
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503
        if not changed:
            return jsonify(error="approval_not_found_or_already_decided"), 409
        return jsonify(ok=True, approval_id=approval_id, status=decision)

    @bp.post("/api/agent/messages")
    def agent_message_send():
        token = os.getenv("ULTIMA_AGENT_SHARED_TOKEN", "").strip()
        supplied = request.headers.get("X-ULTIMA-AGENT-TOKEN", "").strip()
        if not token or not supplied or not hmac.compare_digest(token, supplied):
            return jsonify(error="agent_authentication_required"), 401
        data = request.get_json(silent=True) or {}
        sender = str(data.get("sender", "")).strip()[:80]
        recipient = str(data.get("recipient", "")).strip()[:80]
        payload = data.get("payload")
        if not sender or not recipient or not isinstance(payload, dict):
            return jsonify(error="sender_recipient_and_object_payload_required"), 400
        if len(str(payload)) > 12000:
            return jsonify(error="payload_too_large"), 413
        try:
            message = agent_store.add_message(sender, recipient, payload, str(data.get("task_id") or "")[:80] or None)
            return jsonify(ok=True, message=message), 201
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503

    @bp.get("/api/agent/messages/<recipient>")
    def agent_message_inbox(recipient):
        token = os.getenv("ULTIMA_AGENT_SHARED_TOKEN", "").strip()
        supplied = request.headers.get("X-ULTIMA-AGENT-TOKEN", "").strip()
        if not token or not supplied or not hmac.compare_digest(token, supplied):
            return jsonify(error="agent_authentication_required"), 401
        try:
            return jsonify(messages=agent_store.list_messages(recipient[:80]))
        except Exception:
            return jsonify(error="agent_store_unavailable"), 503
