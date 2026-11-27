# ULTIMA Update Matrix

## Implemented foundation
- Flask blueprint at `/api/update-matrix/*`, registered by `portal_server.py`.
- Four isolated crypto update-agent profiles with distinct domain/persona boundaries.
- Bearer-token protected API using `ULTIMA_UPDATE_MATRIX_TOKEN`.
- Optional OpenAI-compatible chat-completions endpoint configured only through environment variables:
  - `UPDATE_MATRIX_LLM_API_URL`
  - `UPDATE_MATRIX_LLM_API_KEY`
  - `UPDATE_MATRIX_LLM_MODEL` (optional)
- Generated proposals are stored in SQLite at `/tmp/ultima_update_matrix.sqlite3` by default. This is ephemeral on Render; durable storage is not claimed.
- Proposals are review-only. Approval records an approval state but never executes code or deploys.
- No service credentials, API keys, wallet keys, or seed phrases are stored in Git.

## API
- `GET /api/update-matrix/status`
- `GET /api/update-matrix/agents`
- `POST /api/update-matrix/proposals/generate` JSON: `{"agent_id":"omnia_mining","task":"Review block archive reliability" }`
- `GET /api/update-matrix/proposals`
- `POST /api/update-matrix/proposals/{id}/approve`

All endpoints require `Authorization: Bearer <ULTIMA_UPDATE_MATRIX_TOKEN>`.

## Safety and rollout
- Every agent is scoped to one target and has its own persona.
- Generated output is untrusted proposal text. It is never executed.
- No automatic GitHub writes, production changes, deployments, wallet signing, mining payout activation, or trading.
- Before enabling scheduled generation, configure the model API and token in Render environment settings. Do not put secrets in source control.
- The current SQLite location is temporary. Connect a persistent database before relying on proposal history.
- The ULTIMA Render deployment must be verified after the commit before this service can be called live.

## Global GAUSS72 operating standard (2026-11-27)
- The canonical cross-project policy is `GAUSS72_GLOBAL_OPERATING_RULES.md`.
- Every Update Matrix proposal agent receives this policy in its system context before generating a proposal.
- Scope: all compatible, owner-controlled or explicitly approved projects in both connected GitHub accounts and Render Primary, after per-target inventory and compatibility review.
- Distribution is staged and target-specific: inspect → propose/version → isolated tests/security review → owner approval where required → deploy → verify commit, deploy, logs, health and key functions → record status/rollback.
- No blind mass writes or deployments. Excluded integrations remain excluded unless a later instruction explicitly changes that specific integration. Update Matrix may track maintenance status without connecting excluded sites to shared identity, shared AI context or network data.
- Preserve each AI's personality, system prompt, design and product behavior. Shared Aurealis character profiles are optional and must not override target security/system rules.
- Copilot actions require server-side authorization and confirmation for sending, publishing, deleting, payments, role changes or external side effects. Private messages are not globally exposed; sharing requires an explicit user action.
- Cyber Shield follows layered defense; no absolute-security claim is permitted. Secrets remain in secret stores/Render environment settings and never enter Git, prompts, logs or cross-agent messages.
- Financial actions, mining payouts, wallet signing, transfers, trading, paid-resource changes and destructive operations are not executed by generated proposals.
