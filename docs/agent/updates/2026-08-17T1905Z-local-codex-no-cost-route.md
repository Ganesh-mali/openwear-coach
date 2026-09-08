# Agent update — local Codex no-extra-cost route — 2026-08-17T19:05Z

## Scope and result

Read-only audit only. No plugin was installed, no MCP server was started, no
credentials were created, and no authorization or billing action occurred.

The no-extra-cost route is to use the existing OpenWear MCP server directly
from the local ChatGPT/Codex desktop host. It does **not** need Secure MCP
Tunnel, a Platform API key, a public endpoint, or a Garmin connection.

The current package at `plugins/openwear-coach/` is a valid **skills-only**
plugin package: it has `.codex-plugin/plugin.json` and
`skills/strength-coach/SKILL.md`, but no `.app.json` or registered MCP
connection. Therefore it can add coaching instructions through a local
marketplace, but by itself it cannot give the skill access to OpenWear tools.

## Exact safe activation / test path (user action required)

1. Leave Platform billing at $0 and do not create a tunnel, runtime key, or
   external forwarding URL.
2. From the repository with its existing ignored virtual environment active,
   start the server using an explicit isolated synthetic database and its
   loopback default:

   ```powershell
   $env:OPENWEAR_DB = "$PWD\.local\openwear-synthetic.db"
   $env:OPENWEAR_HOST = "127.0.0.1"
   $env:OPENWEAR_PORT = "8000"
   openwear-coach
   ```

   The project server defaults to `127.0.0.1` and has no code path that
   changes the host without `OPENWEAR_HOST`; setting it explicitly is the
   safe proof. Ensure `.local/` stays untracked (the database extension is
   already ignored; directory-wide ignore can be considered by the
   coordinator later).
3. In the **ChatGPT desktop app**: Settings → MCP servers → Add server →
   Streamable HTTP; set a local name such as `OpenWear local` and the URL
   `http://127.0.0.1:8000/mcp`; Save; Restart. This is local-host MCP
   configuration shared with Codex on the same host.
4. In a new Codex task, type `/mcp` and confirm `OpenWear local` appears.
   First test only `get_data_coverage`; an empty isolated database is an
   expected successful result. Do not import health data for this proof.
5. If a coaching workflow is desired, add the existing skills-only package to
   a local marketplace, refresh the desktop app, install it from that local
   marketplace, then create a **new** task and ask a representative prompt.
   The skills-only plugin does not require a `.app.json` or connection ID.
   Adding the MCP connection to the packaged plugin remains deferred until a
   connection is registered; that route uses developer-mode plugin
   connection flow and, for private non-loopback access, potentially a tunnel.

## Evidence

- `src/openwear_coach/server.py`: `main()` uses Streamable HTTP and defaults
  to `OPENWEAR_HOST=127.0.0.1`, `OPENWEAR_PORT=8000`; endpoint is `/mcp`.
- `pyproject.toml`: console command is `openwear-coach`.
- Official OpenAI documentation says the ChatGPT desktop app, Codex CLI, and
  IDE share MCP configuration, and local clients can connect directly to MCP
  servers. It documents Settings → MCP servers → Add server and supports
  Streamable HTTP URLs. [MCP guide](https://learn.chatgpt.com/docs/extend/mcp)
- Official plugin documentation identifies the package as a normal
  skills-only shape and states a local marketplace can install/test it.
  [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- Official tunnel documentation says the tunnel requires both a `tunnel_id`
  and a runtime API key. It is unnecessary when the desktop host can directly
  reach `127.0.0.1`. [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)

## Blocker

No technical blocker for direct local MCP use, provided the server's Python
environment is already installed. The only remaining user action is consent
to add a local server entry and, optionally, to install the local skills-only
plugin. A plugin-integrated MCP connection remains intentionally blocked by
the absent registered connection ID; do not fabricate one.
