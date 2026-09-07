# Handoff

Updated: 2026-09-07 (Europe/London)

## Goal and current result

User asked to finish the Garmin personal coach, update GitHub and make it usable.
The supported Apple Health export/manual local workflow is implemented and
tested. The user selected account safety over full automation. No developer
approval, Garmin login or unofficial account connector is part of this route.

## Next pickup

1. Read STATUS.md.
2. Read only updates/2026-09-07T1940Z-ready-local-workflow.md.
3. Run `git -c safe.directory=C:/Users/GANESH/open_source_projects/openwear-coach status -sb`.
4. Follow docs/USE_NOW.md to import user-reviewed dated observations and build
   a personal Project pack. Do not use synthetic demo records as user measurements.

## Repository

Branch: agent/initial-openwear-coach. Existing PR: #1 into main.
The source archive and duplicate extraction remain untracked intentionally.
Never stage them, databases, generated packs, .venv, caches or metadata.

## Boundaries

No Garmin passwords, scraping, third-party fitness plugins, extra Platform
charges, health-data uploads or Garmin application submission without the
appropriate user authorization. The official application is historical and is not a prerequisite; do not
resume it unless explicitly requested. No actual health
records were imported in the readiness phase. The file workflow does not need
MCP host loading, an API key, a tunnel, or an external service.

## Ownership

Root owns READY-001 and coordination files. No delegated agents are active.
Remaining publishing/docs work fits Terra/low; automatic-provider privacy and
identity architecture warrants Sol under the repository policy.
