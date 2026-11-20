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
