# Agent update — first-party OpenWear plugin — 2026-08-17T18:40Z

## Outcome

The user rejected Fitness AI Connector and LiftTrack and chose a first-party
OpenWear Coach plugin. Neither vendor was installed or authorized. No Garmin,
Apple Health, FIT, location, device-identifier, or other personal health data
was accessed.

The repository now contains a validated plugin package at
`plugins/openwear-coach/`, including its required manifest and Strength Coach
skill. No `.app.json` or fabricated MCP connection ID was added: ChatGPT must
generate the `plugin_asdk_app...` ID during developer-mode registration.

DATA-001 is complete. Strength rows use `(date, source, session_id, exercise,
set_index)` identity; legacy databases migrate transactionally; exact replays
update payload fields only. Source now survives reads, session grouping, and
export. `get_data_coverage` reports local SQLite without exposing the absolute
database path.

## Changed files

- `plugins/openwear-coach/.codex-plugin/plugin.json`
- `plugins/openwear-coach/skills/strength-coach/SKILL.md`
- `src/openwear_coach/models.py`
- `src/openwear_coach/storage.py`
- `src/openwear_coach/server.py`
- `tests/test_storage_and_imports.py`
- `README.md`
- `docs/FIRST_PARTY_PLUGIN.md`
- agent exchange files and unique updates under `docs/agent/`

## Validation

- `PYTHONPATH=src python -m unittest discover -s tests -v` — 10/10 passed.
- `python -m compileall -q src tests` — passed.
- OpenAI plugin-creator validator — passed.
- Skill quick validator — passed.
- Local MCP Streamable HTTP smoke — 9 tools discovered and
  `get_data_coverage` returned without a tool error.
- Independent final diff review — no code blocker; explicit staging required to
  exclude the source archive and duplicate extraction.
- `git diff --check` — passed; only Git line-ending notices were emitted.

PyYAML 6.0.3 was installed only into the ignored project `.venv` to run the
required plugin validator. It was not added as an application dependency.

## Architecture and blocker

The supported automatic personal flow is Venu 4 to Garmin Connect on iPhone,
Garmin Connect cloud, OpenWear's official Garmin Activity/Health API adapter,
the user-controlled OpenWear database, MCP, and the first-party plugin. The
Garmin phase is approval-gated.

The immediate blocker is the one-time ChatGPT developer-mode connection step.
When the user is ready, start the isolated local MCP server, register its URL,
capture the generated connection ID, add local `.app.json`/marketplace wiring,
and test only synthetic data.

## Model review

Model switch recommendation: Sol -> Terra/medium. The data-integrity and
architecture decisions are complete; the next plugin connection and synthetic
fixture work is bounded implementation. Return to Sol for OAuth, consent,
token-storage, deletion, or cross-provider identity design.
