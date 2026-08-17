# Agent update — zero-cost local MCP decision — 2026-08-17T19:35Z

## Outcome

The user set a hard requirement: OpenWear must not create an additional paid
OpenAI charge. The proof path is therefore direct loopback MCP in the local
ChatGPT desktop/Codex host, using an empty synthetic SQLite database.

The selected URL is `http://127.0.0.1:8000/mcp`. It needs no public endpoint,
Garmin login, Platform API key, Secure MCP Tunnel client, or health-data
transfer. The first proof must call only `get_data_coverage`.

## Platform preflight and boundary

- ChatGPT web rejected the loopback URL as unsafe.
- A Platform tunnel was created during the preflight and associated with the
  personal workspace, but it is unused.
- No runtime API key was created; its prepared form requested only Tunnels Read
  and Use permissions, but the final creation action was not taken.
- No tunnel client was downloaded or run; no credits were bought; auto-reload
  remains off; no health data or Garmin account was accessed.

OpenAI states that ChatGPT and API Platform billing are separate. Its Secure
MCP Tunnel guide requires a Platform runtime API key but does not state a
price. Prepaid billing documentation warns that cutoffs can be delayed. That
evidence is insufficient for a strict zero-cost promise, so the tunnel route
is deferred.

## Changed files

- `.gitignore` — ignores the local synthetic-data directory.
- `docs/FIRST_PARTY_PLUGIN.md` — documents the direct desktop path and defers
  the web/tunnel path.
- `docs/agent/HANDOFF.md`, `STATUS.md`, `TASKS.md`, `DECISIONS.md`, and
  `EFFICIENCY.md` — record the decision and next safe action.

## Next safe action

With the user's action-time consent, start the loopback MCP server using an
isolated synthetic database, add it in ChatGPT desktop/Codex as a Streamable
HTTP MCP server, restart the desktop host, and call only
`get_data_coverage`. Optionally delete the unused Platform tunnel only with
the user's explicit approval.

## Sources

- [OpenAI billing separation](https://help.openai.com/en/articles/9039756)
- [OpenAI prepaid-billing behavior](https://help.openai.com/en/articles/8264644-how-do-i-cancel-my-chatgpt-plus-subscription)
- [Secure MCP Tunnel requirements](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
- [Desktop-local MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)
