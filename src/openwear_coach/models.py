"""Typed domain models used by storage, analytics and MCP tools."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthSample:
    date: str
    metric: str
    value: float
    unit: str


@dataclass(frozen=True, slots=True)
class StrengthSet:
    date: str
    session_id: str
    exercise: str
    set_index: int
    reps: int
    weight_kg: float
    rir: float | None = None
    source: str = "user_import"
