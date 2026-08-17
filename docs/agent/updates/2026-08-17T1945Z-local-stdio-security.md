# Agent update — local STDIO security — 2026-08-17T19:45Z

## Outcome

Implemented the zero-additional-cost local server path with STDIO as the
preferred transport. No API key, tunnel client, public endpoint, Garmin login,
or personal health data was used.

## Security controls

- Added project-scoped `.codex/config.toml` using a local STDIO child process.
- Initially allowlisted only the read-only `get_data_coverage` tool with prompt
  approval.
- Added a fail-closed HTTP transport guard: only numeric loopback addresses and
  unprivileged ports are accepted.
- Retained HTTP solely as a manual development fallback via
  `scripts/start-local.ps1`.
- Added `SECURITY.md` covering data handling, residual local risks, and the
  no-tunnel/no-Platform-key boundary.

## Changed files

- `.codex/config.toml`
- `src/openwear_coach/security.py`
- `src/openwear_coach/server.py`
- `tests/test_server_security.py`
- `scripts/start-local.ps1`
- `README.md`
- `SECURITY.md`
- `docs/FIRST_PARTY_PLUGIN.md`
- coordination files owned by root

## Validation

- `PYTHONPATH=src python -m unittest discover -s tests -v`: 17/17 passed.
- Python compilation: passed.
- TOML parse and least-privilege assertions: passed.
- STDIO initialize plus `get_data_coverage`: passed; empty database, no error.
- HTTP initialize plus `get_data_coverage`: passed; empty database.
- Non-loopback launch using `0.0.0.0`: rejected before listening.
- Invalid HTTP Host: 421; invalid Origin: 403; valid loopback request: 200.
- `git diff --check`: passed, line-ending warnings only.

## Next safe action

Restart the desktop host, confirm `openwear_local` appears under `/mcp`, and
approve only `get_data_coverage`. Do not import personal health data yet.
