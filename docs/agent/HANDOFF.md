# Handoff

Updated: 2026-08-17 (Europe/London)

## Goal

Finish the user's first-party OpenWear Coach plugin and automatic Garmin path without third-party fitness plugins, extra Platform charges, or raw personal health data in Git.

## Repository state

- Branch: `agent/initial-openwear-coach`
- Current validated implementation is on the branch below; use `git log -1`
  for the latest published commit.
- Draft PR: [#1](https://github.com/Ganesh-mali/openwear-coach/pull/1) into `main`
- Working tree contains two intentional, untracked source inputs; never stage them.

## Completed

- Imported and published the pre-alpha scaffold.
- Fixed SQLite connection cleanup, package-safe server imports, and repository ignores.
- Passed 17 unit tests, compilation, plugin/skill validation, and MCP STDIO and
  HTTP read-call smoke checks.
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
- Confirmed ChatGPT web rejects a plain loopback MCP URL; Secure MCP Tunnel is
  therefore not needed for the selected desktop-local route.
- Created an unused Platform tunnel during the preflight, but did not create a
  runtime API key, download or run a tunnel client, add credits, or transmit
  data. Delete it only with the user's explicit approval.
- Recorded the user's hard no-extra-charge constraint. The selected proof is a
  project-scoped STDIO MCP process with synthetic data and no listening port.
- Added `.codex/config.toml` with only `get_data_coverage` enabled and prompt
  approval, plus a fail-closed loopback-only HTTP development fallback.
- Added `SECURITY.md`; verified HTTP rejects wildcard/LAN serving, invalid Host
  headers, and invalid Origin headers.

## Next exact action

1. Run `git -c safe.directory=C:/Users/GANESH/open_source_projects/openwear-coach status -sb`.
2. Read `updates/2026-08-17T1945Z-local-stdio-security.md`.
3. Restart the desktop host, then create a new task inside this trusted project.
   Reopening a task created before the config change retains its old MCP
   inventory.
4. Confirm `openwear_local` under `/mcp` in the new task and approve only the read-only
   `get_data_coverage` proof call. Keep personal health data out of the proof.
5. Optionally install the skills-only package through a local marketplace; it
   has no MCP mapping yet and must not fabricate a connection ID.
6. Prepare `PROVIDER-001` and the Garmin Developer Program application in
   parallel, retaining the no-extra-charge constraint.
7. Use Terra/medium for bounded plugin wiring and fixtures; return to Sol for
   OAuth/privacy or cross-provider identity decisions.

## Do not

- Stage the archive, duplicate extraction, venv, caches, databases, or egg metadata.
- Treat readiness or wearable-derived values as medical conclusions.
- Claim exact token usage or savings without telemetry.
- Collect Garmin credentials, scrape Garmin Connect, or claim that ChatGPT itself can access watch Bluetooth.
- Commit raw Apple Health, Garmin, FIT, device-identifier, or location data.
- Claim the Shortcut route is fully headless: Garmin Connect must be open in the iPhone foreground for Apple Health transfer.
- Install or authorize Fitness AI Connector or LiftTrack.
- Authorize Garmin or transmit health data without the user's action-time consent.
- Create a Platform runtime key, run `tunnel-client`, buy credits, enable
  auto-reload, or assume Secure MCP Tunnel is free.

## Blocker or decision needed

The local server entry is implemented, validated, and reported as enabled by
the bundled Codex CLI. The remaining proof requires a new desktop task created
after restart; reopening the existing task preserves its old MCP inventory. A
web plugin mapping remains deferred because it needs a Platform runtime key and
pricing assurance. Garmin automatic sync remains blocked on Developer Program
approval and credentials.
