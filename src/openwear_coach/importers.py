"""Strict CSV parsers for the credential-free MVP adapter."""

from __future__ import annotations

import csv
import io
from datetime import date

from .health_metrics import normalize_health_sample
from .models import HealthSample, StrengthSet
from .strength_metrics import normalize_strength_set


def _validate_date(value: str) -> str:
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError as exc:
        raise ValueError(f"invalid ISO date: {value!r}") from exc


def parse_health_csv(csv_text: str) -> list[HealthSample]:
    reader = csv.DictReader(io.StringIO(csv_text))
    required = {"date", "metric", "value", "unit"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError(f"health CSV requires columns: {sorted(required)}")

    samples: list[HealthSample] = []
    for line, row in enumerate(reader, start=2):
        try:
            metric = row["metric"].strip().lower()
            unit = row["unit"].strip()
            if not metric or not unit:
                raise ValueError("metric and unit must be non-empty")
            samples.append(
                normalize_health_sample(
                    HealthSample(
                        date=_validate_date(row["date"]),
                        metric=metric,
                        value=float(row["value"]),
                        unit=unit,
                    )
                )
            )
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid health CSV row {line}: {exc}") from exc
    return samples


def parse_strength_csv(csv_text: str) -> list[StrengthSet]:
    reader = csv.DictReader(io.StringIO(csv_text))
    required = {
        "date",
        "session_id",
        "exercise",
        "set_index",
        "reps",
        "weight_kg",
    }
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError(f"strength CSV requires columns: {sorted(required)}")

    items: list[StrengthSet] = []
    for line, row in enumerate(reader, start=2):
        try:
            session_id = row["session_id"].strip()
            exercise = row["exercise"].strip().lower().replace(" ", "_")
            if not session_id or not exercise:
                raise ValueError("session_id and exercise must be non-empty")
            rir_text = (row.get("rir") or "").strip()
            item = StrengthSet(
                date=_validate_date(row["date"]),
                session_id=session_id,
                exercise=exercise,
                set_index=int(row["set_index"]),
                reps=int(row["reps"]),
                weight_kg=float(row["weight_kg"]),
                rir=float(rir_text) if rir_text else None,
            )
            if item.set_index <= 0 or item.reps <= 0 or item.weight_kg <= 0:
                raise ValueError("set_index, reps and weight_kg must be positive")
            if item.rir is not None and not 0 <= item.rir <= 10:
                raise ValueError("rir must be between 0 and 10")
            items.append(normalize_strength_set(item))
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid strength CSV row {line}: {exc}") from exc
    return items
