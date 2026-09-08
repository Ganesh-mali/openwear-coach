# OpenWear Coach (provisional name)

An open-source, local-first MCP server for strength-training and recovery analysis from user-owned wearable data.

The project is deliberately vendor-neutral. The first version works with CSV imports and local SQLite. An official Garmin Connect adapter is planned behind the same interface, subject to Garmin Connect Developer Program approval and any applicable licensing terms.

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

This repository is a working pre-alpha scaffold, not yet a public ChatGPT app.

Implemented:

- SQLite schema for health samples, activities and strength sets;
- CSV import for health and strength data;
- deterministic readiness and strength-progression calculations;
- MCP tools with explicit safety annotations;
- unit tests for the dependency-free analytics core.

Not yet implemented:

- Garmin OAuth and webhooks/push ingestion;
- FIT/TCX/GPX decoding;
- hosted multi-user authentication;
- workout publication to Garmin;
- public HTTPS deployment and ChatGPT directory submission.

## Quick start

Requirements: Python 3.11+ and `uv` (recommended) or `pip`.

```bash
cd openwear-coach
python -m venv .venv
. .venv/bin/activate
pip install -e .
openwear-coach
```

The Streamable HTTP MCP endpoint is `http://127.0.0.1:8000/mcp` by default. Override the local database with:

```bash
export OPENWEAR_DB=/absolute/path/to/openwear.db
```

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
