# ULTIMA live specialist adapters

The ULTIMA coordinator can call these authenticated service adapters directly:
- `aurealis` → `https://aurealis-omnia.onrender.com`
- `ionos7` → `https://ionos-7-gauss-portal.onrender.com`
- `ionos_ki` → `https://ionos-ki.onrender.com`
- `ultra_ki_pro` → `https://quantum-ki-ultra-pro-v2-renewed.onrender.com`
- `quantum_ai` → `https://quantum-ai-zeah.onrender.com`

Each service exposes `GET /api/agent/health` and `POST /api/agent/analyze`. ULTIMA uses `ULTIMA_AGENT_SHARED_TOKEN` as an HTTP header and never sends that secret to browser clients. The health endpoint is `GET /ultima-ai/api/agent-network/health`.

The same high-entropy `ULTIMA_AGENT_SHARED_TOKEN` must be configured as a protected environment variable on ULTIMA and each listed service. Until then, health checks report not configured and remote calls are unavailable. This does not affect the ordinary ULTIMA chat. The endpoints are analysis-only; they cannot execute code, deploy, trade, sign wallet transactions or control mining hardware.
