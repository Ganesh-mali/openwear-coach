# Use OpenWear Coach now

The usable personal version is **supported Apple Health exports or manual Garmin
observations → local database → dated files for a ChatGPT Project**, or local
MCP when connected. We do not use unofficial Garmin account access or depend
on Garmin developer approval. You need no OpenAI API key, paid tunnel,
or third-party fitness plugin for this file workflow. ChatGPT account limits
still apply.

## 1. Set up Windows

From the repository folder, with Python 3.11+ installed:

```powershell
.\scripts\setup.ps1
```

No shell activation is needed. All commands below run from this repository.
Data defaults to `.local/openwear-local.db`, matching the project MCP config.
The `.local/` folder is ignored by Git. SQLite is not application-encrypted;
keep it in your private Windows account, use disk protection appropriate for
your device, and do not place it in a shared or synced directory unintentionally.

## 2. Try synthetic data separately

```powershell
.\.venv\Scripts\python.exe -m openwear_coach.cli --db .local/demo.db import-health examples/synthetic-health.csv --source synthetic_demo
.\.venv\Scripts\python.exe -m openwear_coach.cli --db .local/demo.db import-strength examples/synthetic-strength.csv --source synthetic_demo
.\.venv\Scripts\python.exe -m openwear_coach.cli --db .local/demo.db project-pack --start 2026-09-01 --end 2026-09-02 --out .local/demo-pack
```

Open `.local/demo-pack/START_HERE.md`. These records are invented and must never
be treated as your measurements. Use a new output folder for each pack.

## 3. Bring your Garmin observations

For supported iPhone exports, use the [Apple Health import guide](APPLE_HEALTH.md).
It reads a limited, source-filtered subset of Apple's native XML locally.
Use the CSV path below for metrics missing from Apple Health.

In Garmin Connect, select the exact date and copy the metrics you want to use
into `.local/health.csv` using the [canonical CSV format](../README.md#csv-formats).
Screenshots can help transcribe values, but check every value, date and unit.
Native Garmin CSV downloads have different schemas and are **not** directly
supported. FIT archives are not supported yet. Do not enter Garmin passwords.

For sleep use the waking date. Record the same kind of HRV/stress/Body Battery
observation consistently each day; do not mix overnight averages and spot
readings under one metric/source. If the meaning differs, use a separate source.
Omit unavailable metrics. This schema keeps one value per date/metric/source.

```powershell
.\.venv\Scripts\python.exe -m openwear_coach.cli import-health .local/health.csv --source garmin_manual --dry-run
.\.venv\Scripts\python.exe -m openwear_coach.cli import-health .local/health.csv --source garmin_manual
.\.venv\Scripts\python.exe -m openwear_coach.cli status
```

For strength, create `.local/strength.csv` using the README format, then:

```powershell
.\.venv\Scripts\python.exe -m openwear_coach.cli import-strength .local/strength.csv --source garmin_manual --dry-run
.\.venv\Scripts\python.exe -m openwear_coach.cli import-strength .local/strength.csv --source garmin_manual
```

Reimporting the same keys updates values without duplication. Imports add/update
sets; omitting a previously imported set does not delete it. Whole-session
replacement is not supported. Use positive external load in kg; bodyweight and
assisted-exercise load semantics are not supported yet.

## 4. Create the coaching Project

Export the date range you actually imported (replace these example dates):

```powershell
.\.venv\Scripts\python.exe -m openwear_coach.cli project-pack --start 2026-09-01 --end 2026-09-07 --out .local/coach-pack-2026-09-07
```

Review the JSON before sharing it. In ChatGPT, create a Project named **Garmin
Personal Coach**. Paste the generated `PROJECT_INSTRUCTIONS.md` into its
instructions. Fill in `MY_PROFILE.md` with goals, schedule and preferences,
then upload that profile and `coach-data.json` as Project sources.

Projects keep related chats, instructions and sources together; a ChatGPT
Project does not automatically read your local database. See the
[official Projects documentation](https://learn.chatgpt.com/docs/projects).
Memory, when available, can retain preferences; the dated files remain the
measurement record. Keep your profile and decision log current explicitly.

Start a chat in that Project:

> Check the coverage and sources in my attached data. Summarize my recent
> training and recovery, ask how I feel, then help me plan my next session.

After new imports, generate a fresh pack and replace the old data attachment.
Keep your completed profile instead of uploading a new blank template. Nothing
is uploaded by the command, and attachments do not synchronize automatically.

## Local MCP and automatic sync

The repository includes an optional local STDIO MCP configuration. If OpenWear
tools are available in the host, start with `get_data_coverage` and use the
exact source shown there for health tools. This file workflow works even when
the host has not loaded that connection.

The selected route needs no Developer Program application. Direct Garmin API
integration and unofficial personal-account access are outside this release.
The older application document is historical, not a prerequisite. This release
does not claim a live Garmin connection or fully automatic transfer.
