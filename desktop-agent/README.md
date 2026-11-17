# ULTIMA AI — macOS Local Companion (safe bootstrap)

This first local build is a deliberately small, localhost-only companion for macOS Catalina and newer.

## Requirements
- macOS
- Python 3.8 or newer available as `python3`
- A browser on the same Mac

## Install
1. Download this repository (or the `desktop-agent` folder) to the Mac.
2. Open Terminal and run:
   ```bash
   cd path/to/Unify-App/desktop-agent
   chmod +x install.sh uninstall.sh
   ./install.sh
   ```
3. Open `http://127.0.0.1:8765` on the Mac.
4. Read the local access token from:
   ```bash
   cat "$HOME/Library/Application Support/UltimaAI/local.token"
   ```
5. Paste the token into the local page and test the status command.

The installer creates a macOS LaunchAgent with RunAtLoad and KeepAlive. It does not run before the user logs in. To stop/remove autostart, run `./uninstall.sh`. The token and logs are retained by that script.

## Safe-mode boundaries
- Binds only to `127.0.0.1:8765`; it is not reachable from the LAN or internet.
- Uses a random local token stored with owner-only permissions.
- Supports only status checks and opening HTTPS URLs on a short allowlist.
- Does not execute shell commands, arbitrary programs, file writes, email sends, payments, or account changes.
- No remote-control or phone-to-Mac relay is implemented yet.
- Voice input is optional browser speech recognition and requires the user's microphone permission.

## Important
This is a bootstrap prototype, not a full Copilot replacement. Keep the token private. Do not commit local token files, logs, or credentials. The next stage is a reviewed permission broker with per-action approvals, audit history, revocation, and a separately authenticated remote relay before adding mobile access or broader computer control.
