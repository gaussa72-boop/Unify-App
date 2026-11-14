# AITE local-first assistant

This is a reusable, site-embeddable AITE assistant UI with a star-singularity visual treatment.

## Embed
Add before the closing body tag:
```html
<script>window.AITE_CONFIG={persona:"compass",ollamaModel:"qwen2.5:3b"};</script>
<script src="https://astralis-app-center.onrender.com/aite/aite.js" defer></script>
```

The widget has six spiritual/creative/technical reflection modes. It stores chat history in localStorage on the current device. The default Local/Offline mode tries Ollama at http://localhost:11434 using qwen2.5:3b. Install Ollama and download the model once on the user's own computer:
```bash
ollama pull qwen2.5:3b
ollama serve
```
The model then runs on the user's device and does not require OpenAI credits. Hardware requirements vary. Mobile browser support for local Ollama is limited. If Ollama is not available, a small built-in offline reflection fallback is used; this fallback is not a generative LLM.

OpenAI remains optional. A site may provide window.AITE_CONFIG.openAIRequest(text, history, context), implemented through its own protected server endpoint. Never put an OpenAI API key in browser JavaScript.

The online assistant is not configured automatically. Existing site-specific AI and spiritual features must be preserved and integrated individually. Do not overwrite payment, checkout, authentication or existing assistant flows.
