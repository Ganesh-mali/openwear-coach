"""Canonical health metric validation for local imports and storage."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import date

from .models import HealthSample


@dataclass(frozen=True)
class MetricSpec:
    unit: str
    minimum: float
    maximum: float
    aliases: frozenset[str]


def _spec(unit: str, minimum: float, maximum: float, *aliases: str) -> MetricSpec:
    return MetricSpec(unit, minimum, maximum, frozenset({unit, *aliases}))


HEALTH_METRICS: dict[str, MetricSpec] = {
    "sleep_hours": _spec("h", 0, 24, "hour", "hours"),
    "sleep_score": _spec("score", 0, 100),
    "resting_hr_bpm": _spec("bpm", 20, 250, "beats/min"),
    "average_hr_bpm": _spec("bpm", 20, 250, "beats/min"),
    "min_hr_bpm": _spec("bpm", 20, 250, "beats/min"),
    "max_hr_bpm": _spec("bpm", 20, 300, "beats/min"),
    "hrv_ms": _spec("ms", 1, 500, "millisecond", "milliseconds"),
    "stress": _spec("score", 0, 100),
    "body_battery": _spec("score", 0, 100),
    "respiration_rate_brpm": _spec("breaths/min", 1, 80, "brpm"),
    "spo2_percent": _spec("%", 1, 100, "percent", "pct"),
    "steps": _spec("count", 0, 200_000, "step", "steps"),
    "active_minutes": _spec("min", 0, 1_440, "minute", "minutes"),
    "calories_kcal": _spec("kcal", 0, 20_000),
    "weight_kg": _spec("kg", 20, 500),
    "skin_temperature_delta_c": _spec("deg_c_delta", -10, 10),
}

_SOURCE_PATTERN = re.compile(r"[a-z0-9][a-z0-9_.-]{0,63}\Z")


def normalize_health_source(source: str) -> str:
    """Return a safe stable source identifier or fail closed."""

    normalized = source.strip().lower().replace(" ", "_")
    if not _SOURCE_PATTERN.fullmatch(normalized):
        raise ValueError(
            "source must be 1-64 lowercase letters, numbers, dots, underscores or hyphens"
        )
    return normalized


def normalize_health_sample(sample: HealthSample) -> HealthSample:
    """Validate a supported metric and normalize its unit."""

    metric = sample.metric.strip().lower()
    spec = HEALTH_METRICS.get(metric)
    if spec is None:
        raise ValueError(f"unsupported health metric: {metric!r}")
    unit = sample.unit.strip().lower()
    if unit not in spec.aliases:
        raise ValueError(
            f"unit {sample.unit!r} is not valid for {metric}; expected {spec.unit!r}"
        )
    value = float(sample.value)
    if not math.isfinite(value):
        raise ValueError(f"{metric} must be finite")
    if not spec.minimum <= value <= spec.maximum:
        raise ValueError(
            f"{metric} must be between {spec.minimum:g} and {spec.maximum:g} {spec.unit}"
        )
    return HealthSample(date.fromisoformat(sample.date).isoformat(), metric, value, spec.unit)
