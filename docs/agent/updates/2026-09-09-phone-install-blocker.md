# Phone delivery and official export preparation

## Completed

- Published Shortcut source, native-action privacy checks and coaching prompt.
- Added reusable official Garmin export subset reader and history-pack script.
- Prepared a private local history pack from the user-provided archive. No
  personal measurements, identifiers or filenames are recorded in this exchange.
- Excludes profile/contact, ECG, location and device data; no automatic uploads.
- Full local test command `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
  passed 38 tests, including source references/copy gate and export filtering.
- `.\.venv\Scripts\python.exe scripts/prepare-garmin-history.py <private-export> --out .local/garmin-history-20260909`
  succeeded; retain actual private input path only in the user conversation.

## Signing evidence

Public GitHub macOS runner was tried with Apple's own `/usr/bin/shortcuts sign`.
Run 34291888518 rejected XML/plist input format. Run 34292007875 accepted binary
Shortcut packaging but failed: `In order to do this, you must be signed into iCloud.`
No credentials were collected and no personal files reached the runner.
Removed the failing hosted workflow. Added shortcuts/sign-on-mac.sh for a
one-time run on a Mac already signed into iCloud. Never put Apple credentials
into GitHub, use a signing bypass, or call an unsigned file installable.

## Remaining user step

Asked whether the user can assemble once on iPhone with guidance or use an
already-signed-in Mac once. User chose on-iPhone assembly with guidance. Next inspect and test
the actual Health actions, permission denial and cancellation behavior on phone.
Current snapshot is capped and starts today; not complete daily totals or last
night's sleep. Do not claim the entire mobile product is finished or validated.

## GitHub

Branch agent/initial-openwear-coach; PR #1 open. Source/signing attempt commits
332f23e and 1b8b565 published. Final cleanup/history changes follow those commits.
