# Agent task ledger

Status values: `backlog`, `in_progress`, `blocked`, `completed`.

| ID | Status | Owner | Scope | Dependencies | Outcome / next step |
|---|---|---|---|---|---|
| OPS-001 | completed | root | Establish shared agent exchange and model-efficiency protocol | None | `AGENTS.md` and `docs/agent/` created |
| DATA-001 | completed | root/strength_identity | Define strength-set identity across date, session, exercise, set, and source | Product semantics | Five-field PK, transactional legacy migration, source-aware reads/exports, and collision tests passed |
| DATA-002 | backlog | unassigned | Validate finite health values and canonical units | Metric catalog | Reject/normalize invalid inputs and add adversarial tests |
| SESSION-001 | backlog | unassigned | Define append versus replace semantics for edited sessions | DATA-001 | Implement atomically and test stale-set removal |
| ANALYTICS-001 | backlog | unassigned | Define readiness baseline history and source aggregation | DATA-002 | Exclude target-day self-baselines and require documented coverage |
| PLUGIN-001 | in_progress | root/user | Package and connect the first-party OpenWear plugin | ChatGPT developer-mode registration | Manifest and skill validate; obtain generated connection ID, add `.app.json`/marketplace mapping, then run a synthetic chat proof |
| SECURITY-001 | backlog | unassigned | Guard non-loopback serving and remove unnecessary path disclosure | Deployment design | Absolute path disclosure removed; require auth or reject unauthenticated non-loopback serving |
| DEVICE-001 | completed | root | Define the Venu 4 path for the user's iPhone and Windows setup | User device and privacy constraints | First-party official Garmin API is the supported target; Apple Health/iCloud is an optional incomplete fallback |
| SHORTCUT-001 | backlog | unassigned | Build a personal Apple Health Shortcut export proof | DEVICE-001; iCloud Drive setup; DATA-001 | Export bounded rolling-window JSON envelopes with minimum Health/Files permissions |
| INGEST-001 | backlog | unassigned | Build a Windows iCloud drop-folder importer | DEVICE-001; DATA-001 | Validate schema/units/source, deduplicate revisions, record receipts, and quarantine invalid envelopes |
| IOS-001 | backlog | unassigned | Build a native HealthKit bridge only if the Shortcut proof is insufficient | DEVICE-001; iOS signing path | Replace polling snapshots with anchored/background queries when justified |
| CIQ-001 | backlog | unassigned | Probe Venu 4 Connect IQ wellness and OpenWear-owned strength capture only for missing metrics | DEVICE-001; private app install path | Verify exact device fields and background delivery without claiming access to native Garmin history |
| VENDOR-001 | completed | user | Decide whether to use Fitness AI Connector | Vendor audit | Rejected: user wants a first-party OpenWear plugin; nothing installed or authorized |
| LIFTTRACK-001 | completed | user | Decide whether to use LiftTrack | Vendor audit | Rejected: user wants a first-party OpenWear plugin; nothing installed or authorized |
| PROVIDER-001 | backlog | unassigned | Add a provider-neutral ingest contract and synthetic fixtures | DATA-001; DATA-002 | Normalize provenance, timestamps, units, idempotency keys, and receipts without personal data |
| GARMIN-001 | backlog | user/root | Apply for and integrate Garmin Activity and Health APIs | Provider application and privacy/security plan | OAuth once, then push plus reconciliation; never collect Garmin passwords |
