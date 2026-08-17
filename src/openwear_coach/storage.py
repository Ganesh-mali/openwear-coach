"""Local SQLite persistence with explicit, portable schemas."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from statistics import median

from .models import HealthSample, StrengthSet


STRENGTH_SET_IDENTITY = ("date", "source", "session_id", "exercise", "set_index")
LEGACY_STRENGTH_SET_IDENTITY = ("session_id", "exercise", "set_index")


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS health_samples (
    date TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'user_import',
    PRIMARY KEY (date, metric, source)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    duration_seconds INTEGER,
    distance_meters REAL,
    source TEXT NOT NULL,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS strength_sets (
    date TEXT NOT NULL,
    session_id TEXT NOT NULL,
    exercise TEXT NOT NULL,
    set_index INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight_kg REAL NOT NULL,
    rir REAL,
    source TEXT NOT NULL DEFAULT 'user_import',
    PRIMARY KEY (date, source, session_id, exercise, set_index)
);
"""


class Database:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as connection:
            connection.executescript(SCHEMA)
            self._migrate_strength_set_identity(connection)

    @staticmethod
    def _strength_set_primary_key(
        connection: sqlite3.Connection,
    ) -> tuple[str, ...]:
        columns = connection.execute("PRAGMA table_info(strength_sets)").fetchall()
        primary_key = sorted(
            (int(column["pk"]), str(column["name"]))
            for column in columns
            if column["pk"]
        )
        return tuple(name for _, name in primary_key)

    def _migrate_strength_set_identity(
        self, connection: sqlite3.Connection
    ) -> None:
        primary_key = self._strength_set_primary_key(connection)
        if primary_key == STRENGTH_SET_IDENTITY:
            return
        if primary_key != LEGACY_STRENGTH_SET_IDENTITY:
            raise RuntimeError(
                "unsupported strength_sets primary key: "
                f"{primary_key!r}; expected {STRENGTH_SET_IDENTITY!r}"
            )

        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                """
                CREATE TABLE strength_sets_identity_migration (
                    date TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    exercise TEXT NOT NULL,
                    set_index INTEGER NOT NULL,
                    reps INTEGER NOT NULL,
                    weight_kg REAL NOT NULL,
                    rir REAL,
                    source TEXT NOT NULL DEFAULT 'user_import',
                    PRIMARY KEY (date, source, session_id, exercise, set_index)
                )
                """
            )
            connection.execute(
                """
                INSERT INTO strength_sets_identity_migration(
                    date, session_id, exercise, set_index,
                    reps, weight_kg, rir, source
                )
                SELECT date, session_id, exercise, set_index,
                       reps, weight_kg, rir, source
                FROM strength_sets
                """
            )
            previous_count = connection.execute(
                "SELECT COUNT(*) FROM strength_sets"
            ).fetchone()[0]
            migrated_count = connection.execute(
                "SELECT COUNT(*) FROM strength_sets_identity_migration"
            ).fetchone()[0]
            if migrated_count != previous_count:
                raise RuntimeError("strength_sets migration did not preserve every row")
            connection.execute("DROP TABLE strength_sets")
            connection.execute(
                """
                ALTER TABLE strength_sets_identity_migration
                RENAME TO strength_sets
                """
            )
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()

    def upsert_health_samples(
        self, samples: Iterable[HealthSample], source: str = "user_import"
    ) -> int:
        rows = [(s.date, s.metric, s.value, s.unit, source) for s in samples]
        with self.connection() as connection:
            connection.executemany(
                """
                INSERT INTO health_samples(date, metric, value, unit, source)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(date, metric, source) DO UPDATE SET
                    value = excluded.value,
                    unit = excluded.unit
                """,
                rows,
            )
        return len(rows)

    def upsert_strength_sets(
        self, sets: Iterable[StrengthSet], source: str | None = None
    ) -> int:
        rows = [
            (
                item.date,
                item.session_id,
                item.exercise,
                item.set_index,
                item.reps,
                item.weight_kg,
                item.rir,
                item.source if source is None else source,
            )
            for item in sets
        ]
        with self.connection() as connection:
            connection.executemany(
                """
                INSERT INTO strength_sets(
                    date, session_id, exercise, set_index, reps, weight_kg, rir, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date, source, session_id, exercise, set_index)
                DO UPDATE SET
                    reps = excluded.reps,
                    weight_kg = excluded.weight_kg,
                    rir = excluded.rir
                """,
                rows,
            )
        return len(rows)

    def data_coverage(self) -> dict[str, object]:
        with self.connection() as connection:
            health = connection.execute(
                """
                SELECT COUNT(*) AS records, MIN(date) AS first_date, MAX(date) AS last_date,
                       COUNT(DISTINCT metric) AS metrics
                FROM health_samples
                """
            ).fetchone()
            strength = connection.execute(
                """
                SELECT COUNT(*) AS sets,
                       (
                           SELECT COUNT(*) FROM (
                               SELECT date, source, session_id
                               FROM strength_sets
                               GROUP BY date, source, session_id
                           )
                       ) AS sessions,
                       MIN(date) AS first_date, MAX(date) AS last_date,
                       COUNT(DISTINCT exercise) AS exercises
                FROM strength_sets
                """
            ).fetchone()
            metrics = [
                row["metric"]
                for row in connection.execute(
                    "SELECT DISTINCT metric FROM health_samples ORDER BY metric"
                )
            ]
        return {
            "health": dict(health),
            "strength": dict(strength),
            "health_metrics": metrics,
            "storage": "local_sqlite",
        }

    def health_points(
        self, start_date: str, end_date: str, metrics: Sequence[str] | None = None
    ) -> list[dict[str, object]]:
        sql = """
            SELECT date, metric, value, unit, source
            FROM health_samples
            WHERE date BETWEEN ? AND ?
        """
        params: list[object] = [start_date, end_date]
        if metrics:
            placeholders = ",".join("?" for _ in metrics)
            sql += f" AND metric IN ({placeholders})"
            params.extend(metrics)
        sql += " ORDER BY metric, date"
        with self.connection() as connection:
            return [dict(row) for row in connection.execute(sql, params)]

    def health_value(self, date: str, metric: str) -> float | None:
        with self.connection() as connection:
            row = connection.execute(
                """
                SELECT value FROM health_samples
                WHERE date = ? AND metric = ?
                ORDER BY source LIMIT 1
                """,
                (date, metric),
            ).fetchone()
        return None if row is None else float(row["value"])

    def metric_baseline(
        self, metric: str, on_or_before: str, limit: int = 28
    ) -> float | None:
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT value FROM health_samples
                WHERE metric = ? AND date <= ?
                ORDER BY date DESC LIMIT ?
                """,
                (metric, on_or_before, limit),
            ).fetchall()
        values = [float(row["value"]) for row in rows]
        return median(values) if values else None

    def strength_sets(
        self, start_date: str, end_date: str, exercise: str | None = None
    ) -> list[StrengthSet]:
        sql = """
            SELECT date, session_id, exercise, set_index, reps, weight_kg, rir, source
            FROM strength_sets
            WHERE date BETWEEN ? AND ?
        """
        params: list[object] = [start_date, end_date]
        if exercise:
            sql += " AND lower(exercise) = lower(?)"
            params.append(exercise)
        sql += " ORDER BY date, source, session_id, exercise, set_index"
        with self.connection() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [StrengthSet(**dict(row)) for row in rows]

    def export_data(self, start_date: str, end_date: str) -> dict[str, object]:
        health = self.health_points(start_date, end_date)
        strength = [
            {
                "date": item.date,
                "session_id": item.session_id,
                "exercise": item.exercise,
                "set_index": item.set_index,
                "reps": item.reps,
                "weight_kg": item.weight_kg,
                "rir": item.rir,
                "source": item.source,
            }
            for item in self.strength_sets(start_date, end_date)
        ]
        return {
            "start_date": start_date,
            "end_date": end_date,
            "health_samples": health,
            "strength_sets": strength,
        }
