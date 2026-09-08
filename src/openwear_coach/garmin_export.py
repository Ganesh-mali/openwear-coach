"""Read only an explicit wellness subset of Garmin's official account export."""
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from .health_metrics import normalize_health_sample
from .models import HealthSample


def read_garmin_export(path: Path) -> list[HealthSample]:
    points = {}
    budget = 0
    with ZipFile(path) as archive:
        for entry in archive.infolist():
            name = PurePosixPath(entry.filename).name
            daily = name.startswith("UDSFile_") and name.endswith(".json")
            sleeping = name.endswith("_sleepData.json")
            if not entry.filename.startswith("DI_CONNECT/") or not (daily or sleeping):
                continue
            budget += entry.file_size
            if budget > 32 * 1024 * 1024:
                raise ValueError("Selected wellness JSON exceeds 32 MiB limit")
            records = json.loads(archive.read(entry))
            if not isinstance(records, list):
                raise ValueError("Unexpected wellness export schema")
            for row in records:
                if not isinstance(row, dict):
                    raise ValueError("Unexpected wellness record")
                day = row.get("calendarDate")
                if not day:
                    continue
                values = []
                if daily:
                    for field, metric, unit in (
                        ("totalSteps", "steps", "count"),
                        ("restingHeartRate", "resting_hr_bpm", "bpm"),
                        ("totalKilocalories", "calories_kcal", "kcal"),
                    ):
                        if row.get(field) is not None:
                            values.append((metric, row[field], unit))
                else:
                    stages = [row.get(key) for key in ("deepSleepSeconds", "lightSleepSeconds", "remSleepSeconds")]
                    if all(isinstance(v, (float, int)) and not isinstance(v, bool) and v >= 0 for v in stages):
                        values.append(("sleep_hours", sum(stages) / 3600, "h"))
                for metric, value, unit in values:
                    if isinstance(value, bool):
                        raise ValueError("Boolean wellness value rejected")
                    item = normalize_health_sample(HealthSample(day, metric, value, unit))
                    key = (item.date, item.metric)
                    if key in points and points[key] != item:
                        raise ValueError("Conflicting daily wellness records require review")
                    points[key] = item
    if not points:
        raise ValueError("No supported wellness observations in export")
    return [points[key] for key in sorted(points)]
