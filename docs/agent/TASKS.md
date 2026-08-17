# Agent task ledger

Status values: `backlog`, `in_progress`, `blocked`, `completed`.

| ID | Status | Owner | Scope | Dependencies | Outcome / next step |
|---|---|---|---|---|---|
| OPS-001 | completed | root | Establish shared agent exchange and model-efficiency protocol | None | `AGENTS.md` and `docs/agent/` created |
| DATA-001 | completed | root/strength_identity | Define strength-set identity across date, session, exercise, set, and source | Product semantics | Five-field PK, transactional legacy migration, source-aware reads/exports, and collision tests passed |
| DATA-002 | completed | root | Validate finite health values and canonical units | Metric catalog | Canonical catalogue, unit normalization, finite/range/source validation and adversarial tests passed |
| SESSION-001 | backlog | unassigned | Define append versus replace semantics for edited sessions | DATA-001 | Implement atomically and test stale-set removal |
| ANALYTICS-001 | completed | root | Define readiness baseline history and source aggregation | DATA-002 | Source-specific reads; target excluded; 7-sample prior baseline requirement documented and tested |
| PLUGIN-001 | in_progress | root/user | Run the first-party OpenWear desktop-local wellbeing flow | New task created after desktop restart | Seven-tool STDIO configuration and MCP health smoke pass; submit `/mcp`, verify coverage, then approve a dated screenshot-derived health import |
| WEB-PLUGIN-001 | backlog | root/user | Map OpenWear to a ChatGPT web plugin | User permits separately billed Platform route and generated connection ID | Deferred under the hard no-extra-charge requirement; never fabricate an ID |
| SECURITY-001 | completed | root | Guard non-loopback serving and remove unnecessary path disclosure | Deployment design | Path redacted; preferred STDIO opens no port; HTTP rejects non-loopback/hostname/privileged binds and SDK guards Host/Origin |
| DEVICE-001 | completed | root | Define the Venu 4 path for the user's iPhone and Windows setup | User device and privacy constraints | First-party official Garmin API is the supported target; Apple Health/iCloud is an optional incomplete fallback |
| SHORTCUT-001 | backlog | unassigned | Build a personal Apple Health Shortcut export proof | DEVICE-001; iCloud Drive setup; DATA-001 | Export bounded rolling-window JSON envelopes with minimum Health/Files permissions |
| INGEST-001 | backlog | unassigned | Build a Windows iCloud drop-folder importer | DEVICE-001; DATA-001 | Validate schema/units/source, deduplicate revisions, record receipts, and quarantine invalid envelopes |
| IOS-001 | backlog | unassigned | Build a native HealthKit bridge only if the Shortcut proof is insufficient | DEVICE-001; iOS signing path | Replace polling snapshots with anchored/background queries when justified |
| CIQ-001 | backlog | unassigned | Probe Venu 4 Connect IQ wellness and OpenWear-owned strength capture only for missing metrics | DEVICE-001; private app install path | Verify exact device fields and background delivery without claiming access to native Garmin history |
| VENDOR-001 | completed | user | Decide whether to use Fitness AI Connector | Vendor audit | Rejected: user wants a first-party OpenWear plugin; nothing installed or authorized |
| LIFTTRACK-001 | completed | user | Decide whether to use LiftTrack | Vendor audit | Rejected: user wants a first-party OpenWear plugin; nothing installed or authorized |
| PROVIDER-001 | backlog | unassigned | Add a provider-neutral ingest contract and synthetic fixtures | DATA-001; DATA-002 | Normalize provenance, timestamps, units, idempotency keys, and receipts without personal data |
| GARMIN-001 | in_progress | user/root | Apply for and integrate Garmin Activity and Health APIs | User contact/business details and action-time submission confirmation | Evaluation application package prepared; OAuth once, then push plus reconciliation; never collect Garmin passwords |
