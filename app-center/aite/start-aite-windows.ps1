$ErrorActionPreference = "Stop"
Write-Host "AITE Local AI setup - Windows" -ForegroundColor Cyan
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  if (Get-Command winget -ErrorAction SilentlyContinue) { winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements }
  else { throw "Bitte Ollama von https://ollama.com/download installieren und erneut starten." }
}
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python 3 wird benötigt." }
$ramGB = [math]::Floor((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
if ($ramGB -ge 32) { $model = "qwen3.5:27b" }
elseif ($ramGB -ge 16) { $model = "qwen3.5:9b" }
else { $model = "qwen3.5:4b" }
Write-Host "Erkannter Arbeitsspeicher: $ramGB GB. Modell: $model" -ForegroundColor Yellow
ollama pull $model
$env:AITE_MODEL = $model
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
Start-Process -WindowStyle Minimized -FilePath ollama -ArgumentList "serve"
Start-Sleep -Seconds 3
Write-Host "AITE Bridge läuft auf 127.0.0.1:8765. Dieses Fenster offen lassen." -ForegroundColor Green
if ($python -eq "py") { py -3 "$root\local_bridge.py" } else { python "$root\local_bridge.py" }
