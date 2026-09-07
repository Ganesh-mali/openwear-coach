"""MCP interface for the OpenWear Coach local-first core."""

from __future__ import annotations

import os
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import fmean
from typing import Any

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from openwear_coach.analytics import (
    normalized_recovery_components,
    readiness_score,
    summarize_strength_sets,
)
from openwear_coach.health_metrics import normalize_health_source
from openwear_coach.importers import parse_health_csv, parse_strength_csv
from openwear_coach.models import StrengthSet
from openwear_coach.security import (
    require_local_transport,
    require_loopback_host,
    require_tcp_port,
)
from openwear_coach.storage import Database


def _database_path() -> Path:
    configured = os.environ.get("OPENWEAR_DB")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".openwear-coach" / "data.db"


db = Database(_database_path())
mcp = MCPServer(
    "openwear-coach",
    title="OpenWear Coach",
    description="Local-first physical wellbeing and strength coaching from user-owned wearable data.",
    instructions=(
        "Use exact ISO dates. Report missing data and readiness coverage. "
        "Keep sources separate. Treat readiness as a coaching heuristic, not medical advice."
    ),
    version="0.1.0",
)

READ_LOCAL = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)
WRITE_LOCAL = ToolAnnotations(
    read_only_hint=False,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)


def _iso_date(value: str) -> str:
    return date.fromisoformat(value).isoformat()


@mcp.tool(annotations=READ_LOCAL)
def get_data_coverage() -> dict[str, Any]:
    """Return exact available date ranges, metrics and record counts."""

    return db.data_coverage()


@mcp.tool(annotations=READ_LOCAL)
def get_health_trends(
    start_date: str,
    end_date: str,
    metrics: list[str] | None = None,
    source: str = "user_import",
) -> dict[str, Any]:
    """Return exact dated health points plus per-metric summary changes."""

    start = _iso_date(start_date)
    end = _iso_date(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")
    clean_metrics = [metric.strip().lower() for metric in metrics] if metrics else None
    clean_source = normalize_health_source(source)
    points = db.health_points(start, end, clean_metrics, clean_source)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for point in points:
        grouped[str(point["metric"])].append(point)

    summaries: dict[str, Any] = {}
    for metric, values in grouped.items():
        first = float(values[0]["value"])
        last = float(values[-1]["value"])
        summaries[metric] = {
            "records": len(values),
            "first": values[0],
            "last": values[-1],
            "average": round(fmean(float(item["value"]) for item in values), 2),
            "absolute_change": round(last - first, 2),
            "percent_change": None
            if first == 0
            else round((last - first) / abs(first) * 100.0, 2),
        }
    return {
        "start_date": start,
        "end_date": end,
        "source": clean_source,
        "points": points,
        "summaries": summaries,
    }


@mcp.tool(annotations=READ_LOCAL)
def get_daily_readiness(
    on_date: str, source: str = "user_import"
) -> dict[str, Any]:
    """Calculate a transparent recovery heuristic for one exact date."""

    target = _iso_date(on_date)
    clean_source = normalize_health_source(source)
    hrv = db.health_value(target, "hrv_ms", clean_source)
    resting_hr = db.health_value(target, "resting_hr_bpm", clean_source)
    components = normalized_recovery_components(
        sleep_hours=db.health_value(target, "sleep_hours", clean_source),
        body_battery=db.health_value(target, "body_battery", clean_source),
        stress=db.health_value(target, "stress", clean_source),
        hrv_ms=hrv,
        hrv_baseline_ms=db.metric_baseline("hrv_ms", target, clean_source),
        resting_hr_bpm=resting_hr,
        resting_hr_baseline_bpm=db.metric_baseline(
            "resting_hr_bpm", target, clean_source
        ),
    )
    result = readiness_score(components)
    return {
        "date": target,
        "source": clean_source,
        **result,
        "method": "weighted available components; missing inputs are excluded",
        "baseline_policy": "up to 28 prior days from the same source; minimum 7 samples",
        "not_medical_advice": True,
    }


@mcp.tool(annotations=READ_LOCAL)
def get_strength_sessions(start_date: str, end_date: str) -> dict[str, Any]:
    """Summarize strength sessions between two exact dates, inclusive."""

    start = _iso_date(start_date)
    end = _iso_date(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")
    grouped: dict[tuple[str, str, str], list[StrengthSet]] = defaultdict(list)
    for item in db.strength_sets(start, end):
        grouped[(item.date, item.source, item.session_id)].append(item)

    sessions: list[dict[str, Any]] = []
    for (session_date, source, session_id), items in sorted(grouped.items()):
        by_exercise: dict[str, list[StrengthSet]] = defaultdict(list)
        for item in items:
            by_exercise[item.exercise].append(item)
        sessions.append(
            {
                "date": session_date,
                "source": source,
                "session_id": session_id,
                "summary": summarize_strength_sets(items),
                "exercises": {
                    exercise: summarize_strength_sets(exercise_sets)
                    for exercise, exercise_sets in sorted(by_exercise.items())
                },
            }
        )
    return {"start_date": start, "end_date": end, "sessions": sessions}


@mcp.tool(annotations=READ_LOCAL)
def get_strength_progress(
    exercise: str, start_date: str, end_date: str
) -> dict[str, Any]:
    """Return exact-date volume and estimated-1RM progression for one exercise."""

    start = _iso_date(start_date)
    end = _iso_date(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")
    exercise_key = exercise.strip().lower().replace(" ", "_")
    grouped: dict[tuple[str, str, str], list[StrengthSet]] = defaultdict(list)
    for item in db.strength_sets(start, end, exercise_key):
        grouped[(item.date, item.source, item.session_id)].append(item)
    points = [
        {
            "date": session_date,
            "source": source,
            "session_id": session_id,
            **summarize_strength_sets(items),
        }
        for (session_date, source, session_id), items in sorted(grouped.items())
    ]
    return {
        "exercise": exercise_key,
        "start_date": start,
        "end_date": end,
        "sessions": points,
    }


@mcp.tool(annotations=WRITE_LOCAL)
def import_health_csv(
    csv_text: str, source: str = "user_import"
) -> dict[str, Any]:
    """Import health CSV text into local storage; existing identical keys are updated."""

    samples = parse_health_csv(csv_text)
    clean_source = normalize_health_source(source)
    return {
        "imported": db.upsert_health_samples(samples, clean_source),
        "kind": "health",
        "source": clean_source,
    }


@mcp.tool(annotations=WRITE_LOCAL)
def import_strength_csv(csv_text: str) -> dict[str, Any]:
    """Import strength CSV text into local storage; existing identical keys are updated."""

    sets = parse_strength_csv(csv_text)
    return {"imported": db.upsert_strength_sets(sets), "kind": "strength"}


@mcp.tool(annotations=WRITE_LOCAL)
def record_strength_session(
    session_date: str, session_id: str, sets: list[dict[str, Any]]
) -> dict[str, Any]:
    """Add or update a local strength session using kg, reps and optional RIR."""

    target = _iso_date(session_date)
    if not session_id.strip():
        raise ValueError("session_id must be non-empty")
    parsed: list[StrengthSet] = []
    for index, raw in enumerate(sets, start=1):
        parsed.append(
            StrengthSet(
                date=target,
                session_id=session_id.strip(),
                exercise=str(raw["exercise"]).strip().lower().replace(" ", "_"),
                set_index=raw.get("set_index", index),
                reps=raw["reps"],
                weight_kg=float(raw["weight_kg"]),
                rir=None if raw.get("rir") is None else float(raw["rir"]),
            )
        )
    for item in parsed:
        if not item.exercise or item.set_index <= 0 or item.reps <= 0 or item.weight_kg <= 0:
            raise ValueError("each set needs exercise and positive set_index, reps and weight_kg")
        if item.rir is not None and not 0 <= item.rir <= 10:
            raise ValueError("rir must be between 0 and 10")
    return {
        "recorded": db.upsert_strength_sets(parsed, source="manual"),
        "date": target,
        "session_id": session_id.strip(),
    }


@mcp.tool(annotations=READ_LOCAL)
def export_user_data(start_date: str, end_date: str) -> dict[str, Any]:
    """Export local health and strength records for an exact inclusive date range."""

    start = _iso_date(start_date)
    end = _iso_date(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")
    return db.export_data(start, end)


def main() -> None:
    transport = require_local_transport(
        os.environ.get("OPENWEAR_TRANSPORT", "streamable-http")
    )
    if transport == "stdio":
        mcp.run("stdio")
        return

    host = require_loopback_host(os.environ.get("OPENWEAR_HOST", "127.0.0.1"))
    port = require_tcp_port(os.environ.get("OPENWEAR_PORT", "8000"))
    mcp.run(
        "streamable-http",
        host=host,
        port=port,
        stateless_http=True,
        json_response=True,
    )


if __name__ == "__main__":
    main()
