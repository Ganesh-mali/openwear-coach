# OpenWear Coach status

Last verified: 2026-08-17 (Europe/London)

## Project phase

Working pre-alpha for a local-first, vendor-neutral wearable-data MCP server and first-party OpenWear Coach plugin. The user rejected third-party Garmin plugins and requires no extra Platform charge. The current proof target is a project-scoped STDIO MCP process in the ChatGPT desktop/Codex host; the supported automatic target remains OpenWear's own adapter to Garmin's official Activity and Health APIs.

## Repository state

- Branch: `agent/initial-openwear-coach`
- The validated implementation is maintained on the branch below; use
  `git log -1` for the latest published commit.
- Draft PR: [#1](https://github.com/Ganesh-mali/openwear-coach/pull/1) into `main`
- Remote: `https://github.com/Ganesh-mali/openwear-coach.git`
- Local-only inputs deliberately excluded from Git: `openwear-coach-prealpha.tar.gz` and `openwear-coach-prealpha/`

## Implemented

- Python 3.11+ package with `mcp[cli]>=2,<3`
- Local SQLite storage and CSV import for health and strength data
- Strength volume/e1RM, health trends, readiness, sessions, progression, and export logic
- STDIO and loopback Streamable HTTP MCP transports with nine server tools
- Validated first-party plugin manifest and packaged Strength Coach skill
- Source-aware strength-set identity and transactional legacy-schema migration
- Windows-safe SQLite connection cleanup and package-safe MCP Inspector imports
- User-facing first-party architecture and Windows setup guide
- A no-extra-cost project MCP configuration that opens no port and exposes
  coverage, approved health/strength recording, trends and progress tools
- Fail-closed HTTP bind validation and a documented local threat model
- Canonical health metric/unit/range validation and safe source identifiers
- Source-specific health trends and readiness baselines that exclude the target
  date and require seven earlier samples
- A coverage-aware, non-medical physical wellbeing skill and today's Garmin
  screenshot workflow

## Verified

- Unit suite: 21/21 passed
- Editable install, compilation, imports, and dependency check passed
- MCP STDIO and HTTP initialization plus a read-only tool call passed
- Invalid Host and Origin requests were rejected; non-loopback launch failed
  before listening
- `tools/list` returned all nine tools
- OpenAI plugin validator and skill validator passed
- End-to-end MCP STDIO health import, trends and readiness calls passed against
  a temporary synthetic database
- Draft PR is open and marked draft

## Known risks and follow-ups

- Session replacement semantics still need explicit design and tests.
- The plugin package is skills-only and has no `.app.json`; a local marketplace
  can install its coaching instructions, but a web plugin mapping remains
  deferred under the user's no-extra-charge requirement.
- Secure MCP Tunnel requires a Platform runtime API key. A preflight tunnel
  exists but is unused; no key, client, credits, or health data were used.
- Hosted/non-loopback deployments are rejected; enabling them later requires
  authentication and a privacy/security design.
- Apple Health provides an automatic but incomplete Garmin subset and requires Garmin Connect to be foregrounded for transfer.
- iCloud for Windows is not installed on the current laptop; the recommended drop-folder bridge cannot run until the user installs, signs in, and enables iCloud Drive.
- The Shortcut route should use a rolling window and importer-side idempotency; it must never treat missing metrics as zero.
- Public Connect IQ APIs do not expose native Garmin strength history, sleep stages, or HRV status; a sidecar can only provide supported device-local metrics and OpenWear-owned activities.
- Garmin Activity/Health API access remains approval-gated; OAuth, consent, revocation, push ingestion, reconciliation, and deletion are not implemented.
- A truthful Health plus Activity API evaluation package is ready; sending it
  needs the user's business/contact details and action-time confirmation.
- SQLite is not application-encrypted; the synthetic proof must remain empty
  until Windows storage/access expectations are reviewed.

## Next three actions

1. After restarting the desktop host, create a new task inside this project,
   submit `/mcp`, confirm `openwear_local`, check coverage, and approve a dated
   Garmin screenshot import using `docs/TODAY_WELLBEING.md`.
2. Optionally install the skills-only package from a local marketplace.
3. Prepare the official Garmin Developer Program application and a provider adapter with synthetic fixtures while approval is pending.
