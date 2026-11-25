# ULTIMA multi-agent integration contract

## Architecture
ULTIMA is the coordinator. Specialist agents retain their own persona and domain. The coordinator may request parallel analysis and combine results. The message bus provides authenticated service-to-service inbox/outbox semantics; task history and approval decisions are recorded separately.

## Runtime configuration
- `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` and `OPENAI_MODEL`: model-provider access for analysis.
- `ULTIMA_AGENT_SHARED_TOKEN`: random secret shared only with trusted agent services for the message bus. Send it as `X-ULTIMA-AGENT-TOKEN`; never expose it in browser code.
- `ULTIMA_AGENT_ADMIN_TOKEN`: separate random secret for the operator-only task and approval endpoints. Send it as `X-ULTIMA-ADMIN-TOKEN`.
- `ULTIMA_AGENT_DATABASE_URL`: PostgreSQL connection string for durable production storage. If absent, `ULTIMA_AGENT_DB` selects a SQLite fallback; Render's ordinary filesystem is ephemeral, so SQLite is not a production long-term memory store unless it is placed on a persistent disk.

## API
- `GET /ultima-ai/api/agent-network/status`: capabilities and configuration status.
- `POST /ultima-ai/api/collaborate`: parallel specialist analysis and ULTIMA synthesis. Analysis only; it does not run code or change external systems.
- `GET /ultima-ai/api/tasks`: operator-only task history.
- `GET /ultima-ai/api/approvals`: operator-only approval queue.
- `POST /ultima-ai/api/approvals/{id}/decision`: approve or reject a queued action; this records the decision and does not itself execute a deployment or financial action.
- `POST /ultima-ai/api/agent/messages`: authenticated agent-to-agent message.
- `GET /ultima-ai/api/agent/messages/{recipient}`: authenticated recipient inbox.

## Safety boundaries
All cross-service writes, GitHub mutations, production deploys, wallet signing, payouts, trading and mining-hardware control require a separate reviewed adapter and an explicit approval. The Bitcoin module is a read-only observer unless a separately secured mining gateway is configured. Blockchain observation is not mining and does not earn block rewards.

## Rollout status
This contract is the central ULTIMA integration layer. Each individual AI repository still needs its own small authenticated adapter and service URL/secret configuration before it can exchange live messages. Never report all agents as connected until a health handshake from each service succeeds.
