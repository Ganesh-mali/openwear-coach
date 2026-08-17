# Agent update — root — 2026-08-17T16:22Z

## Intent

Define the safest approval-free route from the user's Garmin Venu 4 to OpenWear after confirming that the watch is paired with Garmin Connect on an iPhone.

## Evidence and findings

- Garmin Connect can write active energy, heart rate, sleep, steps, distance, weight, and generic workouts to Apple Health after a successful device sync. Garmin documents that Connect must be open in the foreground for this transfer to complete: <https://support.garmin.com/en-US/?faq=lK5FPB9iPF5PXFkIpFlFPA&searchType=noProduct>.
- Garmin does not document Apple Health delivery of HRV, stress, Body Battery, or native strength sets/reps/weights. OpenWear must report those coverage gaps rather than infer them.
- An OpenWear iOS companion can read user-approved HealthKit types and receive background updates, subject to iPhone lock/background timing. HealthKit keeps its local store encrypted and requires granular permission and a privacy policy: <https://developer.apple.com/documentation/healthkit/protecting-user-privacy>.
- A Venu 4 Connect IQ sidecar can read selected current/device-local history such as heart rate, stress, and Body Battery where supported, then send compact deltas. It cannot read native Garmin Strength history, sleep stages, or HRV status as a general API: <https://developer.garmin.com/connect-iq/api-docs/Toybox/SensorHistory.html>.
- Connect IQ can record OpenWear-owned strength sessions, but the user must start the OpenWear activity instead of expecting access to Garmin's native Strength activity records.
- No documented approval-free Windows BLE API exposes arbitrary Venu 4 history. USB/MTP requires a cable and remains a manual fallback.
- Gadgetbridge is Android-only and therefore is not the primary route for this user's current setup.
- Unofficial Garmin Connect clients are not an acceptable product path: they require Garmin account secrets or fragile tokens, and the previously common Garth flow was deprecated after an authentication change.
- ChatGPT/Codex can be the coaching interface through OpenWear MCP tools, but it is not the watch transport. Raw records should stay local; only explicitly requested, minimized summaries should be returned to a cloud model.

## Recommended architecture to validate

1. Venu 4 syncs normally to Garmin Connect on iPhone.
2. Garmin Connect writes its supported subset to Apple Health.
3. An OpenWear iOS companion reads only authorized HealthKit types and keeps an encrypted local cursor/store.
4. The companion synchronizes over an authenticated, encrypted local channel to the user's Windows OpenWear service when reachable.
5. An optional Venu 4 Connect IQ sidecar supplies supported Garmin-only wellness deltas and records OpenWear-owned strength sessions.
6. The Windows service remains the primary database, dashboard, analytics, and MCP endpoint. Raw health data is not published or committed.

## Blockers and product boundaries

- Need the user's agreement to install an OpenWear iPhone companion and a private/beta Venu 4 Connect IQ app.
- Need an iOS signing/distribution path: access to macOS/Xcode for direct device testing, or an Apple Developer Program membership plus a secure macOS CI/TestFlight workflow. Apple documents free Xcode testing on one's own devices and a USD 99/year membership for TestFlight/distribution: <https://developer.apple.com/programs/>.
- Apple Health alone cannot satisfy full-fidelity Garmin strength/recovery requirements.
- Fully automatic native Garmin history without opening Garmin Connect still requires the approved Garmin Activity/Health APIs.

## Next safe action

Confirm the iOS build/distribution capability and willingness to install both companion components. Then specify a non-production proof of concept for HealthKit workout/sleep/heart-rate ingestion and a separately scoped Connect IQ capability probe, without ingesting real health data into Git.

## Efficiency

- Model routing: Terra/medium subagents handled bounded platform research; root retained architecture/privacy synthesis.
- Exact token and billing telemetry: not exposed.
- Model review: use Terra/medium for a bounded proof-of-concept after the architecture is accepted; reserve Sol for the privacy threat model and cross-device trust design.
