#!/usr/bin/env python3
"""Monthly, read-only scan of tracked AI projects and selected AI tooling releases.

This scanner deliberately does not modify application code, dependency pins,
production settings, secrets, databases, or deployments. It writes a dated
report and latest.json for review in the ULTIMA Updates dashboard.
"""
from __future__ import annotations
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "update-registry.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "updates"
API = "https://api.github.com"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

def github_json(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ULTIMA-Monthly-Update-Scanner"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(f"{API}{path}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"_error": str(exc)}

def inspect_repo(item: dict, source_type: str):
    full_name = item["repository"]
    release = github_json(f"/repos/{full_name}/releases/latest")
    repo = github_json(f"/repos/{full_name}")
    default_branch = repo.get("default_branch", "main") if isinstance(repo, dict) else "main"
    commit = github_json(f"/repos/{full_name}/commits/{default_branch}")
    return {
        "name": item.get("name", full_name),
        "repository": full_name,
        "type": source_type,
        "default_branch": default_branch,
        "latest_release": release.get("tag_name") if isinstance(release, dict) else None,
        "release_url": release.get("html_url") if isinstance(release, dict) else None,
        "release_published_at": release.get("published_at") if isinstance(release, dict) else None,
        "latest_commit": (commit.get("sha") or "")[:12] if isinstance(commit, dict) else None,
        "latest_commit_url": commit.get("html_url") if isinstance(commit, dict) else None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "error": next((x.get("_error") for x in (release, repo, commit) if isinstance(x, dict) and x.get("_error")), None),
    }

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checked_at = datetime.now(timezone.utc).isoformat()
    projects = [inspect_repo(p, "project") for p in REGISTRY["projects"]]
    innovations = [inspect_repo(p, "innovation-source") for p in REGISTRY["innovation_sources"]]
    report = {
        "generated_at": checked_at,
        "schedule": REGISTRY.get("schedule", "monthly"),
        "timezone": REGISTRY.get("timezone", "Europe/Berlin"),
        "projects": projects,
        "innovation_sources": innovations,
        "policy": {
            "mode": "review-before-integration",
            "automatic_code_changes": False,
            "automatic_production_deployments": False,
            "note": "The scan is automatic. Code changes, major dependency upgrades, provider integrations, and production deployments require review and approval."
        }
    }
    (OUT / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# ULTIMA Monthly Update Report — {stamp}", "",
        f"Generated: {checked_at}", "",
        "## Project inventory",
        "| Project | Repository | Latest release | Latest commit | Status |",
        "|---|---|---:|---|---|"
    ]
    for p in projects:
        lines.append(f"| {p['name']} | [{p['repository']}](https://github.com/{p['repository']}) | {p['latest_release'] or 'No GitHub release'} | {p['latest_commit'] or 'Unavailable'} | {'Error: '+p['error'] if p['error'] else 'Checked'} |")
    lines += ["", "## AI innovation sources", "| Tool / framework | Latest release | Latest commit | Status |", "|---|---:|---|---|"]
    for p in innovations:
        lines.append(f"| {p['name']} | {p['latest_release'] or 'No GitHub release'} | {p['latest_commit'] or 'Unavailable'} | {'Error: '+p['error'] if p['error'] else 'Checked'} |")
    lines += [
        "", "## Integration and safety",
        "- This run is a discovery and review pass, not an unattended code deployment.",
        "- Stable, compatible dependency updates can be prepared as reviewable pull requests.",
        "- Major upgrades, new AI providers, model changes, new costs, permissions, payment flows, database migrations, and production deployments require approval.",
        "- Preserve every AI's individual name, persona, system prompt, knowledge context, and existing features.",
        "- Excluded projects: " + ", ".join(REGISTRY.get("excluded", [])) + ".",
        "- Protected repository: " + ", ".join(REGISTRY.get("protected", [])) + " (no changes).",
        "", "## Result",
        f"- Projects checked: {len(projects)}",
        f"- AI tool/framework sources checked: {len(innovations)}",
        f"- Repository lookup errors: {sum(bool(p['error']) for p in projects + innovations)}",
        ""
    ]
    (OUT / f"report-{stamp}.md").write_text("\n".join(lines), encoding="utf-8")
    reports = sorted(p.name for p in OUT.glob("report-*.md"))
    (OUT / "index.json").write_text(json.dumps({"files": reports}, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(f"ULTIMA update scan complete: {len(projects)} projects, {len(innovations)} innovation sources")

if __name__ == "__main__":
    main()
