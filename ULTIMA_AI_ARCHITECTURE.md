# ULTIMA AI — Architecture

## Implemented foundation
- Isolated Flask blueprint mounted at /ultima-ai.
- Agent registry preserving distinct roles/personas.
- OpenAI-compatible chat provider configured only through Render environment variables.
- Capability roadmap with explicit maturity labels.
- Planning endpoint with production approval gates.
- Browser voice input/output where supported.
- Rate-limited chat endpoint and bounded input sizes.

## Configuration
Set OPENAI_API_KEY in Render. Optional: OPENAI_BASE_URL and OPENAI_MODEL. Never commit secrets.

## Autonomy and security
This first release can chat and plan. It does not execute shell commands, arbitrary code, payments, account changes, public posts, destructive operations, or production deployments from chat. GitHub and Render write actions must be added as scoped integrations with audit logs, allowlists, per-action approval, and rollback. Project-specific assistants remain independent.

## Roadmap
1. Persistent PostgreSQL project memory and vector retrieval.
2. OAuth-scoped GitHub and Render read-only connectors.
3. Isolated build/test runners and signed artifacts.
4. Permissioned write tools with approval workflows.
5. Multi-agent delegation, task queue, observability and kill switch.
6. Multimodal providers, mobile companion and plugin SDK.
7. Experimental research sandbox for classical quantum-circuit simulation.

## Maturity
Available = implemented in this release; Prototype = partial foundation; Planned = not yet integrated; Experimental = isolated research concept.


## Multi-agent collaboration (implemented on feature branch)
- ULTIMA exposes `GET /ultima-ai/api/agent-network/status` and `POST /ultima-ai/api/collaborate`.
- Up to four registered specialist personas analyse one task concurrently through the configured OpenAI-compatible provider; ULTIMA then synthesizes their contributions.
- The ULTIMA AI page includes an **Agententeam** action.
- This is collaborative analysis, not autonomous code execution. The endpoint does not access GitHub, Render, wallets, mining hardware, payment systems, or user devices.
- Production writes, commits to protected branches, merges, deployments, financial actions and hardware control remain separate, explicitly approved integrations.
- The endpoint is stateless. Persistent shared memory and durable task history require a configured persistent database and retention/deletion policy.
- Tests: `python -m unittest discover -s tests`.
