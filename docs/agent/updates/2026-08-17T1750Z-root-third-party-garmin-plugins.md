# Agent update — third-party Garmin plugins — 2026-08-17T17:50Z

## Discovery

The user found two public ChatGPT plugins:

- **Fitness AI Connector** by FMP: a hosted, read-only Garmin wellness/activity connector.
- **LiftTrack — Weightlifting For Garmin** by LiftTrack, LLC: a strength-workout planner and tracker that sends workouts to Garmin and reads completed strength sessions back.

Neither plugin is currently installed in the user's ChatGPT account according to the available permission-status check. No account was connected and no consent screen was accepted during this audit.

## Product impact

Fitness AI Connector is now the quickest personal proof for automatic Garmin-to-ChatGPT access. It claims Garmin Health, Activity, and Women's Health API access through Garmin OAuth; its published tool surface includes sleep, HRV, stress, Body Battery, activities, lap/HR analysis, body composition, and trends. It says access starts at connection time, is read-only, and does not expose the Garmin password.

This does not make it local-first. FMP states that Garmin health data is stored encrypted in Supabase/AWS US East and is provided to ChatGPT/Claude through MCP. Free retention is two days; Basic is $3/month with up to five years. Health data deletion is within 30 days, while some identifiers/payment records remain, and Garmin access must be revoked separately. FMP identifies itself as independent and not Garmin-endorsed; no Garmin-owned public record verifying FMP's individual approval was found.

LiftTrack is useful for strength training, not general wellness ingestion. It creates/schedules strength workouts, sends them through Garmin Connect to the watch, and reads sets/reps/weights/rest/duration back. Its ChatGPT plugin exposes templates and completed sessions. Public materials do not document exact Garmin scopes or whether ChatGPT can invoke writes. Its 2024 privacy notice does not name Garmin, ChatGPT, workout, or health data and says it does not process sensitive information, which is a material documentation gap.

## Recommended sequencing

1. Offer a bounded Fitness AI Connector free-tier experiment first, because it directly answers the user's immediate goal with read-only Garmin access.
2. Before authorization, the user should inspect the exact Garmin consent screen and accept the FMP/Supabase/OpenAI health-data boundary. Do not enable Women's Health data unless explicitly wanted.
3. Validate only yesterday's steps and sleep duration with timestamps/source; do not request broad raw history initially.
4. Treat LiftTrack as an optional strength-specific second experiment using a disposable workout template and explicit review of Garmin write permissions.
5. Keep OpenWear as the durable local/portable layer. Official OpenAI documentation does not establish direct plugin-to-plugin export, so neither third-party plugin should be assumed to populate OpenWear's SQLite database.
6. Continue `DATA-001` before any OpenWear real-data ingestion. The Apple Shortcut/iCloud route remains the local-first fallback if the user rejects third-party hosted health storage.

## Evidence updates

- `2026-08-17T1730Z-plugin-strategy-compare.md`
- `2026-08-17T1735Z-fitness-ai-connector-audit.md`
- `2026-08-17T1735Z-lifttrack-plugin-audit.md`

## Model routing

The vendor audits were bounded Terra tasks. Use Terra/low for the consent checklist and bounded test. Use Sol for any decision to transfer vendor data into OpenWear or for the local data-identity/security design.
