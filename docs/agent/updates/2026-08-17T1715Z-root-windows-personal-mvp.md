# Agent update — Windows personal MVP — 2026-08-17T17:15Z

## User environment and goal

- Garmin Venu 4 paired to Garmin Connect on an iPhone.
- OpenWear and ChatGPT/Codex run on a Windows laptop.
- First target is one private user with automatic transfer after one-time authorization/setup; multi-user Garmin API work can follow later.

## Recommended personal architecture

Use a private iCloud Drive drop-folder for the first proof:

```text
Venu 4 -> Garmin Connect (iPhone foreground sync) -> Apple Health
        -> personal Shortcut -> iCloud Drive/OpenWear-inbox
        -> iCloud for Windows -> validated local importer -> SQLite
        -> OpenWear MCP tools + Strength Coach skill -> ChatGPT
```

This avoids Mac/Xcode signing, a public ingest endpoint, Windows firewall exposure, and collecting Garmin credentials. Enable Advanced Data Protection so iCloud Drive envelopes are end-to-end encrypted. This Windows environment does not currently have iCloud for Windows or a standard iCloud Drive folder installed.

The route is near-automatic, not fully headless: Garmin documents that Connect must be open in the iPhone foreground for data to transfer to Apple Health. The Shortcut can run after the Connect app is closed and export a bounded rolling window without another prompt.

## Coverage boundary

The documented Garmin-to-Apple-Health subset includes all-day heart rate, sleep analysis, steps, energy, distance, and workout summaries. It does not include native Garmin strength sets/reps/weight, GPS tracks, detailed activity heart-rate samples, stress, Body Battery, or HRV status. Do not describe those missing fields as obtainable through this bridge.

## Plugin explanation

- The existing MCP server is the live-data/tool layer. It already exposes nine local OpenWear operations.
- The existing `strength-coach` skill is the behavioural layer: it tells ChatGPT when and how to use those tools and adds coaching guardrails.
- The repository is not an installable plugin yet because it lacks `.codex-plugin/plugin.json` and an MCP connection/dependency mapping.
- The Plugins section packages a stable identity, skills, MCP tools/connections, and optional UI/auth. It does not itself acquire Bluetooth/watch data.
- No Garmin connector is present in the plugins currently exposed to this task or in the supplied recommended-plugin list.

## Safe implementation order

1. User installs/signs into iCloud for Windows, enables iCloud Drive, and decides whether to enable Advanced Data Protection with a recovery method.
2. Fix `DATA-001` strength identity before accepting personal data.
3. Build and test a synthetic Apple Health JSON envelope contract, folder watcher, validation, deduplication, receipts, and quarantine.
4. Build the iPhone Shortcut with minimum Health/Files permissions and an app-close/time trigger.
5. Use the `plugin-creator` skill to package the existing server and skill, then connect/test it locally with synthetic data.
6. Only then conduct a minimal real-data proof and keep raw envelopes out of Git, logs, agent updates, and ChatGPT prompts.

## Evidence updates

- `2026-08-17T1635Z-windows-bridge-check.md`
- `2026-08-17T1640Z-plugin-audit.md`
- `2026-08-17T1705Z-shortcut-bridge-design.md`

## Model routing

Use Terra/medium for the bounded importer and plugin packaging. Use Sol for the strength identity migration and any decision to replace iCloud Drive with LAN/public transport.
