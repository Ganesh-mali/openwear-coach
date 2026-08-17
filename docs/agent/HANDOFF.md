# Handoff

Updated: 2026-08-17 (Europe/London)

## Goal

Finish the user's first-party OpenWear Coach plugin and automatic Garmin path without third-party fitness plugins or raw personal health data in Git.

## Repository state

- Branch: `agent/initial-openwear-coach`
- Implementation baseline: `cf505b8` plus the current validated first-party/plugin and DATA-001 work
- Draft PR: [#1](https://github.com/Ganesh-mali/openwear-coach/pull/1) into `main`
- Working tree contains two intentional, untracked source inputs; never stage them.

## Completed

- Imported and published the pre-alpha scaffold.
- Fixed SQLite connection cleanup, package-safe server imports, and repository ignores.
- Passed 10 unit tests, compilation, plugin/skill validation, and MCP HTTP/tool-discovery/read-call smoke checks.
- Established the file-based agent exchange and model-efficiency policy under `docs/agent/`.
- Confirmed the user's Venu 4 is paired through Garmin Connect on iPhone.
- Documented an iCloud Drive/Apple Shortcut fallback, subject to user acceptance and one-time setup.
- Confirmed this Windows laptop does not currently have iCloud for Windows installed.
- Created and validated `plugins/openwear-coach/` with its own manifest and packaged Strength Coach skill.
- Audited two public Garmin plugins found by the user: Fitness AI Connector is the fastest read-only wellness/activity proof; LiftTrack is a separate strength-planning/read-back product.
- Confirmed neither third-party plugin is installed; no external account or health data was connected during the audit.
- Recorded the user's decision to reject both third-party plugins and build OpenWear's own.
- Implemented source/date-safe strength identity, transactional legacy migration, source-aware reads/exports, and path-redacted coverage output.
- Added `docs/FIRST_PARTY_PLUGIN.md` with the supported Garmin API architecture and Windows/ChatGPT connection path.

## Next exact action

1. Run `git -c safe.directory=C:/Users/GANESH/open_source_projects/openwear-coach status -sb`.
2. Read `updates/2026-08-17T1840Z-root-first-party-plugin.md`.
3. When the user is ready, launch the local HTTP MCP server with an isolated database and have the user enable ChatGPT developer mode and register its URL.
4. Capture the generated `plugin_asdk_app...` ID, add the local `.app.json` and marketplace wiring, validate, and test one synthetic read-only prompt.
5. Keep personal health data out of the proof; use synthetic rows until Garmin OAuth and consent handling exist.
6. Prepare `PROVIDER-001` and the Garmin Developer Program application in parallel.
7. Use Terra/medium for bounded plugin wiring and fixtures; return to Sol for OAuth/privacy or cross-provider identity decisions.

## Do not

- Stage the archive, duplicate extraction, venv, caches, databases, or egg metadata.
- Treat readiness or wearable-derived values as medical conclusions.
- Claim exact token usage or savings without telemetry.
- Collect Garmin credentials, scrape Garmin Connect, or claim that ChatGPT itself can access watch Bluetooth.
- Commit raw Apple Health, Garmin, FIT, device-identifier, or location data.
- Claim the Shortcut route is fully headless: Garmin Connect must be open in the iPhone foreground for Apple Health transfer.
- Install or authorize Fitness AI Connector or LiftTrack.
- Authorize Garmin or transmit health data without the user's action-time consent.

## Blocker or decision needed

ChatGPT must generate the user's MCP connection ID during developer-mode registration; no valid `.app.json` can be created before that one-time user action. Garmin automatic sync remains blocked on Developer Program approval and credentials.
