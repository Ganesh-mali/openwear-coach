# Agent update — plugin audit — 2026-08-17T16:40Z

## Scope

Read-only audit of the repository's current ChatGPT/Codex plugin pieces and the minimum wiring required for a locally installable OpenWear Coach plugin.

## Current repository state

- `src/openwear_coach/server.py` is a working local Streamable HTTP MCP server. It exposes nine focused local-data tools, binds to `127.0.0.1:8000` by default, and advertises server instructions plus tool safety annotations.
- `pyproject.toml` packages the server as the `openwear-coach` command and depends on the Python `mcp` SDK.
- `plugin/skills/strength-coach/SKILL.md` is a valid reusable coaching workflow: it tells ChatGPT/Codex which existing MCP tools to call, requires exact dates and coverage checks, and applies non-medical safety constraints.
- The repository has **no** `.codex-plugin/plugin.json`, `.app.json`, `.mcp.json`, or `.agents/plugins/marketplace.json`. Thus its skill and server are separate source assets, not an installable ChatGPT/Codex plugin.
- The current server's default loopback URL is suitable for local development, but a ChatGPT developer-mode MCP connection must be registered explicitly before a ChatGPT plugin can reference it.

## Official packaging model

OpenAI describes an MCP server as the component that exposes live data and controlled tools to ChatGPT/Codex; a skill supplies repeatable instructions for using those tools. Plugin packaging groups these pieces under a stable identity. Every plugin requires `.codex-plugin/plugin.json`; a plugin can additionally include `skills/`, `.app.json` for a registered MCP connection, `.mcp.json` for a bundled MCP server, and optional assets/hooks. Sources: <https://developers.openai.com/plugins/build/mcp-server> and <https://developers.openai.com/plugins/build/plugins>.

## Minimum local-installable shape for this project

For the current Streamable HTTP server, use a connection-backed plugin:

```text
plugins/openwear-coach/
  .codex-plugin/plugin.json       # required identity; points at skills and .app.json
  .app.json                       # maps to the ChatGPT developer-mode plugin_asdk_app... connection
  skills/strength-coach/SKILL.md  # move/copy existing workflow here
.agents/plugins/marketplace.json  # exposes the local plugin in ChatGPT desktop
```

Required out-of-repository user action for ChatGPT: enable Developer mode, create the MCP connection from the local server URL in ChatGPT Plugins, then obtain the generated `plugin_asdk_app...` ID. That ID belongs in `.app.json`; it must not be committed if it identifies a private connection. OpenAI's documented local flow then installs the plugin from a repository or personal marketplace after restarting ChatGPT desktop.

For Codex-only local testing, an alternative is a bundled `.mcp.json` that starts the installed `openwear-coach` command. Its exact command/environment contract must be validated on this Windows host; do not add it until the package installation and database-path behaviour are decided.

## Recommended sequencing

1. Finish `DATA-001` identity/integrity work before any real health-data bridge.
2. Preserve the existing MCP server and skill; package them after the iPhone-to-Windows ingestion boundary is defined.
3. Use the `plugin-creator` skill to scaffold the manifest and local marketplace entry; it is OpenAI's documented fast path.
4. Register and test the local MCP connection, then test one new ChatGPT conversation for coverage, trends, and strength progression with synthetic data only.

## Validation performed

```powershell
rg --files -g '!openwear-coach-prealpha/**' -g '!openwear-coach-prealpha.tar.gz' | rg '(^plugin/|SKILL\\.md$|server|pyproject|README|\\.mcp\\.json$|\\.app\\.json$|plugin\\.json$|marketplace\\.json$)'
```

Result: only `plugin/skills/strength-coach/SKILL.md`, `src/openwear_coach/server.py`, `pyproject.toml`, and README references exist; no plugin manifest, MCP-connection mapping, or marketplace catalog was found.

## Next safe action

Once the personal iPhone ingestion choice is accepted, have the coordinator use `plugin-creator` to create the package and marketplace wiring, then ask the user to perform the one-time Developer mode/MCP connection registration. Do not expose a health-data server beyond loopback or commit connection identifiers.
