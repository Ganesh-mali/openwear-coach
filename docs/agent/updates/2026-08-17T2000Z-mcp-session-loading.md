# Agent update — MCP session loading — 2026-08-17T20:00Z

## Outcome

The user restarted the desktop app and reopened the existing task, but
`openwear_local` did not appear under `/mcp`.

The bundled Codex CLI, run from the repository root, lists `openwear_local` as
enabled with the expected project-scoped STDIO command, environment, working
directory, and one-tool allowlist. The project is also marked trusted. The
configuration is therefore accepted; the remaining issue is that an existing
task retains the MCP inventory with which it was created.

## Evidence

- Project config exists at `.codex/config.toml` and parses successfully.
- Project trust entry exists for the exact repository path.
- `.venv/Scripts/openwear-coach.exe` exists.
- Bundled CLI `mcp list` reports `openwear_local` as `enabled`.
- The same relative command and STDIO environment previously completed an MCP
  initialize and `get_data_coverage` call without opening a network port.

## Changed files

Updated `README.md`, `SECURITY.md`, `docs/FIRST_PARTY_PLUGIN.md`, and the root
coordination files to require a new task after restart, rather than reopening
the pre-existing task.

## Next safe action

Create a new task inside the OpenWear Coach project and enter `/mcp`. Approve
only `get_data_coverage`. No tunnel, API key, paid service, or personal health
data is involved.
