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

## Limitations

- Tool calls and turns are not token counts.
- Prompt, completion, reasoning, cached-token, tool-fee, and subscription usage may be unavailable.
- Do not convert proxy fields into monetary savings.
- Model availability and app entitlements can differ from API documentation.
