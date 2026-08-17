# Agent task ledger

Status values: `backlog`, `in_progress`, `blocked`, `completed`.

| ID | Status | Owner | Scope | Dependencies | Outcome / next step |
|---|---|---|---|---|---|
| OPS-001 | completed | root | Establish shared agent exchange and model-efficiency protocol | None | `AGENTS.md` and `docs/agent/` created |
| DATA-001 | backlog | unassigned | Define strength-set identity across date, session, exercise, set, and source | Product semantics | Add migration-safe schema decision and collision tests |
| DATA-002 | backlog | unassigned | Validate finite health values and canonical units | Metric catalog | Reject/normalize invalid inputs and add adversarial tests |
| SESSION-001 | backlog | unassigned | Define append versus replace semantics for edited sessions | DATA-001 | Implement atomically and test stale-set removal |
| ANALYTICS-001 | backlog | unassigned | Define readiness baseline history and source aggregation | DATA-002 | Exclude target-day self-baselines and require documented coverage |
| PLUGIN-001 | backlog | unassigned | Decide scaffold versus installable plugin packaging | Product decision | Add manifest/dependency mapping or clarify docs |
| SECURITY-001 | backlog | unassigned | Guard non-loopback serving and remove unnecessary path disclosure | Deployment design | Require auth or loopback; avoid exposing absolute DB path |
