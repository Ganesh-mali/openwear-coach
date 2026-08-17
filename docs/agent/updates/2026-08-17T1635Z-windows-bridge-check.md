# Agent update — windows bridge check — 2026-08-17T16:35Z

## Scope

Read-only check of this Windows environment for a personal iCloud Drive handoff and the current OpenWear/Codex plugin wiring. No user files, credentials, or health data were inspected.

## Findings

- iCloud for Windows was not detected as an installed Appx package.
- No standard local iCloud Drive folder was present at the checked safe candidate paths: `%USERPROFILE%\\iCloudDrive`, `%USERPROFILE%\\iCloud Drive`, or `%USERPROFILE%\\Apple\\iCloudDrive`.
- `iCloudDrive.exe` was not on `PATH`.
- The repository exposes a local Streamable HTTP MCP server on `127.0.0.1:8000` by default (`src/openwear_coach/server.py`) and defines nine local tools.
- The repository has a coaching skill at `plugin/skills/strength-coach/SKILL.md`, but no `.codex-plugin/plugin.json`, MCP dependency mapping, or local installation manifest was found. It is therefore a skill scaffold rather than an installable OpenWear plugin.

## Implication

The iCloud Drive queue remains a viable personal bridge only after iCloud for Windows is installed, signed in, and its Drive folder is enabled. It would avoid exposing an inbound Windows endpoint to the internet. The present project still needs an Apple Health payload importer/watcher and plugin packaging before ChatGPT can query the automatically imported local data.

## Exact checks performed

```powershell
Get-AppxPackage -Name '*iCloud*'
Test-Path <three standard iCloud Drive candidate paths>
Get-Command iCloudDrive.exe
rg --files
Get-Content pyproject.toml src/openwear_coach/server.py plugin/skills/strength-coach/SKILL.md
```

## Next safe action

Ask whether the user is willing to install and use iCloud for Windows as the private personal handoff. If yes, prototype an incremental Apple Shortcuts export plus a local folder watcher using only synthetic payloads.
