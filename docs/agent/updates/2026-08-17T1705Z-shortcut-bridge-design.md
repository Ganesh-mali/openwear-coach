# Agent update — shortcut-bridge-design — 2026-08-17T17:05Z

## Intent

Assess an approval-free, personal iPhone-to-Windows bridge for the user's Venu 4, Garmin Connect, Apple Health, and local OpenWear MCP service. This update is design/research only; no personal data, credentials, or application code was created.

## Evidence

- Garmin documents that Garmin Connect sends the following supported data to Apple Health after each successful device sync: active/resting energy, body-fat percentage, BMI, flights climbed, all-day heart rate, sleep analysis, steps, walking/running distance, water, weight, and uploaded workouts. Workout GPS tracks are not sent. Garmin Connect must be open in the foreground for the Apple Health transfer; the transfer resumes only at the next sync while it is open. Garmin also notes that only high/low HR values are sent for timed activities, so a detailed activity HR graph may be unavailable: <https://support.garmin.com/en-US/?faq=lK5FPB9iPF5PXFkIpFlFPA&searchType=noProduct>.
- Apple Shortcuts has a **Find Health Samples** action. Find actions retrieve their own content when no input is supplied, and support filtering: <https://support.apple.com/en-au/guide/shortcuts/apd3c845e881/ios>.
- A Shortcut can issue `POST`, `PUT`, or `PATCH` HTTP requests, with a JSON, form, or file request body through **Get Contents of URL**: <https://support.apple.com/guide/shortcuts/request-your-first-api-apd58d46713f/9.0/ios/26>.
- iCloud for Windows can sync iCloud Drive to File Explorer. Files under 1 MB download automatically, and the default local path is `C:\Users\[username]\iCloud Drive` (customisable in version 14+): <https://support.apple.com/en-gb/guide/icloud-windows/-icw0144825a5/icloud>.
- iCloud Drive is encrypted in transit and at rest by default. With Advanced Data Protection enabled, iCloud Drive becomes end-to-end encrypted and only trusted devices can decrypt it; account recovery must be configured: <https://support.apple.com/guide/iphone/use-advanced-data-protection-iph584ea27f5/ios>.

## Recommended personal MVP

Use an iCloud Drive drop-folder rather than a LAN HTTP listener for the first personal proof.

```text
Venu 4 -> Garmin Connect on iPhone -> Apple Health
                                       |
                                 personal Shortcut
                                       |
              iCloud Drive/OpenWear-inbox (small encrypted JSON envelopes)
                                       |
              iCloud for Windows -> local OpenWear importer -> SQLite -> MCP -> ChatGPT
```

Why this is the safest practical first route:

- It does not require a Mac, Xcode signing, a public endpoint, router configuration, or an exposed Windows port.
- It retains a user-owned, auditable transfer queue. The Windows importer can move a successfully verified envelope into a local processed/quarantine directory without changing the phone workflow.
- It can be automatic after a one-time consent/setup step. The only unavoidable upstream caveat is Garmin's documented requirement to open Garmin Connect in the foreground for Apple Health delivery.
- Enable Advanced Data Protection before storing health envelopes in iCloud Drive. Without it, iCloud Drive is encrypted but not end-to-end encrypted.

The Shortcut should initially export a deliberately small wellness subset: daily steps, active energy, resting energy, sleep analysis, all-day HR summaries, walking/running distance, and workout summaries. It should not export location, notes, identifiers, or unrelated Health categories. Do not present missing values as zero.

## Automation and incrementality design

1. The user enables the selected Garmin Connect -> Apple Health categories and confirms Garmin is the intended Apple Health source when another app has competing data.
2. The user grants the Shortcut the minimum Health and Files/iCloud access it asks for, then creates a personal automation on a predictable trigger (for example, at an evening time and/or after using Garmin Connect). The trigger should run the Shortcut without confirmation where iOS permits; the exact trigger/run-immediately options must be verified on the user's installed iOS version during setup.
3. The Shortcut uses **Find Health Samples** with a bounded look-back window (initially the current day plus the preceding two days). It writes an immutable, small JSON envelope into `iCloud Drive/OpenWear-inbox/` using a timestamp plus random suffix in the filename.
4. The Windows importer validates schema, size, permitted metrics, timestamps, units, and source label; it then deduplicates/reconciles records before committing them. It records an import receipt (filename/hash/imported-at), not raw personal values, in operational logs.
5. The importer must treat repeated or revised health samples as expected. The bounded look-back is intentional: Garmin/Apple Health can deliver a late sync or revise sleep, while a file-based cursor alone can lose data after an interrupted run. Durable record identity and session replacement semantics remain gated by `DATA-001`.

Do **not** rely on a Shortcut-only last-run cursor as the source of truth. A rolling snapshot plus server-side idempotency is more recoverable. Files should be written under a temporary suffix and renamed only when complete; the Windows importer must ignore temporary/partial files.

## LAN HTTPS alternative

After the file-queue proof works, a local HTTPS endpoint can reduce iCloud latency. It must be HTTPS with a device-held client secret or mutual TLS, replay protection, request-size/rate limits, and no non-loopback access beyond the private LAN. Plain HTTP plus a bearer token is not acceptable for health data. This option adds certificate, iPhone local-network, Windows firewall, discovery, and sleep/reachability complexity, so it is not the recommended first build.

## Coverage boundaries

- This path does **not** provide native Garmin strength sets/reps/weights, GPS tracks, detailed activity HR samples, stress, Body Battery, HRV status, or a guarantee of real-time background delivery. Garmin's documented Apple Health list is the product contract for this MVP.
- Apple Health may merge competing sources by priority. Validate provenance/source metadata where the Shortcut exposes it and avoid double-counting.
- No raw-health export belongs in Git, the agent exchange, tests, or ChatGPT prompts. The MCP layer should return minimized user-requested aggregates rather than automatic raw-history disclosure.
- A custom iOS HealthKit app would offer stronger anchored-query/background behaviour but requires iOS signing/build infrastructure. Apple requires granular health-data authorization and warns that locked devices can prevent background reads from the encrypted HealthKit store: <https://developer.apple.com/documentation/healthkit/protecting-user-privacy>.

## Next safe action

Confirm that the user is willing to use a private iCloud Drive handoff and can install/sign in to iCloud for Windows. Then implement only synthetic-envelope ingestion, idempotency, quarantine, and tests before requesting any actual health export. Build the Shortcut interactively on the user's iPhone only after that import path is verified.

## Efficiency

- Model routing: bounded official-platform research; no billing-token telemetry is available.
- Model review: a Terra/medium implementation is appropriate for the synthetic file importer. Escalate to Sol before any LAN/tunnel security design or real-data threat-model decision.
