"""Read an explicitly selected subset of a local Apple Health XML export."""

from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import median

from defusedxml.ElementTree import iterparse
from defusedxml.common import DefusedXmlException
from xml.etree.ElementTree import ParseError

from .health_metrics import normalize_health_sample
from .models import HealthSample


def parse_apple_health(path: Path, source_name: str, start: str, end: str):
    start, end = date.fromisoformat(start).isoformat(), date.fromisoformat(end).isoformat()
    if start > end or not source_name.strip():
        raise ValueError("choose a non-empty source name and an ordered date range")
    if path.stat().st_size > 1024 * 1024 * 1024:
        raise ValueError("XML exceeds the 1 GiB local import limit")
    groups = defaultdict(list)
    seen = set()
    omitted = 0
    kinds = {
        "HKQuantityTypeIdentifierStepCount": ("steps", "count"),
        "HKQuantityTypeIdentifierRestingHeartRate": ("resting_hr_bpm", "count/min"),
        "HKCategoryTypeIdentifierSleepAnalysis": ("sleep_hours", None),
    }
    try:
        with path.open("rb") as stream:
            context = iterparse(stream, events=("start", "end"), forbid_entities=True, forbid_external=True)
            _, root = next(context)
            if root.tag != "HealthData":
                raise ValueError("expected an Apple HealthData export")
            for event, element in context:
                if event != "end":
                    continue
                if element.tag != "Record":
                    element.clear()
                    continue
                attrs = dict(element.attrib)
                element.clear()
                root.clear()
                if attrs.get("sourceName") != source_name or attrs.get("type") not in kinds:
                    continue
                first = datetime.fromisoformat(attrs["startDate"])
                last = datetime.fromisoformat(attrs["endDate"])
                if first.tzinfo is None or last.tzinfo is None or last < first:
                    raise ValueError("invalid timestamp interval")
                day = last.date().isoformat()
                if not start <= day <= end:
                    continue
                metric, expected_unit = kinds[attrs["type"]]
                if metric == "sleep_hours":
                    # Only complete unsegmented asleep intervals have unambiguous
                    # waking dates. In-bed/awake/stage rows are not sleep totals.
                    if attrs.get("value") not in ("HKCategoryValueSleepAnalysisAsleep",
                                                   "HKCategoryValueSleepAnalysisAsleepUnspecified"):
                        omitted += 1
                        continue
                    value = (last - first).total_seconds() / 3600
                    unit = "h"
                else:
                    if attrs.get("unit") != expected_unit:
                        raise ValueError("unexpected Apple Health unit")
                    if first.date() != last.date():
                        omitted += 1
                        continue
                    value = float(attrs["value"])
                    unit = "bpm" if metric == "resting_hr_bpm" else "count"
                sample = normalize_health_sample(HealthSample(day, metric, value, unit))
                identity = (metric, first, last, sample.value)
                if identity not in seen:
                    seen.add(identity)
                    groups[(day, metric, unit)].append((first, last, sample.value))
    except (DefusedXmlException, ParseError, KeyError, TypeError, StopIteration, ValueError):
        raise ValueError("Apple Health XML rejected: check its schema, timestamps, units and values; no data was written") from None
    samples = []
    for (day, metric, unit), rows in sorted(groups.items()):
        rows.sort()
        if metric == "resting_hr_bpm":
            value = median(row[2] for row in rows)
        else:
            # Exact duplicates were removed. Conflicting overlaps need user review.
            if any(current[0] < previous[1] or current[:2] == previous[:2]
                   for previous, current in zip(rows, rows[1:])):
                raise ValueError("Overlapping Apple Health samples require review; no data was written")
            value = sum(row[2] for row in rows)
        samples.append(normalize_health_sample(HealthSample(day, metric, value, unit)))
    if not samples:
        raise ValueError("No supported samples for that exact source and date range")
    return samples, {"daily_records": len(samples), "omitted_selected_records": omitted,
                     "metrics": sorted({sample.metric for sample in samples})}
