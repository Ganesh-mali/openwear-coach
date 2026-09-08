# OpenWear Coach

**iPhone-first work in progress:** [OpenWear Check-in Shortcut](shortcuts/README.md)
has generated source and a phone-only assembly guide. Signing, installation
and native execution are not yet verified. The PC workflow below is optional
and is not the intended daily phone experience.

**Start here: [Use your Garmin personal coach now](docs/USE_NOW.md).**
Import supported Apple Health XML or manually prepared Garmin observations, keep them locally, and generate
a dated coaching pack for a ChatGPT Project. Includes a Windows setup script,
synthetic demo, profile template and offline CLI. No Garmin developer approval
or unofficial Garmin account access is required. Transfers are file-based.

An open-source, local-first MCP server for strength-training and recovery analysis from user-owned wearable data.

The project is deliberately vendor-neutral. The personal version works with
supported file exports and local SQLite. Direct Garmin account integration is
outside the selected safety-first workflow.

> This project is independent and is not affiliated with, endorsed by, or sponsored by Garmin, OpenAI, or ChatGPT. Garmin and Garmin Connect are trademarks of Garmin Ltd. or its subsidiaries.

## Why this exists

The currently listed Fitness AI Connector is a useful proof of demand, but its public repository contains documentation and a remote-server manifest rather than the backend implementation. Its published privacy policy says that the free plan retains two days of fitness data. OpenWear Coach is intended to offer a transparent alternative:

- local-first storage and self-hosting;
- no paywall around the open-source core;
- exact-date strength analytics: sets, reps, load, volume and estimated 1RM;
- transparent recovery scoring using available sleep, HRV, resting-HR, stress and Body Battery inputs;
- portable imports and exports;
- adapter boundaries for Garmin, Apple Health and other sources;
- optional workout publishing through Garmin's Training API after approval.

## Status

This repository is a working pre-alpha with a validated first-party plugin
package. It is not yet connected to a ChatGPT MCP registration or published in
the public plugin directory.

Implemented:

- SQLite schema for health samples, activities and strength sets;
- CSV import for health and strength data;
- deterministic readiness and strength-progression calculations;
- MCP tools with explicit safety annotations;
- a first-party plugin manifest and packaged Strength Coach skill;
- source-aware strength identity with legacy database migration;
- unit tests for the dependency-free analytics core.

Not yet implemented:

- Garmin OAuth and webhooks/push ingestion;
- FIT/TCX/GPX decoding;
- hosted multi-user authentication;
- workout publication to Garmin;
- public HTTPS deployment and ChatGPT directory submission.

The implementation and connection roadmap is in
[docs/FIRST_PARTY_PLUGIN.md](docs/FIRST_PARTY_PLUGIN.md).

## Quick start

Requirements: Python 3.11+ and `uv` (recommended) or `pip`.

```bash
cd openwear-coach
python -m venv .venv
. .venv/bin/activate
pip install -e .
openwear-coach
```

PowerShell on Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
openwear-coach
```

The Streamable HTTP MCP endpoint is `http://127.0.0.1:8000/mcp` by default. Override the local database with:

```bash
export OPENWEAR_DB=/absolute/path/to/openwear.db
```

PowerShell equivalent:

```powershell
$env:OPENWEAR_DB = "$env:LOCALAPPDATA\OpenWearCoach\data.db"
```

The checked-in `.codex/config.toml` is the preferred zero-extra-cost setup for the
ChatGPT desktop/Codex host. It starts OpenWear through STDIO, opens no network
port, stores data under the Git-ignored `.local/` directory, and initially
enables coverage, approved health/strength recording, trends, readiness and
strength-progress tools. After restarting the
desktop host, create a new task inside this trusted project; an already-open
task keeps its original MCP inventory. Enter `/mcp` and submit it in the new
task to confirm `openwear_local`. See `docs/TODAY_WORKOUT.md` for the current
strength-session workflow. See `docs/TODAY_WELLBEING.md` for sleep, heart-rate,
HRV, stress, Body Battery and other wellbeing observations.

For manual HTTP development and MCP Inspector testing, use:

```powershell
.\scripts\start-local.ps1
```

This fallback launcher also uses `.local/` and binds only to `127.0.0.1`. The
server refuses LAN, wildcard, and hostname bindings because network
authentication is not implemented.

## First-party ChatGPT plugin

The plugin source is in `plugins/openwear-coach/`. It contains OpenWear's own
manifest and coaching skill; it does not install or call another fitness
plugin. The MCP mapping is intentionally added only after the local OpenWear
server is registered in ChatGPT developer mode, because ChatGPT generates a
user-specific connection ID during that one-time setup.

For development with the MCP Inspector:

```bash
mcp dev src/openwear_coach/server.py
```

## CSV formats

Health CSV:

```csv
date,metric,value,unit
2026-08-14,sleep_hours,7.6,h
2026-08-14,hrv_ms,52,ms
2026-08-14,resting_hr_bpm,55,bpm
2026-08-14,stress,24,score
2026-08-14,body_battery,71,score
```

Strength CSV:

```csv
date,session_id,exercise,set_index,reps,weight_kg,rir
2026-08-14,session-001,barbell_bench_press,1,8,60,2
2026-08-14,session-001,barbell_bench_press,2,8,60,1
```

Dates must be ISO `YYYY-MM-DD`. Weight is stored in kilograms. Import is additive and idempotent for identical primary keys.

Health imports use a canonical metric/unit catalogue and reject unknown metrics,
wrong units, non-finite values and values outside broad validation bounds. Health
trends and readiness are source-specific. HRV and resting-heart-rate baselines
use at least seven prior same-source samples and exclude the target date.

## MCP tools in the scaffold

- `get_data_coverage`
- `get_health_trends`
- `get_daily_readiness`
- `get_strength_sessions`
- `get_strength_progress`
- `import_health_csv`
- `import_strength_csv`
- `record_strength_session`
- `export_user_data`

The readiness score is a transparent coaching heuristic, not a medical metric. The result reports input coverage and component scores so missing data is visible.

## Tests

The analytics tests use Python's standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Open-source model

The scaffold is licensed under Apache-2.0 for permissive reuse plus an explicit patent grant. Keep the self-hosted core free. A hosted community service may still need sponsorship because public HTTPS hosting, support, security operations and some Garmin commercial API uses can create real costs.

Read the product and platform audit in [docs/PRODUCT_BRIEF.md](docs/PRODUCT_BRIEF.md).
