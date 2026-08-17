# Agent update — local MCP/plugin contract review — 2026-08-17T18:05Z

## Scope and evidence

Read-only review of `pyproject.toml`, `src/openwear_coach/server.py`, `README.md`, `plugin/skills/strength-coach/SKILL.md`, the named prior handoff update, and the official OpenAI plugin packaging page. No package installation, server launch, or health-data access was performed.

## Exact current local launch contract (Windows)

- The installed console entry point is `openwear-coach` (`pyproject.toml`: `[project.scripts] openwear-coach = "openwear_coach.server:main"`). On this host's existing virtual environment it resolves to `.venv\\Scripts\\openwear-coach.exe`.
- `python -m openwear_coach.server` reaches the same `main()` only when run by the interpreter that can import the installed `openwear_coach` package (for this checkout, `.venv\\Scripts\\python.exe` after `pip install -e .`). The console entry point is the clearer packaged launch contract.
- `main()` calls `mcp.run("streamable-http", host=..., port=..., stateless_http=True, json_response=True)`. Defaults are `OPENWEAR_HOST=127.0.0.1` and `OPENWEAR_PORT=8000`; the MCP URL is therefore `http://127.0.0.1:8000/mcp`. The database defaults to `%USERPROFILE%\\.openwear-coach\\data.db`, unless `OPENWEAR_DB` is set before process startup.
- The existing skill is valid source content but is outside an installable plugin package; it has no manifest or MCP mapping.

## Bundled `.mcp.json` determination

Not with the server unchanged. OpenAI's documented bundled-server shape is command plus `args: ["--stdio"]` (or equivalent wrapped `mcp_servers` map): <https://developers.openai.com/plugins/build/plugins>. The current `openwear-coach` command has no `--stdio` mode and always serves HTTP, so a command-spawned `.mcp.json` could start a listener but would not speak MCP over the spawned process's stdio. It is not a valid bundled-MCP launch configuration for this implementation.

To support a bundled `.mcp.json`, add and test an explicit stdio transport/CLI switch, then configure the virtual-environment executable (for example `openwear-coach --stdio`) and a deterministic `OPENWEAR_DB` location. Otherwise retain the HTTP server and use a registered connection through `.app.json`.

## ChatGPT developer-mode registration still required

For the existing HTTP route, start the local server first, enable ChatGPT Developer mode, add an MCP connection using `http://127.0.0.1:8000/mcp` (or the local URL actually reachable from the ChatGPT client), and copy the generated technical ID beginning `plugin_asdk_app`. The plugin needs `.codex-plugin/plugin.json` plus a root `.app.json` mapping that ID; the manifest's `apps` field must point to `./.app.json`. A repo-scoped `.agents/plugins/marketplace.json` is then needed to install/test locally. This is the official local workflow: <https://developers.openai.com/plugins/build/plugins>.

Do not commit a private connection ID. A loopback endpoint is suitable for local developer-mode testing only; public submission requires a stable public HTTPS streamable-HTTP endpoint, not a local endpoint or temporary tunnel: <https://developers.openai.com/plugins/build/mcp-server>.

## Startup/import concerns

- No Python import defect is evident statically: the console script points at `main`, and imports are package-qualified. The previous audit records package-safe Inspector imports as already fixed.
- The README's Quick start is POSIX-only and incorrect as Windows guidance: `. .venv/bin/activate` and `export OPENWEAR_DB=...` do not work in PowerShell, and `cd openwear-coach` assumes a parent directory rather than this repository root. Document PowerShell equivalents before presenting it as a Windows setup path.
- Importing `openwear_coach.server` has a side effect: its module-global `Database(_database_path())` creates the parent directory/database and initializes schema. Set `OPENWEAR_DB` before any import/launch during tests so local default-path state is not created unexpectedly.

## Next safe action

Choose one transport deliberately: preserve Streamable HTTP and complete the developer-mode `.app.json` registration, or implement/test a distinct stdio mode before adding `.mcp.json`. Use the console script as the Windows packaged command; do not infer that it supports stdio today.
