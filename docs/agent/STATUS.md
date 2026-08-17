# OpenWear Coach status

Last verified: 2026-08-17 (Europe/London)

## Project phase

Working pre-alpha for a local-first, vendor-neutral wearable-data MCP server and first-party OpenWear Coach plugin. The user rejected third-party Garmin plugins. The supported automatic target is OpenWear's own adapter to Garmin's official Activity and Health APIs; an Apple Health/iCloud bridge remains an optional personal fallback while approval is pending.

## Repository state

- Branch: `agent/initial-openwear-coach`
- Implementation baseline: `5b47f07d5227a2207b6d18dc52a1cf8693648a09`
- Draft PR: [#1](https://github.com/Ganesh-mali/openwear-coach/pull/1) into `main`
- Remote: `https://github.com/Ganesh-mali/openwear-coach.git`
- Local-only inputs deliberately excluded from Git: `openwear-coach-prealpha.tar.gz` and `openwear-coach-prealpha/`

## Implemented

- Python 3.11+ package with `mcp[cli]>=2,<3`
- Local SQLite storage and CSV import for health and strength data
- Strength volume/e1RM, health trends, readiness, sessions, progression, and export logic
- Streamable HTTP MCP endpoint with nine tools
- Validated first-party plugin manifest and packaged Strength Coach skill
- Source-aware strength-set identity and transactional legacy-schema migration
- Windows-safe SQLite connection cleanup and package-safe MCP Inspector imports
- User-facing first-party architecture and Windows setup guide

## Verified

- Unit suite: 10/10 passed
- Editable install, compilation, imports, and dependency check passed
- MCP HTTP initialization and a read-only tool call passed
- `tools/list` returned all nine tools
- OpenAI plugin validator and skill validator passed
- Draft PR is open and marked draft

## Known risks and follow-ups

- Known health metrics need finite-value checks and unit validation/normalization.
- Session replacement semantics and readiness baseline requirements need explicit design and tests.
- The plugin package has no `.app.json` yet because ChatGPT must first register the user's OpenWear MCP connection and generate its technical ID.
- Hosted/non-loopback deployments require authentication and a privacy/security design.
- Apple Health provides an automatic but incomplete Garmin subset and requires Garmin Connect to be foregrounded for transfer.
- iCloud for Windows is not installed on the current laptop; the recommended drop-folder bridge cannot run until the user installs, signs in, and enables iCloud Drive.
- The Shortcut route should use a rolling window and importer-side idempotency; it must never treat missing metrics as zero.
- Public Connect IQ APIs do not expose native Garmin strength history, sleep stages, or HRV status; a sidecar can only provide supported device-local metrics and OpenWear-owned activities.
- Garmin Activity/Health API access remains approval-gated; OAuth, consent, revocation, push ingestion, reconciliation, and deletion are not implemented.
- The absolute database path is no longer returned by `get_data_coverage`; non-loopback serving still needs an explicit guard.

## Next three actions

1. Start the local MCP server when the user is ready, register it in ChatGPT developer mode, and capture the generated connection ID without collecting health data.
2. Add the local `.app.json`/marketplace mapping and run a synthetic ChatGPT tool-call proof.
3. Prepare the official Garmin Developer Program application and a provider adapter with synthetic fixtures while approval is pending.
