# Use OpenWear for today's workout

This is the zero-additional-cost personal workflow while automatic Garmin API
access is pending.

## Activate OpenWear

1. Restart the ChatGPT/Codex desktop app after configuration changes.
2. Create a new task inside the `openwear-coach` project.
3. Type `/mcp` and **submit it** with Enter or the send arrow. Text still
   visible in the composer has not been submitted.
4. Confirm `openwear_local` appears.
5. Ask: `Use openwear_local to check my data coverage.`

The project allows four local tools: coverage, record strength session,
strength session history, and exercise progress. Recording is a write and must
prompt for approval. No network port, tunnel, Platform API key, or Garmin login
is used.

## Record a session

During or after training, send a message like:

```text
Record today's OpenWear strength session.
Session ID: workout-2026-08-17-01

Back squat
- 5 reps at 60 kg, RIR 3
- 5 reps at 70 kg, RIR 2
- 5 reps at 75 kg, RIR 1

Bench press
- 8 reps at 40 kg, RIR 3
- 8 reps at 45 kg, RIR 2
```

Review the parsed sets, then approve the `record_strength_session` tool call.
Use the weights and repetitions actually completed. RIR is optional and means
estimated repetitions left in reserve, from 0 to 10.

## Use the Venu 4 today

Record the strength activity on the watch as usual and correct repetitions and
weight on the watch where practical. OpenWear cannot automatically download
that completed Garmin activity until Garmin grants API access and the provider
adapter is implemented.

For a lower-effort bridge today, sync the watch to Garmin Connect, attach clear
screenshots of the completed strength activity to the new OpenWear task, and
ask ChatGPT to extract the sets for review before recording them locally. Do
not include profile, location, device serial, or unrelated health screens.

## Review the workout

Ask:

```text
Show my OpenWear strength sessions for 2026-08-17 and summarize the volume.
```

For one exercise:

```text
Show my bench press progress in OpenWear from 2026-08-17 to 2026-08-17.
```
