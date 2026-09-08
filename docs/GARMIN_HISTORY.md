# Initial history from an official Garmin export

An account export is useful once to seed your coaching history. It is not
necessary to repeat the full export for every daily check-in. Fresh measurements
still need the iPhone handoff; exported history cannot update itself.

The local preparation tool reads only daily wellness and sleep JSON from
Garmin's archive, without extracting nested ZIPs. It keeps dated steps, resting
heart rate, total calories and sleep duration. Sleep duration is the sum of
deep/light/REM seconds, only when all three are present. Other metrics and
documents are excluded. Conflicting duplicate measurements fail for review.

Developer/one-time preparation (not a daily phone task):

```powershell
.\.venv\Scripts\python.exe scripts/prepare-garmin-history.py PATH_TO_YOUR_EXPORT.zip --out .local/initial-history
```

The output contains `coach-data.json` and Project/profile instructions. Review
the selected measurements locally before choosing to add the JSON to your
ChatGPT Project. Do not upload the original archive. Its excluded content may
include contacts, profile data, ECG records and other sensitive information.
Do not put a private export or generated history pack into GitHub.

These numerical records remain dated observations, not clinical conclusions.
The current reader does not import strength sets, HRV or Body Battery from the
archive, and does not claim complete coverage of the account.
