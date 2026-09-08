# Agent update — Fitness AI Connector public audit — 2026-08-17T17:35Z

## Scope and conclusion

Read-only audit of the public ChatGPT plugin shown in the user screenshot: **Fitness AI Connector**. It is a real ChatGPT Apps Directory listing and a hosted remote MCP service, operated by **FMP**. It may be a fast personal-use alternative to OpenWear, but it is not local-first: health data is sent to the operator and then to the selected AI platform.

The evidence supports that it uses the kind of official Garmin Connect Developer Program integration it claims, but it does **not** publicly prove that Garmin has specifically approved or endorsed FMP/Fitness AI Connector. The service itself expressly says it is not affiliated with, endorsed, or sponsored by Garmin.

## Verified public identity and availability

- ChatGPT Apps Directory listing: [Fitness AI Connector](https://chatgpt.com/apps/fitness-ai-connector/asdk_app_69beacb8780c81919104bb111b56346b). The listing identifies the developer as **FMP**, version 1.0.0, and support email `contact@fmp.it.com`.
- Operator website: [FMP Fitness AI Connector](https://fmp.it.com/en/fitness-ai/). The public repository links to the same site and documents a remote Streamable HTTP endpoint.
- Public source/registration metadata: [GitHub repository](https://github.com/fmp-projects/fitness-ai-connector) and [server manifest](https://github.com/fmp-projects/fitness-ai-connector/blob/main/server.json). The repository contains service metadata and documentation, not the hosted service implementation.
- Legal identity is limited in public disclosure: FMP states it is a **sole proprietor**, gives a trade name and `contact@fmp.it.com`, and says the person's name, address, and phone number are disclosed on request. See [commercial disclosure](https://fmp.it.com/en/commercial-transaction/). Therefore, no public corporate-registration verification was found.
- A third-party community registry labels the publisher unverified and the source community-indexed. This is not proof of wrongdoing, but it is not an identity assurance either: [Forge listing](https://forgeregistry.com/registry/io.github.fmp-projects%2Ffitness-ai-connector).

## Garmin authorization: claims vs. what can be verified

| Statement | Evidence level | Finding |
| --- | --- | --- |
| Uses Garmin Health/Activity/Women's Health APIs | Provider claim; technically consistent with Garmin docs | FMP says it obtains data through those APIs. Garmin documents that those official APIs provide the listed general categories after user consent and device sync: [Health API](https://developer.garmin.com/gc-developer-program/health-api/), [Activity API](https://developer.garmin.com/gc-developer-program/activity-api/), [Women's Health API](https://developer.garmin.com/gc-developer-program/womens-health-api/). |
| User signs in on Garmin's page via OAuth 2.0 + PKCE | Provider claim; OAuth 2.0 is independently consistent | FMP describes a Garmin consent screen and says Garmin passwords are not shared. Garmin confirms Developer Program APIs use OAuth 2.0: [Program FAQ](https://developer.garmin.com/gc-developer-program/program-faq/). I did not complete an OAuth authorization or inspect its scopes. |
| Garmin approved FMP specifically | Not verified | No Garmin-owned partner-directory entry or approval record naming Fitness AI Connector/FMP was located. Garmin says access follows approval, but that only establishes the general program process. |
| Garmin endorses the service | Contradicted by provider disclaimer | FMP's repository says it is not affiliated with, endorsed, or sponsored by Garmin. |

## Account and consent flow

Based on FMP's public setup instructions, connection is two stages:

1. Add the ChatGPT plugin (or use its Custom GPT) and sign into a Fitness AI account using email/password or Google.
2. Follow an FMP `.../garmin/link` URL, sign in to Garmin on Garmin's consent page, and select **Allow**. FMP says later use is automatic and Garmin can be disconnected in Garmin Connect settings.

FMP says one Garmin account can be linked to only one Fitness AI login at a time, and support can remove an old link after identity verification. See [FAQ/setup](https://fmp.it.com/en/fitness-ai/).

## Claimed scopes, metrics, and limits

FMP's privacy policy says it collects heart rate, sleep/stages/score, HRV, stress, activities, VO2max, Body Battery, and (only with Garmin sharing enabled) menstrual-cycle or pregnancy-related data. It also lists email from Auth0 and Stripe-managed billing information. [Privacy policy](https://fmp.it.com/en/fitness-ai/privacy/)

The published MCP documentation claims 12 tools: profile/status, daily health summary, activities, activity detail, body composition, cycle data, trends, refresh, missing-detail refetch, subscription/deletion, help, and Garmin-source acknowledgement. Detailed activity responses can include time-series data only on request. [Tool list](https://github.com/fmp-projects/fitness-ai-connector)

Important boundaries stated by FMP:

- It is read-only for Garmin; it says it cannot write/change a Garmin account.
- Data starts from the connection date; it says pre-connection history cannot be retrieved even if Historical Data is enabled.
- Free plan keeps a two-day range; Basic keeps up to five years. It says Free does not retain detailed activity data for a later paid upgrade.
- It says third-party automatic imports (for example, a linked Zwift account) do not reach partner services; device-recorded or manually uploaded activities do.
- The Plugin (v2) does **not** expose menstrual-cycle data according to FMP's ChatGPT setup page; its Custom GPT does. [Connection-method comparison](https://fmp.it.com/en/fitness-ai/setup/chatgpt-mcp/)

## Storage, sharing, retention, deletion, and portability

These are FMP contractual/privacy-policy statements, not independently audited security guarantees:

- Stored encrypted on Supabase in AWS US East; EU/EEA transfers are said to use SCCs.
- Listed subprocessors: Garmin, Auth0, Stripe, Anthropic, OpenAI, Supabase, and Render. The policy says Garmin health data is provided to OpenAI/Anthropic over MCP; handling after that depends on the selected platform, account, and settings.
- Free retention: 2 days. Basic retention: up to 5 years while subscribed. Following paid cancellation, data is held 30 days; then older data is removed under Free rules.
- Account deletion: health data deleted within 30 days. Account identifiers (email/auth/payment IDs) and legally required payment/transaction records are retained. Disconnecting Garmin must be done separately in Garmin Connect; deleting the FMP account does not itself revoke Garmin access.
- The policy grants a right to receive data in a structured format by emailing `contact@fmp.it.com`, but public documentation does not describe a self-service raw-data export/API endpoint. MCP is the documented interoperability surface.
- FMP says data are encrypted in transit/at rest, access controlled, and security-reviewed; no public SOC 2/ISO report or independent audit was found.

Sources: [privacy policy](https://fmp.it.com/en/fitness-ai/privacy/), [terms](https://fmp.it.com/en/fitness-ai/terms/).

## Price and commercial terms

- Free: $0, two days of data.
- Basic: $3/month, five years of data, monthly renewal through Stripe.
- Cancellation is said to take effect for the next billing cycle; refunds are generally not provided.
- FMP reserves the right to change plans/pricing with notice; the English terms say Japanese text controls if translations differ and select Japanese law/Tokyo jurisdiction, subject to applicable consumer protections.

Sources: [pricing](https://fmp.it.com/en/fitness-ai/#pricing), [terms](https://fmp.it.com/en/fitness-ai/terms/), [commercial disclosure](https://fmp.it.com/en/commercial-transaction/).

## Recommended user decision

For a quick exploratory test, this is a reasonable candidate **only if the user accepts** an FMP-hosted US data store plus downstream disclosure to ChatGPT. Before allowing Garmin consent, inspect the exact consent screen and disable Women's Health/Historical Data unless wanted.

For the OpenWear goal (personal data minimization, Windows-local database, and transparent importer), retain the proposed iPhone Shortcut -> iCloud Drive -> local Windows importer route. That path still requires an explicit decision about iCloud Drive, but avoids sending a continuous full Garmin feed to a new third-party hosted service.

## Work performed

- No repository code or shared coordination files changed.
- No external accounts connected; no consent screens accepted; no credentials, health data, device IDs, or OAuth tokens collected.
- Validation: read public ChatGPT listing, FMP website/legal documents, GitHub manifest/repository, and official Garmin Developer Program documentation on 2026-08-17.

## Next safe action

Coordinator can present the privacy trade-off and ask whether the user prefers (a) installing/testing Fitness AI Connector personally, or (b) continuing the local OpenWear bridge. If they choose the connector, the user—not an agent—must complete each authentication/consent action.
