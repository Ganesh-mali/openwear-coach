# Supported Apple Health export route

This path requires no Garmin developer approval and gives OpenWear no Garmin
or Apple credentials. It imports an existing file locally; it does not log in,
scrape a website, call private Garmin endpoints, or upload health data.

## Export from iPhone

1. In Apple Health, open your profile and the app/data-access settings. Select
   Garmin Connect and enable only the categories you want it to write.
2. Sync the watch in Garmin Connect and leave Connect open in the foreground
   while the transfer completes. Check actual dates in Health; availability
   varies by metric and device. Do not assume a successful watch sync means
   every field has reached Apple Health.
3. In Health, tap your profile, then **Export All Health Data**. Save the export
   to a private location you control and transfer it to your Windows laptop.
   iCloud Drive is optional; a supported Files transfer also works. The full
   export can contain much more than Garmin data: do not upload it to GitHub,
   ChatGPT or an online converter.
4. Extract the ZIP locally using Windows and place `export.xml` under this
   repository's ignored `.local/` folder. Keep any original archive private too.

Sources: [Garmin's Apple Health sharing guidance](https://support.garmin.com/en-US/?faq=lK5FPB9iPF5PXFkIpFlFPA),
[Apple's Health export instructions](https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios).

## Validate and import

Use the exact `sourceName` from the XML for Garmin's entries (often `Connect`).
Inspect that attribute locally if no records match; do not share the full XML.
Select only the date range you want the coach to use:

```powershell
.\.venv\Scripts\python.exe -m openwear_coach.cli import-apple-health .local/export.xml --source-name "Connect" --start 2026-09-01 --end 2026-09-07 --dry-run
.\.venv\Scripts\python.exe -m openwear_coach.cli import-apple-health .local/export.xml --source-name "Connect" --start 2026-09-01 --end 2026-09-07
```

The receipt shows the generated source ID, daily record count, metrics and
omitted selected records, without printing measurements. Use that source ID
for subsequent MCP health queries. Complete the [Project-pack workflow](USE_NOW.md).
Keep a separate database for each person: a source name identifies an app,
not a person.

## Exact supported subset

| Apple record | Stored value | Policy |
|---|---|---|
| StepCount | steps/day | Sum non-overlapping same-day intervals; exact duplicates removed |
| RestingHeartRate | resting HR/day | Median of unique same-day resting-HR samples |
| SleepAnalysis Asleep/AsleepUnspecified | sleep hours | Whole asleep intervals assigned to local waking date |

Conflicting overlaps fail the import for review. In-bed, awake and individual
sleep-stage rows are omitted; they are not reliable whole-night totals in this
small adapter. Cross-midnight quantity intervals are omitted rather than split
by an invented distribution. Unsupported records, GPS, clinical information,
names and device metadata are not stored. XML entity expansion and external
entities are blocked. The importer accepts XML up to 1 GiB, not ZIP files.

Garmin may not write all three supported types into Health. Do not substitute
ordinary heart rate for resting HR, or Apple SDNN HRV for Garmin nightly HRV.
For missing sleep totals, Garmin HRV, stress, Body Battery and strength sets,
use the dated manual CSV workflow. The importer reports only data actually
present; no-data is never treated as zero.

Refresh by exporting and importing again. Identical keys update without
duplication; absent keys are not deleted. This is a supported **file export**
workflow, not background watch-to-ChatGPT synchronization. No scheduler, account
connector or third-party fitness plugin is installed by this project.
