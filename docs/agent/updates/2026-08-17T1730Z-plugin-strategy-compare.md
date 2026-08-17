# Agent update — third-party Garmin plugin comparison — 2026-08-17T17:30Z

## Scope

Read-only comparison requested by the coordinator. Evidence is limited to the two user-supplied screenshots and official OpenAI documentation. No account was connected, no third-party terms or privacy policy were opened, and no health data was accessed.

## Screenshot facts

- The ChatGPT Plugin directory search for `garm` shows two public entries: **Fitness AI Connector** (subtitle: “AI coach for your Garmin data”) and **LiftTrack** (subtitle: “Weightlifting For Garmin”).
- The Fitness AI Connector authorization screen says it is an independent app with Garmin-authorized Health API access. Its displayed description claims daily metrics including steps, heart rate, sleep quality, stress and HRV; workout analysis including pace zones, HR-zone distribution and lap splits; and long-term comparisons.
- The consent screen states that, when added, the app receives basic information such as IP address/approximate location and a summary of the recent ChatGPT context and intent. It links to the app’s Terms of Use and Privacy Notice, neither of which was supplied or assessed.

## What OpenAI documents

- A plugin can include apps and skills; apps connect ChatGPT/Codex to external data and actions. Information accessed through an app becomes context ChatGPT can use in its response. [Apps in ChatGPT](https://help.openai.com/en/articles/11487775-apps-in-chatgpt)
- The app’s access is determined by the app, the authorization granted at connection, and workspace controls. App permissions only control when ChatGPT asks before using that access. [Apps in ChatGPT](https://help.openai.com/en/articles/11487775-apps-in-chatgpt)
- A custom OpenWear MCP server can expose its own controlled, goal-focused tools and live data; it must authorize every request for private data. [Build an MCP server](https://developers.openai.com/plugins/build/mcp-server)
- Official docs reviewed do **not** document an API by which one separately installed ChatGPT plugin can programmatically hand its connected-provider data to another plugin/MCP server. Do not design on the assumption that Fitness AI Connector can populate OpenWear’s database.

## Decision comparison

| Dimension | Existing Fitness AI Connector | OpenWear personal bridge |
| --- | --- | --- |
| Fastest way to ask about Garmin metrics in ChatGPT | Likely fastest: add it, complete its Garmin sign-in, and use its exposed tools. | Requires the importer/Shortcut and local-plugin packaging first. |
| Data destination | The screenshot establishes app-to-ChatGPT access, not export to OpenWear. | User-controlled local SQLite is the intended destination. |
| Reuse in OpenWear | No documented app-to-app transfer; treat as unavailable until the provider documents an export/API. | Data contract, retention, deduplication and query tools are controlled by this repository. |
| Garmin coverage | The app claims wider Garmin-native coverage than the Apple Health bridge, but claims need an authenticated validation run. | Apple Health path has the already-recorded documented coverage gaps; later official Garmin API work may expand it. |
| Privacy boundary | Adds a third-party app/operator plus the ChatGPT context described in its consent screen. Its terms, retention, export/deletion policy and Garmin scopes remain unverified. | Avoids Garmin credentials and third-party Garmin processor in the proposed iCloud/Windows design; still requires informed choices about Apple/iCloud and ChatGPT data settings. |
| Portability | Unknown: no export format or deletion/retention guarantee appears in screenshots or official OpenAI docs. | Explicit local export can be built/tested and retained under user control. |

## Threat-model distinction

Using the existing app moves Garmin-authorized data to an independent provider, then exposes relevant results to ChatGPT. The screen itself identifies basic connection metadata and recent ChatGPT context/intent as shared. The open questions are provider-side health-data retention, subprocessors, breach handling, account deletion, Garmin OAuth scopes, and whether the provider can export/delete raw data.

OpenWear changes the acquisition path but not the need for controls: the local importer must validate data and prevent source/session collisions; its MCP tools must minimize returned personal data, authorize requests, and avoid health data in logs. OpenAI’s MCP guidance expressly requires authorization for private data and keeping unnecessary personal data out of tool results/logs.

## Fastest validation experiment (no OpenWear dependency)

1. In the Fitness AI Connector consent flow, inspect the exact Garmin authorization scopes plus its Terms and Privacy Notice before approving.
2. If acceptable, connect it and request a non-sensitive, bounded query such as: “Show yesterday’s step count and sleep duration, with the data source and timestamps.” This validates that the claimed Garmin link works for this account.
3. Ask explicitly whether it supports user data export (CSV/JSON), API access, deletion, and a written retention period. Do not infer any of these from the ChatGPT directory listing.
4. Treat a chat response or copied table as a manual one-off only. It does not establish a secure/reliable integration into OpenWear.

## Recommended position

Use Fitness AI Connector as an optional, rapid *comparison probe* after reviewing its consent and policies. Continue OpenWear for the durable, portable personal data layer. The two can coexist in ChatGPT for separate questions, but OpenWear should not depend on the third-party plugin unless it provides a documented user-authorized export/API with acceptable privacy terms.

## Next safe action

Ask the user whether they want to review/connect Fitness AI Connector for the bounded validation experiment, while separately deciding whether to proceed with the private iCloud/Windows OpenWear proof.
