# Agent decision log

Append durable operational decisions only. Product strategy remains in `docs/PRODUCT_BRIEF.md` unless changed.

| Date | Decision | Rationale | Owner | Revisit trigger |
|---|---|---|---|---|
| 2026-08-17 | Use `docs/agent/` plus root `AGENTS.md` as the common exchange. | Files are local, reviewable, versionable, and available to all workspace agents. | root | A real shared service becomes necessary |
| 2026-08-17 | Use one coordinator for shared state; subagents own unique update files. | Prevents concurrent Markdown conflicts and keeps handoffs auditable. | root | Coordination volume exceeds the file workflow |
| 2026-08-17 | Default bounded subtasks to Terra; reserve Sol for high-risk or cross-cutting work. | Matches current official model guidance and avoids spending frontier capacity on mechanical work. | root | Model availability or official guidance changes |
| 2026-08-17 | Track operational proxies, not invented token or billing totals. | Exact per-agent billing telemetry is not exposed in this workflow. | root | Reliable telemetry becomes available |
| 2026-08-17 | Proceed with archive hash `820c3585f3c3798380ab6bf6c9b3a837c0c58bffdc00ba26984702641a3e965a` despite the supplied mismatch. | User explicitly approved proceeding after the integrity warning. | user | A verified replacement archive appears |
| 2026-08-17 | Keep source archive and duplicate extraction out of Git. | They are local transfer/staging artifacts, not project source. | root | User explicitly requests artifact versioning |
