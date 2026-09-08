# Agent exchange

This directory is the common, Markdown-based exchange for human and agent collaborators. It is operational context, not a billing system or a place for user data.

## Sources of truth

| File | Purpose | Write policy |
|---|---|---|
| `STATUS.md` | Canonical project snapshot and next three actions | Coordinator replaces stale facts |
| `HANDOFF.md` | Immediate pickup instructions | Coordinator overwrites at handoff |
| `TASKS.md` | Task ownership, dependencies, and outcomes | Coordinator maintains rows |
| `DECISIONS.md` | Durable ADR-lite decisions | Append-only |
| `EFFICIENCY.md` | Model routing and token-cost proxies | Coordinator updates at handoff |
| `updates/*.md` | Per-agent evidence and work log | Each agent owns one unique file |

## Low-token pickup sequence

1. Read `HANDOFF.md`.
2. Read `STATUS.md`.
3. Read only the single update named by the handoff.
4. Consult task or decision rows only when the handoff explicitly links them.
5. Inspect source files only after the handoff identifies them.

## Conflict avoidance

- One coordinator owns the shared state files.
- Use one task owner and one non-overlapping file set at a time.
- Name updates `YYYY-MM-DDTHHMMZ-agent-task.md`.
- Subagents report findings in their own update; the coordinator consolidates shared state.
- Keep `STATUS.md` under roughly 100 lines and `HANDOFF.md` under roughly 60 lines.

## Update template

```md
# Agent update — <agent> — <UTC timestamp>

## Intent

## Evidence and findings

## Changes

## Validation

## Next step or blocker

## Efficiency

- Model / reasoning:
- Context scope: small | medium | large
- Planned / actual tool calls: use `not exposed` when unavailable
- Model review: no | suggest Terra | suggest Sol
```
