# AITE local-first assistant and installer

AITE's chat interface is self-contained in `aite.js` (styles are embedded). For each website, copy it into `static/aite/aite.js` and reference that local copy. This avoids relying on the App Center CDN for the widget itself.

## One-time local AI setup
Install Ollama on the device, then:
```bash
ollama pull qwen2.5:3b
ollama serve
python3 local_bridge.py
```
Windows: run `start-aite-windows.ps1`. macOS: run `start-aite-macos.command`. The bridge is loopback-only on 127.0.0.1:8765 and forwards requests to Ollama at 127.0.0.1:11434. It allows HTTPS origins ending in `.onrender.com` by default. Other domains must be explicitly added to `AITE_ALLOWED_ORIGINS`.

## Embed locally
```html
<script>window.AITE_CONFIG={persona:"compass",localModel:"qwen2.5:3b"};</script>
<script src="/static/aite/aite.js" defer></script>
```
For Flask sites this path is served by Flask's default static folder. Static sites can serve the same path from a repository `static/aite` folder.

## Honest offline behavior
The page and local AITE script must have been loaded at least once and cached by the browser. The local model must already be downloaded and Ollama plus the bridge must be running on the same device. Then model inference runs without internet and without OpenAI credits. A remote Render server cannot start a model on a visitor's computer.

If the bridge/model is not running, the UI still offers a short rule-based reflection fallback. That fallback is not a generative model. Qwen 2.5 3B is compact; response quality and speed depend on local hardware. Older Macs may not support current Ollama releases.

OpenAI remains optional. Configure `window.AITE_CONFIG.openAIRequest` through a protected server endpoint only. Never expose API keys in browser JavaScript.
