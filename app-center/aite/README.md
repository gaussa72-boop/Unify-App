# AITE local-first assistant and installer

AITE's chat interface is self-contained in `aite.js` (styles are embedded). Each website now has a repository-local copy under `static/aite/aite.js` (Express public sites use `public/aite/aite.js`). This prevents the widget itself from depending on the App Center CDN.

## Local model tiers
The setup scripts select a Qwen3.5 model based on installed system RAM:
- 8–15 GB: `qwen3.5:4b` (about 3.3 GB download)
- 16–31 GB: `qwen3.5:9b` (about 6.6 GB)
- 32 GB+: `qwen3.5:27b` (about 17 GB)

The model files and memory requirements vary by quantization and context length. Choose the largest tier that leaves memory for the OS and other applications. Ollama's official library lists these variants and sizes: https://ollama.com/library/qwen3.5

## One-time local AI setup
Install Ollama on the device. Windows: run `start-aite-windows.ps1` in PowerShell. macOS: run `start-aite-macos.command`. The script pulls a model selected for available RAM and starts the bridge. Manual setup:
```bash
ollama pull qwen3.5:4b
ollama serve
python3 local_bridge.py
```
The bridge listens only on 127.0.0.1:8765 and forwards to Ollama at 127.0.0.1:11434. It allows HTTPS origins ending in `.onrender.com` by default. Add other domains explicitly with `AITE_ALLOWED_ORIGINS`.

## Embed locally
```html
<script>window.AITE_CONFIG={persona:"compass",localModel:"qwen3.5:4b"};</script>
<script src="/static/aite/aite.js" defer></script>
```
For Express apps serving a `public` folder, use `/aite/aite.js` and place the file in `public/aite/`.

## Offline behavior
The page and local AITE script must have been loaded at least once and cached by the browser. The local model must already be downloaded and Ollama plus this bridge must be running on the same device. Then inference runs without internet and without OpenAI credits. A remote Render service cannot start a model on a visitor's computer.

If the bridge/model is not running, the UI still offers a short rule-based reflection fallback. That fallback is not a generative model. Model quality and speed depend on device hardware. Current Ollama for macOS requires macOS 14 Sonoma or later; older systems cannot run this installer reliably: https://ollama.com/download/mac

OpenAI remains optional. Configure `window.AITE_CONFIG.openAIRequest` through a protected server endpoint only. Never expose API keys in browser JavaScript.
