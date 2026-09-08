"""Deterministic, dependency-free coaching calculations.

These functions are intentionally auditable. They do not diagnose health
conditions and they do not claim that a wearable-derived score is medical
advice.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from statistics import fmean

from .models import StrengthSet


READINESS_WEIGHTS: dict[str, float] = {
    "sleep": 0.35,
    "body_battery": 0.25,
    "stress": 0.20,
    "hrv": 0.10,
    "resting_hr": 0.10,
}


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def estimated_one_rep_max(weight_kg: float, reps: int) -> float:
    """Return Epley estimated 1RM in kilograms.

    Single-repetition sets return the observed weight. Non-positive values are
    rejected because quietly accepting them would corrupt progression trends.
    """

    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")
    if reps <= 0:
        raise ValueError("reps must be positive")
    if reps == 1:
        return round(weight_kg, 2)
    return round(weight_kg * (1.0 + reps / 30.0), 2)


def session_volume(sets: Iterable[StrengthSet]) -> float:
    """Return total external load volume (reps x kg)."""

    return round(sum(item.reps * item.weight_kg for item in sets), 2)


def summarize_strength_sets(sets: Iterable[StrengthSet]) -> dict[str, float | int | None]:
    items = list(sets)
    if not items:
        return {
            "set_count": 0,
            "rep_count": 0,
            "volume_kg": 0.0,
            "top_weight_kg": None,
            "top_estimated_1rm_kg": None,
            "average_rir": None,
        }

    rir_values = [item.rir for item in items if item.rir is not None]
    return {
        "set_count": len(items),
        "rep_count": sum(item.reps for item in items),
        "volume_kg": session_volume(items),
        "top_weight_kg": max(item.weight_kg for item in items),
        "top_estimated_1rm_kg": max(
            estimated_one_rep_max(item.weight_kg, item.reps) for item in items
        ),
        "average_rir": round(fmean(rir_values), 2) if rir_values else None,
    }


def readiness_score(components: Mapping[str, float | None]) -> dict[str, object]:
    """Combine available 0..100 component scores without hiding missing data.

    Missing components are excluded and the remaining weights are normalized.
    Coverage is the fraction of the configured total weight actually observed.
    """

    present: dict[str, float] = {}
    for name, weight in READINESS_WEIGHTS.items():
        value = components.get(name)
        if value is not None:
            present[name] = clamp(float(value))

    observed_weight = sum(READINESS_WEIGHTS[name] for name in present)
    if observed_weight == 0:
        return {
            "score": None,
            "coverage": 0.0,
            "components": {},
            "missing": sorted(READINESS_WEIGHTS),
        }

    weighted = sum(
        present[name] * READINESS_WEIGHTS[name] for name in present
    ) / observed_weight
    return {
        "score": round(weighted, 1),
        "coverage": round(observed_weight, 2),
        "components": present,
        "missing": sorted(set(READINESS_WEIGHTS) - set(present)),
    }


def normalized_recovery_components(
    *,
    sleep_hours: float | None,
    body_battery: float | None,
    stress: float | None,
    hrv_ms: float | None,
    hrv_baseline_ms: float | None,
    resting_hr_bpm: float | None,
    resting_hr_baseline_bpm: float | None,
) -> dict[str, float | None]:
    """Map raw wearable values to explicit 0..100 component scores."""

    sleep_score = None if sleep_hours is None else clamp(sleep_hours / 8.0 * 100.0)
    battery_score = None if body_battery is None else clamp(body_battery)
    stress_score = None if stress is None else clamp(100.0 - stress)

    hrv_score = None
    if hrv_ms is not None and hrv_baseline_ms and hrv_baseline_ms > 0:
        # 80% of baseline maps to 0; 120% maps to 100.
        hrv_score = clamp((hrv_ms / hrv_baseline_ms - 0.8) / 0.4 * 100.0)

    resting_hr_score = None
    if (
        resting_hr_bpm is not None
        and resting_hr_baseline_bpm
        and resting_hr_baseline_bpm > 0
    ):
        # 110% of baseline maps to 0; 90% maps to 100.
        resting_hr_score = clamp(
            (1.1 - resting_hr_bpm / resting_hr_baseline_bpm) / 0.2 * 100.0
        )

    return {
        "sleep": sleep_score,
        "body_battery": battery_score,
        "stress": stress_score,
        "hrv": hrv_score,
        "resting_hr": resting_hr_score,
    }
