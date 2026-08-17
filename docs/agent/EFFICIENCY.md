# Agent efficiency ledger

> Directional operational record only. This is not an OpenAI billing or exact token-usage statement.

[Official OpenAI model guidance](https://developers.openai.com/api/docs/models) currently positions Sol for complex professional/coding work, Terra for balanced intelligence and cost, and Luna for cost-sensitive high-volume work. This environment currently exposes Sol and Terra for subagents.

## Routing policy

| Work type | Default | Escalate or prompt when |
|---|---|---|
| Inspect, search, summarize, test, documentation, mechanical edit | Terra / low | Evidence conflicts or scope becomes architectural |
| Ordinary implementation or reproduced bug | Terra / medium | One grounded attempt fails or risk expands across modules |
| Security, privacy, data integrity, architecture, final integration | Sol / medium+ | Sol is justified; keep scope narrow |

Use the lowest reasoning effort that can complete the work. Do not escalate merely to produce longer prose.

## Model-switch prompt triggers

Prompt the user at a phase boundary when any apply:

- Sol is handling work that has become bounded or mechanical.
- More than two exploratory turns occur without a narrowed hypothesis.
- The same large context is repeatedly re-read.
- A Terra attempt produced conflicting evidence or exposed security/data-integrity risk.
- Tool calls materially exceed the plan.

Use this format:

`Model switch recommendation: <current> -> <suggested>. Reason: <one sentence>. Trade-off: <one sentence>.`

## Ledger

Use `not exposed` rather than guessing unavailable values.

| Date | Agent / task | Status | Model / effort | Context scope | Planned tools | Actual tool calls | Turns | Outcome / evidence | Model review |
|---|---|---|---|---|---:|---:|---:|---|---|
| 2026-08-17 | efficiency_auditor | completed | gpt-5.6-terra / low | Recent request + repo coordination state | bounded | not exposed | 1 | Produced routing policy and proxy schema | Terra appropriate |
| 2026-08-17 | exchange_architect | completed | gpt-5.6-terra / low | Repo docs, Git state, and new exchange files | bounded | not exposed | 2 | Designed the exchange and cold-audited three-file pickup | Terra appropriate |
| 2026-08-17 | context_curator | completed | gpt-5.6-terra / low | Repo and confirmed PR context | bounded | not exposed | 1 | Produced resumable project snapshot | Terra appropriate |
| 2026-08-17 | Garmin automatic-sync research | completed | gpt-5.6-terra / medium subagents | Official Garmin, Apple, Android, open-source bridge, and OpenAI MCP sources | bounded parallel research | not exposed | 1 each | Ruled out Windows BLE and Android-only paths for the user's iPhone; identified HealthKit + Connect IQ boundary | Terra appropriate; Sol retained for privacy synthesis |
| 2026-08-17 | windows_bridge_check | completed | gpt-5.6-terra / low | Windows install state and local plugin wiring | bounded read-only checks | not exposed | 1 | Confirmed iCloud for Windows absent and plugin packaging incomplete | Terra appropriate |
| 2026-08-17 | shortcut_bridge_design | completed | gpt-5.6-terra / medium | Official Apple/Garmin automation, security, and coverage evidence | bounded research | not exposed | 1 | Designed iCloud drop-folder personal proof and recovery-safe rolling import | Terra appropriate |
| 2026-08-17 | current_plugin_audit | completed | gpt-5.6-terra / low | Repo MCP/skill/package state plus official plugin model | bounded read-only audit | not exposed | 1 | Identified exact plugin packaging/connection gap | Terra appropriate |
| 2026-08-17 | plugin_strategy_compare | completed | gpt-5.6-terra / low | Screenshots plus official OpenAI plugin model | bounded read-only comparison | not exposed | 1 | Separated hosted proof from durable OpenWear ingestion | Terra appropriate |
| 2026-08-17 | fitness_ai_connector_audit | completed | gpt-5.6-terra / medium | Vendor legal/privacy/tool claims plus official Garmin API context | bounded vendor audit | not exposed | 1 | Identified read-only coverage, retention, subprocessors, deletion and verification gaps | Terra appropriate; Sol reserved for adoption/privacy decision |
| 2026-08-17 | lifttracz_audit | completed | gpt-5.6-terra / medium | Vendor listings, privacy, device compatibility and pricing | bounded vendor audit | not exposed | 1 | Identified strength read/write scope and privacy-documentation gap | Terra appropriate |
| 2026-08-17 | plugin_contract_review | completed | gpt-5.6-terra / low | MCP launch, Windows setup, and ChatGPT mapping contract | bounded read-only review | not exposed | 1 | Confirmed HTTP-only connection path and generated-ID gate | Terra appropriate |
| 2026-08-17 | first_party_plugin | completed | gpt-5.6-terra / medium | New plugin package and existing skill | bounded scaffold/edit/validate | not exposed | 1 | Created first-party manifest and packaged skill without fabricated MCP IDs | Terra appropriate |
| 2026-08-17 | strength_identity | completed | gpt-5.6-sol / high | SQLite identity, migration, and collision tests | bounded high-risk data change | not exposed | 1 | Migrated to source/date-safe identity; 10-test suite passed | Sol justified for data integrity; switch to Terra for wiring |
| 2026-08-17 | root first-party integration | completed | coordinator / model telemetry not exposed | Plugin docs, source propagation, privacy redaction, validators, MCP smoke | focused integration | not exposed | 1 | Plugin and skill validators passed; nine tools discovered; no vendor installed | Remaining plugin wiring is Terra/medium work |
| 2026-08-17 | final_change_review | completed | gpt-5.6-terra / medium | Current first-party/plugin and DATA-001 diff | bounded read-only review | not exposed | 1 | No code blocker; confirmed explicit staging is required to exclude transfer artifacts | Terra appropriate |
| 2026-08-17 | local_codex_route | completed | gpt-5.6-terra / low | Existing plugin, local transport, and official setup docs | bounded read-only audit | not exposed | 1 | Identified direct desktop loopback MCP as the no-extra-cost route; skills-only package needs a separate MCP connection | Terra appropriate |
| 2026-08-17 | root zero-cost routing | completed | coordinator / model telemetry not exposed | Platform billing state, official billing/tunnel docs, and local route | focused decision and documentation | not exposed | 1 | Deferred runtime key/tunnel client; selected local desktop proof with synthetic data | Sol-level cost/privacy synthesis justified; remaining local wiring is Terra/medium |
| 2026-08-17 | root local transport hardening | completed | coordinator / model telemetry not exposed | Local MCP transport, threat model, tests, and project config | focused implementation and validation | not exposed | 1 | Preferred STDIO with one-tool allowlist; loopback HTTP fail-closed; 17 tests and both transport smokes passed | Sol justified for security boundary; next work can use Terra/medium |
| 2026-08-17 | root local wellbeing mode | completed | coordinator / model telemetry not exposed | Health metric integrity, provenance, readiness semantics, MCP wiring and safety skill | focused implementation and validation | not exposed | 1 | Canonical validation, source-isolated baselines, 21 tests, two skill validators and MCP health smoke passed | Sol justified for health-data integrity; bounded provider fixtures can use Terra/medium |
| 2026-08-17 | root Garmin evaluation package | completed | coordinator / model telemetry not exposed | Official Garmin FAQ, Health API and contact form | focused browser research and documentation | not exposed | 1 | Verified business/OAuth/fee constraints and prepared a truthful application package without transmitting data | Sol appropriate for provider/privacy wording; submission is user-confirmation gated |

## Limitations

- Tool calls and turns are not token counts.
- Prompt, completion, reasoning, cached-token, tool-fee, and subscription usage may be unavailable.
- Do not convert proxy fields into monetary savings.
- Model availability and app entitlements can differ from API documentation.
