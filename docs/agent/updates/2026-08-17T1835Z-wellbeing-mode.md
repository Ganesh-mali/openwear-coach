# Agent update — local wellbeing mode — 2026-08-17T18:35Z

## Outcome

Expanded OpenWear's zero-extra-cost project MCP configuration from workout-only
use to a source-aware physical wellbeing workflow. The enabled STDIO tools now
include approved health CSV import, health trends and daily readiness alongside
coverage and strength tools. No port, tunnel, API key or paid service is used.

Added a canonical health metric catalogue for sleep, heart rate, HRV, stress,
Body Battery, respiration, SpO2, steps, active minutes, calories, weight and
skin-temperature delta. Imports and storage reject unsupported metrics, wrong
units, non-finite values, unsafe source identifiers and broad out-of-range
values. Unit aliases normalize to canonical units.

Health reads and readiness are now source-specific. HRV and resting-HR
baselines exclude the target date, use up to 28 earlier days and require at
least seven samples. Coverage reports the available health sources.

Updated both packaged coach skills with explicit coverage, provenance and
non-medical boundaries. Added `docs/TODAY_WELLBEING.md` for a privacy-minimized
Garmin screenshot workflow today and the official Garmin/Apple automation
constraints.

## Changed files

- `.codex/config.toml`
- `README.md`
- `docs/TODAY_WELLBEING.md`
- `plugin/skills/strength-coach/SKILL.md`
- `plugins/openwear-coach/skills/strength-coach/SKILL.md`
- `src/openwear_coach/health_metrics.py`
- `src/openwear_coach/importers.py`
- `src/openwear_coach/server.py`
- `src/openwear_coach/storage.py`
- `tests/test_storage_and_imports.py`

## Validation

- `PYTHONPATH=src python -m unittest discover -s tests -v`: 21/21 passed.
- `python -m compileall -q src tests`: passed.
- Both skill directories passed the skill-creator `quick_validate.py` check.
- Project TOML parsed with exactly seven enabled tools, `writes` approval and
  STDIO transport.
- End-to-end MCP STDIO smoke listed and successfully called
  `import_health_csv`, `get_health_trends` and `get_daily_readiness` against a
  temporary synthetic database.
- `git diff --check`: passed; only line-ending conversion warnings.
- Bundled `codex mcp get` could not be rerun because Windows denied sandbox
  execution of the packaged app binary. This is a host-access limitation, not
  an MCP server failure; the independent protocol smoke passed.

## Next safe action

Restart Codex desktop, create a new task in this project and submit `/mcp`.
Confirm `openwear_local`, then follow `docs/TODAY_WELLBEING.md`. Attach cropped,
dated Garmin screenshots and approve only the exact proposed CSV. Do not infer
missing values or claim automatic watch connectivity.
