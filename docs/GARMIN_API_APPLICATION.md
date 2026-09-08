# Garmin Connect Developer Program application package

OpenWear Coach is a first-party, privacy-first physical wellbeing and training
coach. It is an open-source pre-alpha, currently being validated with a
consenting Garmin Venu 4 owner on iPhone and Windows. It is not a medical
device, does not diagnose or treat conditions, does not sell health data, and
does not collect Garmin passwords.

## Requested evaluation scope

- **Health API:** daily sleep, heart rate/resting heart rate, steps, intensity
  minutes, calories, stress, Body Battery, Pulse Ox and respiration, limited
  to metrics available for the consenting device/user.
- **Activity API:** completed strength-training activities and their original
  activity data, to reconcile workout history with local strength coaching.
- **Access model:** Garmin OAuth 2.0 consent, Push as the preferred delivery
  model with reconciliation/backfill; no screen scraping or credential sharing.

OpenWear will implement explicit consent, scoped collection, encrypted token
storage, idempotent ingestion, deletion/disconnect handling, provenance, and
an export path before any production release. Raw personal health data, device
identifiers, locations and credentials are never committed to Git.

## Questions for Garmin

1. Is an early-stage business eligible for a Health plus Activity API evaluation
   integration intended initially for a small private beta?
2. Which of the requested Venu 4 metrics are available in the Health API
   evaluation feed, particularly sleep, resting HR, HRV-related data, stress,
   Body Battery, Pulse Ox and respiration?
3. Can Health and Activity feeds be enabled together for the same application?
4. What data-processing, security, business-entity and production-readiness
   requirements apply before evaluation and before production approval?
5. Are there any evaluation, licence, minimum-device-order or other fees for
   the requested scope? Please identify them before any commercial commitment.

## Draft email

**To:** `connect-support@developer.garmin.com`

**Subject:** Request for Garmin Connect Health + Activity API evaluation — OpenWear Coach

Hello Garmin Connect Developer Program team,

I am developing OpenWear Coach, an early-stage, first-party physical wellbeing
and strength-training coach. Our initial validation is with a consenting Garmin
Venu 4 user who syncs through Garmin Connect on iPhone. We are building a
privacy-first experience: users authorize through Garmin OAuth 2.0; OpenWear
will not collect Garmin credentials; and we will minimize, protect, export and
delete health data on request.

We would like to request evaluation access to the Garmin Connect Health API and
Activity API. The intended Health scope is all-day summaries needed for
wellbeing coaching: sleep, heart rate/resting heart rate, steps, intensity
minutes, calories, stress, Body Battery, Pulse Ox and respiration where
available. The Activity scope is completed strength-training activities and
their original activity data, used to improve workout-history and recovery
coaching.

OpenWear is not a medical device and will not use Garmin data for diagnosis,
treatment, insurance decisions, employee monitoring, advertising or data sale.
We are implementing explicit user consent, least-privilege data selection,
encrypted token handling, idempotent delivery processing, revocation/deletion,
and user data export before any production release.

Could you please confirm whether an early-stage business/private beta is
eligible for Health plus Activity API evaluation access, which requested Venu 4
metrics are available, and the exact evaluation and commercial requirements or
fees? We will not proceed with any paid commercial commitment without reviewing
those terms.

Project repository: https://github.com/Ganesh-mali/openwear-coach

Thank you,

`[Your full name]`

`[Company/legal entity name]`

`[Country]`

`[Contact phone]`

`[Contact email]`

## Submission checklist

Before sending email or submitting the Garmin Health enquiry form, replace only
the five bracketed contact fields above. Confirm the company/legal entity name
is accurate. Do not include Garmin credentials, screenshots, raw health exports,
device serial numbers, precise location, passport/identity documents or payment
details.

The Garmin Health enquiry form currently requests company name, country/region,
phone number and a free-text message. The final submit action sends those
personal/business contact details to Garmin and needs the owner's confirmation.

## Evidence

- [Garmin Connect Developer Program FAQ](https://developer.garmin.com/gc-developer-program/program-faq/)
  says the program is for business use, uses OAuth 2.0, responds to applications
  within two business days, and may require licence fees or minimum device order
  quantities for some commercial metrics.
- [Garmin Health API](https://developer.garmin.com/gc-developer-program/health-api/)
  lists the requested all-day metrics, Push/Ping-Pull architectures, an
  evaluation environment after approval, and states commercial use requires a
  licence fee payment.
- [Garmin Activity API](https://developer.garmin.com/gc-developer-program/activity-api/)
  describes completed activity data, including strength training.
