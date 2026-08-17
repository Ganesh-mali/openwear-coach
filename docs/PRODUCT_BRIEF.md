# OpenWear Coach: product and platform brief

Status: pre-alpha decision document, 16 August 2026

Name: provisional; perform trademark and repository-name checks before launch.

## Executive decision

Build our own open-source plugin, but do not begin with direct Garmin cloud sync as the only path.

The viable free product is:

1. a free, local/self-hosted core with SQLite and user-owned imports;
2. an MCP server plus a coaching skill;
3. an optional official Garmin adapter after developer-program approval;
4. an optional hosted community instance only when operating costs and licensing are funded.

This architecture lets contributors run the product without sharing a Garmin password, paying us, or trusting our database. It also avoids making the first release dependent on an external approval process.

## Existing connector audit

The currently listed Fitness AI Connector is useful for validating demand. It should not be forked as our backend foundation.

| Area | Published behavior | Opportunity for our project |
|---|---|---|
| Source availability | Its [GitHub repository](https://github.com/fmp-projects/fitness-ai-connector) publishes a README, license and remote-server manifests, but not the hosted backend implementation. | Publish the complete server, schema, adapters, tests and deployment files. |
| Free history | Its [privacy policy](https://fmp.it.com/en/fitness-ai/privacy/) says the free plan retains two days; the paid plan can retain up to five years. | Keep all local history without a product paywall. |
| Pre-connection history | Its README says refresh skips dates before the user connected. | Use official backfill where approved and always support user-owned export/FIT imports. |
| Tools | Its README documents 12 broad tools. | Add strength-first, coverage, portability and transparent recovery tools. |
| Strength analytics | Activities are presented mainly around running, cycling and swimming. | Model sets, reps, load, RIR, volume, exercise identity and estimated 1RM. |
| Writes | It describes read-only access. | Add an optional, separately authorized workout-publishing adapter. |
| Storage | Its policy describes hosted processing/storage using Auth0, Render, Supabase/AWS and OpenAI. | Default to local SQLite; make remote storage optional and auditable. |
| Portability | No raw-data/local-database workflow is documented. | Give the user import, export and deletion tools from day one. |

The limitation on pre-connection history appears to be product-specific, not a universal Garmin restriction: Garmin's official Health and Activity API pages describe developer backfill tools. Garmin does not publish an unlimited backfill promise, so the adapter must report the actual available range rather than overclaim.

## Platform constraints we must design around

### Garmin

- The [Garmin Connect Developer Program FAQ](https://developer.garmin.com/gc-developer-program/program-faq/) says the program is for approved business/enterprise uses, uses OAuth 2.0, and normally reviews applications within two business days. It says integrations typically take one to four weeks after approval.
- Garmin says general program access has no licensing or maintenance fee, but some metrics or commercial Health API uses may require licensing or minimum device commitments. Therefore a forever-free hosted service cannot be promised before written approval and terms are known.
- The [Health API](https://developer.garmin.com/gc-developer-program/health-api/) exposes sleep, heart rate, stress, Pulse Ox, Body Battery, body composition, respiration and other summaries, and documents backfill tooling.
- The [Activity API](https://developer.garmin.com/gc-developer-program/activity-api/) covers more than 30 activity types including strength training, provides detailed records and supports FIT, GPX and TCX files plus backfill.
- The [Training API](https://developer.garmin.com/gc-developer-program/training-api/) can publish workouts and training plans to Garmin Connect for device sync. This should be opt-in and separately authorized.

### ChatGPT/OpenAI

- OpenAI's [plugin quickstart](https://developers.openai.com/plugins/quickstart) says a plugin can contain MCP capabilities, skills or both. We should ship both.
- OpenAI's [MCP server guide](https://developers.openai.com/plugins/build/mcp-server) requires a durable public HTTPS endpoint for a public listing and OAuth 2.1 for user authentication.
- The [submission guide](https://developers.openai.com/plugins/deploy/submission) also requires verified identity, domain ownership, accurate tool annotations, privacy policy, terms, support details, and positive/negative tool tests.

Local/self-hosted MCP can be free. A public ChatGPT directory app cannot be only a localhost process: it needs a secure hosted endpoint and operations budget.

## Product principles

1. User-owned data: import, export and delete without contacting us.
2. Local first: SQLite is the reference deployment; hosted storage is an optional adapter.
3. No password collection: official OAuth only; never ask for Garmin credentials directly.
4. Exact dates and coverage: every analysis states the date range and missing data.
5. Strength first: progressive overload is a first-class model, not a note attached to cardio activities.
6. Transparent heuristics: readiness outputs its components, weights and coverage.
7. Medical boundary: coaching insight, not diagnosis or treatment.
8. Vendor-neutral core: Garmin is an adapter, not the database schema.

## Architecture

```text
Garmin export / CSV / FIT -----> Import adapters -----+
                                                     |
Official Garmin APIs ----------> Garmin adapter ------+--> Normalized domain --> SQLite
                                                     |                         |
Apple Health / other sources --> Future adapters ----+                         +--> MCP tools
                                                                               +--> Export
                                                                               +--> Coaching skill
                                                                               +--> Optional Garmin Training API write
```

Security boundaries:

- local tools use `openWorldHint: false`;
- the future Garmin adapter uses `openWorldHint: true`;
- read tools use `readOnlyHint: true`;
- imports and local session recording are additive/idempotent writes;
- workout publication is external and must require an explicit confirmation flow;
- public deployment uses per-user OAuth, encryption, rate limits, audit logs and deletion controls.

## MVP tool contract

| Tool | Purpose | Safety |
|---|---|---|
| `get_data_coverage` | Exact ranges, metrics and counts | Local read |
| `get_health_trends` | Dated points and summary changes | Local read |
| `get_daily_readiness` | Transparent recovery heuristic and coverage | Local read |
| `get_strength_sessions` | Session/exercise volume summaries | Local read |
| `get_strength_progress` | Volume, load and e1RM by exact date | Local read |
| `import_health_csv` | Credential-free health import | Local idempotent write |
| `import_strength_csv` | Credential-free set/rep/load import | Local idempotent write |
| `record_strength_session` | Add or update a manual session | Local idempotent write |
| `export_user_data` | Portable dated JSON export | Local read |

Next tools after validation:

- `import_fit_activity`
- `sync_garmin_range`
- `correlate_recovery_with_performance`
- `compare_training_blocks`
- `draft_progression_session`
- `publish_workout_to_garmin`
- `delete_user_data`

## Differentiators worth launching

The launch should be about user value rather than tool count:

- years of user-owned history through imports/backfill where available;
- strength progression with load, volume, RIR and e1RM;
- correlations between sleep/HRV/stress and gym performance;
- local/private mode with no third-party health database;
- auditable formulas and complete source code;
- portable raw/normalized export;
- optional workout push to the watch;
- adapters beyond Garmin.

## Licensing and funding

Recommended initial code license: Apache-2.0. It is permissive and includes an explicit patent grant, which lowers friction for contributors and integrations. Reassess AGPL-3.0 only if preventing closed hosted forks is more important than adoption.

Use “free and open-source core,” not “free forever” for hosted infrastructure. A sustainable public instance can use GitHub Sponsors, Open Collective, grants or capped community sponsorship without putting local data access behind a subscription.

## Roadmap

### Phase 0 — completed in scaffold

- normalized local schema;
- CSV imports;
- strength and readiness calculations;
- initial MCP tool surface and coaching skill;
- dependency-free analytics tests.

### Phase 1 — public developer preview

- select final name and visual identity;
- add Apache-2.0 license, contribution guide, security policy and code of conduct;
- FIT decoder and Garmin export importer;
- golden sample fixtures with anonymized/synthetic data;
- CI, linting, property-based parsing tests and threat model;
- local Docker deployment.

### Phase 2 — official Garmin integration

- apply to Garmin with written use case and privacy architecture;
- implement OAuth, health/activity webhooks and bounded backfill;
- verify strength FIT mappings on multiple watch families;
- publish only Garmin-authorized metrics and attribution.

### Phase 3 — public ChatGPT app

- hosted multi-tenant service and OAuth 2.1;
- privacy policy, terms, support and data-deletion endpoint;
- five positive and three negative tests per OpenAI's submission process;
- domain verification and security review;
- optional Garmin Training API write with explicit confirmation.

## Draft X announcement

> I’m building OpenWear Coach (working name): a free, open-source, local-first MCP plugin for ChatGPT and other AI clients. It will turn user-owned wearable data into strength-training and recovery insights—sets/reps/load, volume, estimated 1RM, sleep/HRV trends, portable exports, and optional Garmin sync after official approval. No password sharing, no paywall around the self-hosted core. Building in public. Which metric or workflow should we support first?

Do not post this until the repository is public, the name is checked, a demo works, and the Garmin wording is approved. Use screenshots based on synthetic data, not personal health data.

## Decisions before public release

1. Final project name and domain.
2. Apache-2.0 versus AGPL-3.0.
3. Local-only preview versus a sponsored hosted beta.
4. Whether write-to-Garmin is launch scope or Phase 3.
5. Which watch model and export samples will be the first compatibility target.
