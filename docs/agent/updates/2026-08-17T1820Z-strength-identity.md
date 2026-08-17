# Agent update — DATA-001 strength identity — 2026-08-17T18:20Z

## Outcome

Implemented the conservative strength-set identity change in the assigned storage
slice. New and migrated tables now use `(date, source, session_id, exercise,
set_index)` as the primary key. Re-importing that exact identity updates only
`reps`, `weight_kg`, and `rir`; identity fields are never rewritten by conflict
handling.

Legacy tables keyed by `(session_id, exercise, set_index)` are rebuilt inside an
explicit SQLite transaction. All rows are copied and counted before the original
table is replaced. An unrecognized primary-key shape fails closed instead of
attempting a destructive migration.

Session replacement behavior was not changed.

## Changed files

- `src/openwear_coach/storage.py`
- `tests/test_storage_and_imports.py`
- `docs/agent/updates/2026-08-17T1820Z-strength-identity.md`

## Test coverage added

- Identical session/exercise/set identifiers coexist across dates and sources.
- An exact-identity replay updates payload fields and remains a single row when
  repeated.
- A populated legacy table migrates to the five-field identity without losing
  stored values or nullable `rir` data.

## Validation

- `$env:PYTHONPATH='src'` then `python -m unittest tests.test_storage_and_imports -v`
  — 6 tests passed.
- `$env:PYTHONPATH='src'` then `python -m unittest discover -s tests -v`
  — 10 tests passed.
- An initial `python -m unittest tests.test_storage_and_imports -v` did not run
  tests because the system Python did not have this `src` layout on its import
  path; the source-path-explicit commands above are the valid repository checks.

## Blockers and next safe action

No blocker in this slice. The coordinator can review the migration semantics,
mark DATA-001 complete if accepted, and proceed without treating this as a
decision on SESSION-001 replacement semantics.
