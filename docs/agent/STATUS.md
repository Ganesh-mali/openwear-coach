# OpenWear Coach status

Last verified: 2026-09-07 (Europe/London)

## Ready locally

Latest target: iPhone-only daily use through existing Garmin Connect, Apple
Health, Shortcuts and ChatGPT. Shortcut source/assembly guide now exists in
shortcuts/, but is unsigned and not installed or runtime-tested. PC imports
below are optional developer capabilities, not completion of the mobile goal.

The supported Apple Health export and manual Garmin-observation workflow is usable: canonical CSV validation and
import, local SQLite storage, an offline CLI, and dated ChatGPT Project packs.
Run `scripts/setup.ps1` and follow `docs/USE_NOW.md`.

- `openwear` CLI: status, import-health, import-strength, project-pack.
- Dry runs do not create a database; imports validate the whole batch first.
- Pack exports preserve dates/sources and refuse empty ranges or existing folders.
- Pack includes JSON, Project instructions, profile template and getting-started text.
- Nine-tool STDIO MCP server also works in an isolated client integration test.
- Health baselines exclude samples older than 28 calendar days and the target day.
- Strength writes reject non-finite loads and fractional counts.
- Windows setup, editable install and pip check passed; 33 tests passed.
- Synthetic demo pack exists under ignored `.local/demo-ready-pack-20260907/`.
- No real health data imported, uploaded or committed during this work.

## GitHub

Branch: `agent/initial-openwear-coach`; existing PR #1 targets `main`.
Publishing this phase uses explicit source paths only. Read the linked update
for the final publishing evidence, and use git log/status for current state.

## Still unfinished

- Fully automatic transfer is outside the selected scope. The user rejected
  developer approval as a dependency and chose supported exports/Apple Health
  over unofficial account access. No Garmin application or login is required.
- This desktop task exposes no OpenWear MCP tool; client smoke is not proof of
  a host-loaded connection. The CLI/file workflow removes that dependency.
- ChatGPT Project creation and personal-file upload remain user setup.
- Session replacement is unsupported: imports are additive/upsert only.
- Native Garmin CSV/FIT parsing, bodyweight/assisted load semantics, hosted auth,
  web plugin registration and workout publishing remain future work.
- SQLite is not application-encrypted. Generated packs contain personal data
  when populated; review before sharing and keep under ignored `.local/`.
- Preserve no-extra-Platform-charge and no-third-party-plugin constraints.

## Safety decision

User explicitly selected supported exports/Apple Health over unofficial sync.
The experimental unofficial connector was removed and garminconnect uninstalled
before commit. It never authenticated. Apple XML imports use defusedxml and
select only exact source/dates; supported subset documented in APPLE_HEALTH.md.

Published implementation: 363ceab on origin/agent/initial-openwear-coach; PR #1 ready for review, not merged. Hosted CI completion remains unverified because the watch command was declined. Final publishing evidence is recorded locally in the linked update.

## 2026-09-09 verification

38 local tests passed. Official Garmin export subset reader and private initial
history pack prepared; no personal data uploaded. Apple signing on GitHub was
attempted and requires an iCloud-signed-in Mac. The failing hosted workflow was
removed; one-time local Mac signing script and phone assembly guide provided.
User chose one-time on-iPhone assembly with guidance; actual iPhone verification remains pending.
