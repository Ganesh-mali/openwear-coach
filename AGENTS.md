# OpenWear Coach agent protocol

This repository uses `docs/agent/` as its file-based coordination exchange.

## Before starting work

1. Read `docs/agent/HANDOFF.md`.
2. Read `docs/agent/STATUS.md`.
3. Read only the single update file named by the handoff.
4. Consult `TASKS.md` or `DECISIONS.md` only when the handoff links a required row or a decision is unclear.
5. Reserve overlapping work through the coordinator before editing the same paths.

## During work

- Keep one owner per task and file set.
- Subagents write only a uniquely named update file; the coordinating agent owns `STATUS.md`, `HANDOFF.md`, `TASKS.md`, `DECISIONS.md`, and `EFFICIENCY.md`.
- Record evidence, changed files, exact validation commands, results, blockers, and the next safe action.
- Never store secrets, credentials, access tokens, raw personal health exports, or unnecessary command output in coordination files.
- Do not stage `openwear-coach-prealpha.tar.gz`, `openwear-coach-prealpha/`, `.venv/`, caches, databases, or generated package metadata.
- Git may require `git -c safe.directory=C:/Users/GANESH/open_source_projects/openwear-coach ...` in this environment.

## Model and token-efficiency policy

- Default bounded inspection, tests, summaries, documentation, and mechanical edits to `gpt-5.6-terra` with low reasoning.
- Use Terra with medium reasoning for ordinary implementation or a clearly reproduced bug.
- Use `gpt-5.6-sol` for security/privacy decisions, data-integrity design, ambiguous cross-module failures, architecture, or final synthesis.
- Exact billing-token telemetry is not available to repository agents. Track the proxies in `docs/agent/EFFICIENCY.md`; never invent token counts or cost savings.
- At a meaningful phase boundary, prompt the user with `Model switch recommendation: <from> -> <to>` when the remaining work has become mechanical or when a cheaper attempt has failed and risk now justifies Sol.

## Handoff

Before stopping, write a unique update file and have the coordinator refresh `STATUS.md`, `TASKS.md`, `HANDOFF.md`, and the efficiency ledger. After the automatically discovered `AGENTS.md`, the next agent should need at most three exchange files.
