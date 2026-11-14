$ErrorActionPreference = "Stop"
Write-Host "AITE Local AI setup - Windows" -ForegroundColor Cyan
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
  } else {
    throw "Bitte Ollama von https://ollama.com/download installieren und dieses Skript erneut starten."
  }
}
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) {
  throw "Python 3 wird benötigt. Installiere Python 3 und starte das Skript erneut."
}
ollama pull qwen2.5:3b
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
Start-Process -WindowStyle Minimized -FilePath ollama -ArgumentList "serve"
Start-Sleep -Seconds 3
Write-Host "AITE Bridge wird gestartet. Dieses Fenster offen lassen." -ForegroundColor Green
if ($python -eq "py") { py -3 "$root\local_bridge.py" } else { python "$root\local_bridge.py" }
