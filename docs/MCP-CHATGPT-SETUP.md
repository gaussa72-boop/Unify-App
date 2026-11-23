# ULTIMA AI Universe — ChatGPT MCP connection

Endpoint: https://ultima-unify-45ne.onrender.com/mcp

## What is implemented

This is a stateless MCP JSON-RPC endpoint with bearer-token authentication. It exposes:
- `list_ai_agents`: ULTIMA agent directory and persona descriptions
- `list_ai_capabilities`: capability catalogue with implementation stages
- `list_render_projects`: the checked-in Render project inventory
- `get_provider_readiness`: provider configuration flags only; no secret values
- `chat_with_ultima_agent`: persona-based chat through the configured OpenAI-compatible provider
- `create_implementation_plan`: planning only; no writes or deployments

The gateway is deliberately read-only for infrastructure. It cannot execute shell commands, change Render services, edit GitHub repositories, publish content, send email, spend money, delete data, or change accounts.

## Configure the shared secret

1. Open the Render service `ultima-unify-45ne`: https://dashboard.render.com/web/srv-dbroeepsrm7s73emvtmg
2. Open Environment and add `ULTIMA_MCP_API_TOKEN`.
3. Generate a long random value locally, for example:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
4. Paste the generated value directly into Render. Do not put it in GitHub, a website, screenshots, or chat.
5. Save changes and wait until the deployment is Live.

The MCP endpoint returns HTTP 503 until this secret is configured, and HTTP 401 for missing or incorrect bearer tokens.

## Connect ChatGPT

In a ChatGPT workspace/account that supports custom remote MCP apps:
1. Open Settings → Apps (or Connectors) → Advanced / Developer mode.
2. Add a custom remote MCP server.
3. Server URL: `https://ultima-unify-45ne.onrender.com/mcp`
4. Authentication: Bearer token; use the value stored in Render as `ULTIMA_MCP_API_TOKEN`.
5. Save, connect, and test `list_ai_agents` and `list_render_projects`.

If the ChatGPT client available on the account does not offer bearer-token authentication for custom MCP servers, do not disable authentication. A separate OAuth 2.1 authorization-code + PKCE flow must be implemented first.

## Provider setup

The persona chat tool uses:
- `OPENAI_API_KEY` (required)
- `OPENAI_BASE_URL` (optional; defaults to OpenAI API)
- `OPENAI_MODEL` (optional; defaults to gpt-4o-mini)

Keep these values in Render Environment only. Model/provider usage may incur separate charges.

## Next integration milestones

1. Register each external AI service with a verified health URL and an authenticated, documented chat endpoint.
2. Add per-agent adapters with timeouts, rate limits, response-size limits, and provider-specific credentials.
3. Add persistent project memory with per-user access control, consent, export, and deletion.
4. Add GitHub read/PR workflows and Render monitoring tools; require explicit approval for every production write/deploy.
5. Add media, document, web-research, voice, translation, learning, community, commerce, premium-entitlement, and automation adapters one by one.
6. Add audit logs, revocation, quotas, abuse controls, and integration tests before expanding privileges.

A persona listed as active in the catalogue does not mean its separate Render service API has already been connected. Only verified adapters may be shown as connected.
