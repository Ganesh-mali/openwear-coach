# Agent update — today's workout mode — 2026-08-17T20:15Z

## Outcome

The screenshot showed `/mcp` still unsent in the new-task composer. The user
also needs OpenWear to be useful for a strength workout today, not only a
coverage proof.

Expanded the project-scoped STDIO allowlist to four tools:

- `get_data_coverage`
- `record_strength_session`
- `get_strength_sessions`
- `get_strength_progress`

The default approval mode is `writes`, so the annotated write tool prompts for
approval while the three read-only tools do not. The server still opens no
network port and uses no tunnel, Platform API key, or paid service.

Added `docs/TODAY_WORKOUT.md` with activation, workout-entry, watch, screenshot
bridge, and review instructions. Automatic Garmin download remains unavailable
until official API access and the provider adapter exist.

## Validation

- Project TOML parsed and the four-tool allowlist plus `writes` approval mode
  matched exactly.
- Bundled Codex CLI `mcp get openwear_local` reported the entry enabled with
  STDIO, the expected command/environment, all four tools, and `writes` mode.
- End-to-end STDIO smoke recorded one synthetic bench-press set, read back one
  session, and returned no MCP errors.
- Unit suite: 17/17 passed.
- `git diff --check`: passed, line-ending warnings only.

## Next safe action

Restart the desktop host, create a new task in the project, submit `/mcp`, and
confirm `openwear_local`. Check coverage, then record a reviewed strength
session. Do not claim that the watch is automatically connected.
