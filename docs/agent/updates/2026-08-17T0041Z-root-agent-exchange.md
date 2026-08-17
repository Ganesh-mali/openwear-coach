# Agent update — root — 2026-08-17T00:41Z

## Intent

Create a durable, low-token collaboration exchange and a model-efficiency review policy for future agents.

## Evidence and findings

- No existing `AGENTS.md` or coordination folder was present.
- Official OpenAI model guidance assigns Sol to complex work and Terra to balanced cost/capability work.
- Exact per-agent billing-token telemetry is not exposed, so the ledger uses operational proxies.
- Three bounded design/curation subtasks completed successfully on `gpt-5.6-terra` with low reasoning.

## Changes

- Added root `AGENTS.md`.
- Added canonical status, handoff, task, decision, efficiency, and exchange protocol files under `docs/agent/`.
- Added a unique per-agent update convention to avoid concurrent write conflicts.

## Validation

- Cross-file paths and branch/PR facts were checked after creation.
- A Terra/low subagent cold-audited the exchange.
- Pickup was reduced to `HANDOFF.md`, `STATUS.md`, and one update file after the root instructions.

## Next step or blocker

Persist the documentation on the current draft-PR branch, then begin `DATA-001` when requested.

## Efficiency

- Model / reasoning: coordinating root plus Terra/low subagents
- Context scope: medium
- Planned / actual tool calls: not exposed
- Model review: future bounded maintenance should use Terra
