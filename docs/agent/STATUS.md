# OpenWear Coach status

Last verified: 2026-08-17 (Europe/London)

## Project phase

Working pre-alpha scaffold for a local-first, vendor-neutral wearable-data MCP server. CSV import and local SQLite are the stable initial path; Garmin and hosted/public integrations remain future work.

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
- Strength Coach skill scaffold, product brief, README, and unit tests
- Windows-safe SQLite connection cleanup and package-safe MCP Inspector imports

## Verified

- Unit suite: 7/7 passed
- Editable install, compilation, imports, and dependency check passed
- MCP HTTP initialization returned 200
- `tools/list` returned all nine tools
- Draft PR is open and marked draft

## Known risks and follow-ups

- Strength-set identity can collide across dates or sources; define durable identity semantics before real user data.
- Known health metrics need finite-value checks and unit validation/normalization.
- Session replacement semantics and readiness baseline requirements need explicit design and tests.
- The skill is a scaffold, not yet an installable plugin manifest with MCP dependency mapping.
- Hosted/non-loopback deployments require authentication and a privacy/security design.

## Next three actions

1. Specify and test strength-set identity plus session replacement semantics.
2. Add health metric validation, normalization, and adversarial tests.
3. Decide whether to package the skill as an installable plugin now or keep it explicitly documented as a scaffold.
