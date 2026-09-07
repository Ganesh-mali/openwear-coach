# OpenWear Coach security model

OpenWear Coach handles sensitive wellness and training data. The current
personal proof is intentionally local, read-only at the MCP client boundary,
and uses synthetic data.

## Preferred local configuration

The project-scoped `.codex/config.toml` starts OpenWear as a child process over
MCP STDIO. This is the safest supported personal setup because it:

- opens no TCP port;
- requires no tunnel, public URL, Platform API key, or extra service;
- stores the SQLite database in the Git-ignored `.local/` directory;
- exposes only coverage, strength recording, strength history, and exercise
  progress to the desktop host; and
- prompts before the write tool records a workout.

Restart the ChatGPT desktop/Codex host, then create a new task inside this
trusted project to load the configuration. Reopening a task that existed before
the configuration change does not rebuild that task's MCP inventory. Expand
`enabled_tools` only after reviewing each tool.

## HTTP development fallback

`scripts/start-local.ps1` exists only for local development and Inspector
testing. The application rejects hostnames, LAN addresses, wildcard addresses,
and privileged ports. It accepts only numeric loopback addresses. The MCP SDK
also validates `Host`, `Origin`, and JSON content type to mitigate browser and
DNS-rebinding attacks. Stop this process when testing is finished.

Do not place the HTTP server behind a tunnel or reverse proxy. It has no user
authentication and is not safe for network exposure.

## Data controls

- Never commit `.local/`, SQLite files, Garmin/Apple exports, device IDs,
  precise location data, tokens, or credentials.
- OpenWear must never collect a Garmin password. A future Garmin integration
  must use Garmin's official OAuth flow and the minimum read-only scopes.
- Treat wearable values as coaching estimates, not medical conclusions.
- Keep raw provider payloads out of logs and error messages.
- Provide explicit export, disconnect, retention, and deletion behavior before
  ingesting provider data.

## Current limitations

- SQLite is not application-encrypted. It relies on the Windows account and
  device storage protections. Do not add real health data until local access,
  backup, and device-encryption expectations are reviewed.
- A process already running as the same Windows user can access user-readable
  files. STDIO removes the network listener but is not an operating-system
  sandbox.
- The current tool allowlist is enforced by the Codex host configuration. The
  underlying server still implements write tools for future controlled use.
- Automatic Garmin ingestion, OAuth token storage, revocation, webhooks,
  replay protection, and provider deletion are not implemented.

## Zero-additional-cost boundary

The selected STDIO path creates no OpenAI Platform API key and uses no Secure
MCP Tunnel. The project will not run a tunnel unless official documentation
explicitly establishes that it is free and the user separately approves it.
Normal use of the user's existing ChatGPT/Codex subscription remains subject
to that subscription's own terms; OpenWear adds no separately billed service.

## Reporting a security issue

Do not include personal health data or credentials in an issue. Report the
minimum reproduction and identify the affected version, transport, and tool.
# Personal file workflow (2026-09-07)

The selected personal route uses supported exports and local processing. There
is no Garmin login, password/token collection, unofficial Garmin dependency,
background account access, or automatic upload. The experimental unofficial
connector was removed before publishing and never authenticated.

Apple XML is parsed with defusedxml; entity expansion and external entities are
rejected. Only selected-source, selected-date supported metrics reach SQLite.
Raw exports may contain extensive sensitive data: keep them in `.local/`, do not
upload them, and review generated Project packs before deliberately sharing.
Git ignores are a convenience, not encryption or access control. SQLite and
exports are not application-encrypted; protect your Windows account and storage.
No software can promise zero security/privacy risk.
