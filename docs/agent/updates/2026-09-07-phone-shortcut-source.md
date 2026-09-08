# iPhone Shortcut source

## User direction

No PC for daily use, no separate iPhone app. User confirmed Garmin Connect
already writes to Apple Health and requested a Shortcut handoff to ChatGPT.
Supported account-safe path remains mandatory. No developer approval or
unofficial Garmin login. Project selection and sending are deliberate.

## Delivered locally

- shortcuts/build_shortcut.py and OpenWear Check-in.unsigned.plist.
- shortcuts/README.md: phone-only assembly guide, exact coverage and pending checks.
- shortcuts/PROJECT_PROMPT.md: coverage/source-aware coaching instructions.
- README points to the phone prototype rather than implying Windows is daily use.

The generated workflow reads up to 50 samples each of Steps, Resting Heart Rate
and Sleep starting today. All dates/source/value/unit/duration are retained in
text. It previews and separately confirms before local-only clipboard copying.
It contains no network, file-write or Health-write actions. It does not compute
daily totals, last-night sleep, readiness or provider identity from missing data.

## Validation

`.\.venv\Scripts\python.exe shortcuts/build_shortcut.py` passed.
Python plistlib round-trip and inline static assertions passed: action allowlist,
unique UUIDs, three bounded Health queries, balanced repeat groups, cancel-enabled
gate before clipboard, local-only copying. `git diff --check` passed.
These checks DO NOT verify iOS import/runtime, permission UI or Health results.

## Blocker and next safe action

Windows host has no iPhone control or Apple Shortcuts signing executable.
Do not offer the unsigned plist as an installable download, fabricate an iCloud
install link, use a signing bypass, or claim the Shortcut has been installed.
On-phone assembly or legitimate Apple signing plus first-run verification is
still required. Ask for an editor screenshot without measurements to guide setup.
Do not claim Ask ChatGPT routes into a Project; review/copy/manual Project paste
is the selected handoff. No personal data was accessed or shared.
