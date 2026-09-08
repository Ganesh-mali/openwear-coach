# Use OpenWear for wellbeing today

This is the zero-extra-cost, local workflow while automatic Garmin access is
being developed. Health records stay in the Git-ignored `.local/` SQLite file.
The MCP process uses STDIO and opens no network port.

## Activate the tools

1. Restart Codex desktop after pulling this project update.
2. Create a **new task** inside this trusted project. Reopened old tasks retain
   their old MCP tool inventory.
3. Submit `/mcp` and confirm `openwear_local` is enabled.
4. Ask: `Check my OpenWear data coverage.`

The enabled wellbeing tools are `import_health_csv`, `get_health_trends` and
`get_daily_readiness`. Imports require approval; read-only queries do not.

## Record today's Garmin observations

After the Venu 4 syncs to Garmin Connect on the iPhone, attach dated screenshots
of the Garmin Connect Sleep, Heart Rate, HRV Status, Stress/Body Battery and
Pulse Ox/Respiration pages. Steps and active minutes are also useful. Crop out
your name, profile image, location, maps and device serial number.

Ask ChatGPT:

> Extract only clearly visible dated values from these screenshots. Show me the
> proposed OpenWear CSV first. Do not infer missing values. After I approve it,
> call `import_health_csv` with source `garmin_screenshot`.

The approved CSV will use this shape:

```csv
date,metric,value,unit
2026-08-17,sleep_hours,7.4,h
2026-08-17,sleep_score,82,score
2026-08-17,resting_hr_bpm,55,bpm
2026-08-17,hrv_ms,48,ms
2026-08-17,stress,24,score
2026-08-17,body_battery,71,score
2026-08-17,respiration_rate_brpm,14.2,breaths/min
2026-08-17,spo2_percent,97,%
2026-08-17,steps,9400,count
2026-08-17,active_minutes,52,min
```

These are example values, not your data. OpenWear rejects unknown metrics,
wrong units, non-finite numbers and values outside broad physiological/device
ranges. It also keeps `garmin_screenshot`, `apple_health` and future provider
feeds separate.

## Ask for coaching

Useful prompts after import:

- `Show my sleep, resting heart rate and HRV trends for 2026-08-10 through 2026-08-17 from garmin_screenshot.`
- `Calculate my 2026-08-17 readiness from garmin_screenshot and explain its coverage.`
- `Combine today's recovery coverage with my recent strength sessions and suggest a conservative workout.`

HRV and resting-HR readiness components require at least seven earlier samples
from the same source. The target day is excluded from its own baseline. Missing
data is reported and never converted to zero.

## Automatic collection roadmap

The supported full-fidelity route is the official Garmin Health and Activity
APIs: Venu 4 → Garmin Connect on iPhone → Garmin cloud → OpenWear after one-time
OAuth consent. Access is approval-gated and Garmin says commercial Health API
use requires a licence fee, so it cannot currently be promised under the
zero-extra-cost requirement.

The no-fee interim automation candidate is a small first-party iPhone bridge
that reads Garmin-written Apple Health records after HealthKit permission and
sends them to the local OpenWear adapter. Garmin's Apple Health export covers
only a subset and requires Garmin Connect to be opened in the foreground to
transfer data. We must validate exact Venu 4 coverage before relying on it.

Official references:

- [Garmin Health API](https://developer.garmin.com/gc-developer-program/health-api/)
- [Garmin Connect data shared with Apple Health](https://support.garmin.com/en-US/?faq=lK5FPB9iPF5PXFkIpFlFPA&searchType=noProduct)
- [Apple HealthKit background delivery](https://developer.apple.com/documentation/HealthKit/HKHealthStore/enableBackgroundDelivery%28for%3Afrequency%3AwithCompletion%3A%29?language=objc)

## Safety boundary

OpenWear is a wellbeing and training coach, not a medical device. Wearable
values can be noisy and must not be used to diagnose or treat a condition.
Persistent unusual readings or symptoms warrant a qualified healthcare
professional. Chest pain, fainting, severe breathlessness or stroke signs call
for urgent local emergency help, not workout coaching.
