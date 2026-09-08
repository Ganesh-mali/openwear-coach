"""Validate strength records before any database write."""

from dataclasses import replace
from datetime import date
from math import isfinite

from .health_metrics import normalize_health_source
from .models import StrengthSet


def normalize_strength_set(item: StrengthSet, source: str | None = None) -> StrengthSet:
    if not item.session_id.strip() or not item.exercise.strip():
        raise ValueError("session_id and exercise must be non-empty")
    for name in ("set_index", "reps"):
        value = getattr(item, name)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if not isfinite(item.weight_kg) or item.weight_kg <= 0:
        raise ValueError("weight_kg must be finite and positive")
    if item.rir is not None and (not isfinite(item.rir) or not 0 <= item.rir <= 10):
        raise ValueError("rir must be between 0 and 10")
    return replace(
        item, date=date.fromisoformat(item.date).isoformat(),
        session_id=item.session_id.strip(),
        exercise=item.exercise.strip().lower().replace(" ", "_"),
        source=normalize_health_source(item.source if source is None else source),
    )
