$ErrorActionPreference = "Stop"
Write-Host "AITE Local AI setup - Windows" -ForegroundColor Cyan
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  if (Get-Command winget -ErrorAction SilentlyContinue) { winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements }
  else { throw "Bitte Ollama von https://ollama.com/download installieren und erneut starten." }
}
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python 3 wird benötigt." }
$ramGB = [math]::Floor((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
if ($ramGB -ge 128) { $model = "qwen3.5:122b" }
elseif ($ramGB -ge 64) { $model = "qwen3.5:35b" }
elseif ($ramGB -ge 32) { $model = "qwen3.5:27b" }
elseif ($ramGB -ge 16) { $model = "qwen3.5:9b" }
elseif ($ramGB -ge 8) { $model = "qwen3.5:4b" }
else { $model = "qwen3.5:2b" }
Write-Host "Erkannter Arbeitsspeicher: $ramGB GB. Modell: $model" -ForegroundColor Yellow
ollama pull $model
$env:AITE_MODEL = $model
$env:AITE_ALLOWED_ORIGINS = "https://aurealis-cyber-shield.onrender.com,https://technologisierte-einheit.onrender.com,https://ate-rea-characterverse.onrender.com,https://aurelis-creative-ai-studio.onrender.com,https://ultima-central-45ne.onrender.com,https://ultima-unify-45ne.onrender.com,https://lichtkrieger-dark-mirror-realms.onrender.com,https://lichtkrieger-cloud-gaming.onrender.com,https://ultima-membership-api.onrender.com,https://astralis-omega.onrender.com,https://novatube-a10l.onrender.com,https://ate-rea-vermachtnis.onrender.com,https://dropshift-store.onrender.com,https://quantum-ai-zeah.onrender.com,https://ki-game-mod.onrender.com,https://note-ki.onrender.com,https://ipad-app-ionos-7.onrender.com,https://galactic-ai-v3.onrender.com,https://quantum-super-intelligence.onrender.com,https://ionos-8.onrender.com,https://quantum-ki-cat-chat.onrender.com,https://ai-quantumlight.onrender.com,https://quantenformel.onrender.com,https://quantum-singularity.onrender.com,https://ionos-ai.onrender.com,https://rea-signature.onrender.com,https://quantum-ai-renewed.onrender.com,https://quantum-ki-ultra-pro-v2-renewed.onrender.com,https://bullrun-apparel.onrender.com,https://quantum-mirror-wonderland.onrender.com,https://ionos-ki.onrender.com,https://ionos-7.onrender.com,https://ultraki-ai.onrender.com,https://ultra-ki-v2.onrender.com,https://quantum-ki-ultra-pro-v2.onrender.com,https://quantumai-chat.onrender.com,https://trinity-trading-k03l.onrender.com,https://aktiv-lyca-rgds.onrender.com,https://royal-palace-4r57.onrender.com,https://business-real-estate-membership-wswk.onrender.com,https://sneaker-store-bow5.onrender.com,https://webshop-parfum-90dl.onrender.com,https://aktiv-lyca-rnmc.onrender.com,https://astralis-app-center.onrender.com,https://sneaker-store-27cn.onrender.com,https://aktiv-lyca-standalone.onrender.com,https://drop-shipping-store.onrender.com,https://autokrypt-boerse.onrender.com,https://ate-rea-library.onrender.com,https://lichtkrieger-hub.onrender.com,https://omega-aurealis.onrender.com,https://quantum-mirror-wonderland-vibh.onrender.com,https://galactic-ai-v3-app.onrender.com,https://quantum-singularity-8liw.onrender.com,https://quantum-ki-cat-chat-2t79.onrender.com,https://ai-quantumlight-k84q.onrender.com,https://ionos-8-platform.onrender.com,https://ultraki-ai-app.onrender.com,https://ultra-ki-v2-app.onrender.com,https://quantum-ki-ultra-pro-v2-9pvf.onrender.com,https://quantum-ai-app.onrender.com,https://quantum-k-app.onrender.com,https://ultima-central-bt56.onrender.com,https://ultima-central-5zeh.onrender.com,https://ultima-central-r88g.onrender.com,https://novatube-studio-vli0.onrender.com,https://ionos-ki-v2-1oki.onrender.com"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
if (-not (Test-NetConnection 127.0.0.1 -Port 11434 -InformationLevel Quiet)) {
  Start-Process -WindowStyle Minimized -FilePath ollama -ArgumentList "serve"
  Start-Sleep -Seconds 5
}
Write-Host "AITE Bridge läuft auf 127.0.0.1:8765. Dieses Fenster offen lassen." -ForegroundColor Green
if ($python -eq "py") { py -3 "$root\local_bridge.py" } else { python "$root\local_bridge.py" }
