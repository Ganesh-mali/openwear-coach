# Agent update — LiftTrack / “Weightlifting For Garmin” plugin audit — 2026-08-17T17:35Z

## Scope and naming

- The screenshot’s second result is **LiftTrack — Weightlifting For Garmin**, not “LiftTracz.”
- This audit covers that result only. The separately listed **Fitness AI Connector** is a different ChatGPT app (developer shown as FMP in its public listing) and needs its own audit before installation.
- Evidence is public/vendor-published unless explicitly labelled “user-supplied screenshot.” Claims are not an independent security review.

## Identity and availability — verified

- Public ChatGPT app listing: `https://chatgpt.com/apps/lifttrack/asdk_app_6999ccabf45481919788bd190c6be537` (search-indexed as version 1.0.0; developer **LiftTrack, LLC**; support `support@lifttrackapp.com`). The live URL may redirect to the ChatGPT plugin catalogue without a signed-in session.
- Product website: `https://lifttrackapp.com/`.
- Apple’s US App Store lists seller/developer **LiftTrack LLC** and copyright **© 2025 Evan Noble**. Google Play lists **Lifttrack LLC**, support email/telephone, and the developer address `2108 N St Ste N, Sacramento, CA 95816-5712, United States`.
- The public privacy notice identifies “Lift Track,” lists a San Francisco mailing address, and is last updated **2024-08-21**. The differing product spelling/address are a documentation-consistency concern, not proof of wrongdoing.

## What it appears to do — verified product claims

- LiftTrack is principally a cloud/mobile strength-workout planner, not a general Garmin-health-data connector. Its flow is: create a strength workout in LiftTrack -> sync it through Garmin Connect to the watch -> follow Garmin’s native Strength workout -> completed workout results sync back to LiftTrack.
- It reads completed strength-workout information sufficiently to show sets, reps, weights, rest time and duration; it writes/pushes workout definitions to Garmin Connect/watch. Its FAQ also says it finds the Garmin-uploaded Strava activity and **updates its title and description**, so it is not read-only.
- The ChatGPT app says ChatGPT can access live LiftTrack workout templates and completed sessions for questions about prior workouts, progression and schedule. It does **not** publicly promise access to Garmin wellness metrics (sleep, HRV, stress, Body Battery, all-day HR) or generic FIT/GPS history.
- App Store release notes say a user can copy a past workout as plain text and that iOS supports sharing workout/exercise CSVs. This is a limited, user-initiated interoperability feature; no documented full-account export or standard data-portability endpoint was found.

## Venu 4 — verified compatibility inference

- LiftTrack’s FAQ says it supports modern Garmin watches with the native Strength app, including the Venu series, rather than listing Venu 4 individually.
- Garmin’s Venu 4 manual verifies that Venu 4 can receive Garmin Connect strength workouts, record sets/reps/weight, and sync saved activities. Garmin’s compatibility table also lists Venu 4 for Strength Coach.
- Therefore LiftTrack’s described strength-workout flow should be compatible with Venu 4, subject to current app/device/account setup. This is an inference from the two vendors’ published compatibility descriptions, not a LiftTrack device-specific guarantee or a real-device test.

## Permissions, authentication, and ChatGPT data direction

- **Garmin OAuth scopes/consent text: not publicly published/found.** Do not assume the minimum scope. Before authorizing, inspect the actual Garmin consent screen and record whether it can read activities, write workouts, and/or access profile data. The observed product behaviour establishes write access to workouts and read-back of completed strength activities, but not the exact API scopes, token lifetime, revocation behaviour or scope separation.
- **ChatGPT connector direction:** its listing describes ChatGPT reading live LiftTrack templates/completed sessions. Current product materials/release notes show LiftTrack’s own AI coach can edit/delete workouts, but the public ChatGPT listing does not document whether ChatGPT can invoke those writes. Treat the ChatGPT plugin as read-only until its connected-tool consent/tool descriptions prove otherwise.
- **User-supplied screenshot:** the ChatGPT add dialog says the app receives basic web information (IP and approximate location) plus a summary of the current ChatGPT context/intent relevant to a request. It also warns that apps can introduce elevated risk. This is ChatGPT platform disclosure, not LiftTrack’s own privacy policy.

## Privacy, retention, deletion — policy claims and gaps

- LiftTrack’s policy says it collects account/contact/authentication data and automatic device/usage/log data; it says information is used for service delivery, administration, communication, security/fraud and legal compliance. It allows business-transfer sharing and says service providers may receive data under contracts.
- The policy says it retains personal information while an account exists unless a longer legal period applies; after no ongoing need, it says it deletes/anonymizes, with backups isolated until deletion is possible. It permits access/correction/deletion requests by email, while retaining some data for fraud, troubleshooting, investigations, legal terms and law.
- The policy says it does **not** process sensitive personal information, but it never explicitly names Garmin data, workout data, health data, Strava data, ChatGPT data, or the ChatGPT plugin. That mismatch means it is not a sufficient assurance for health-data handling.
- Apple’s developer privacy label says contact info, user content and identifiers may be linked to the user; usage/diagnostics may be collected, and usage data may track users across other companies’ apps/sites. Google Play’s developer-provided declaration says it may collect/share personal info, app activity and two other categories, encrypts data in transit, and accepts deletion requests. Neither disclosure supplies Garmin scopes, encryption-at-rest, a health-data retention schedule, backup-deletion timetable, or a subprocessor list.
- No public GDPR/UK representative, DPA, breach process, exact deletion SLA, raw-data export, or Garmin-token revocation procedure was located. These are unknown, not evidence that they do not exist privately.

## Pricing — verified public storefront information (region/time dependent)

- Free tier: up to three workouts, manual scheduling and core features (vendor listing).
- Premium: unlimited workouts and automatic scheduling (vendor listing).
- US App Store currently lists monthly **US$7.99** and yearly options of **US$49.99** and **US$59.99** (duplicate/legacy price entries visible); do not assume the discounted annual price until shown in the purchaser’s store. UK/other regions vary.
- ChatGPT app listing does not state a separate plugin price. Treat ChatGPT access as included only after checking the LiftTrack in-app subscription/paywall and plugin consent screen.

## Recommendation for this user

1. LiftTrack is a credible *strength-workout* shortcut if the user accepts a third-party cloud service and wants planned workouts written to the Venu 4. It does not replace OpenWear’s intended local-first, general Garmin health-data path.
2. Do not connect it merely to obtain sleep/HRV/stress/Body Battery data: its public scope is much narrower.
3. Before clicking Connect, capture the Garmin and LiftTrack authorization pages, check write permissions, choose an account with no unnecessary profile sharing, and identify the unlink/delete path. Ask LiftTrack support for exact Garmin scopes, data categories, storage region/at-rest encryption, retention/backups, ChatGPT tool write capabilities, and full export/deletion procedure.
4. If installed, test on a disposable workout template first. Confirm it sends only the expected workout, that Venu 4 receives it, and what completed data appears in LiftTrack/ChatGPT before using real history.

## Sources

- LiftTrack product site and FAQ: <https://lifttrackapp.com/>, <https://lifttrackapp.com/faq/>
- LiftTrack privacy notice: <https://lifttrackapp.com/privacy-policy/>
- Apple App Store listing: <https://apps.apple.com/us/app/lifttrack-strength-training/id6736655105>
- Google Play listing: <https://play.google.com/store/apps/details?id=com.lifttrack.liftTrack>
- Garmin Venu 4 strength manual: <https://www8.garmin.com/manuals-apac/webhelp/venu4/EN-SG/GUID-D15CEE9A-318C-4205-AE73-9094277325FC-4158.html>
- Garmin Venu 4 plan compatibility: <https://support.garmin.com/en-GB/?faq=pVtmVTZz7C97GZHxtMWgs8>

## Validation

- Public-web/source audit only; no account was created, no connector was authorized, and no user health data was transmitted.
- Exact shell validation: `Get-Content docs/agent/updates/2026-08-17T1735Z-lifttrack-plugin-audit.md`

## Next safe action

- Coordinator can compare this isolated strength-planning option with Fitness AI Connector; do not recommend either as a privacy-verified replacement for the proposed local OpenWear bridge without consent-screen evidence.
