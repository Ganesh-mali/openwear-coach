from __future__ import annotations

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from openwear_coach.importers import parse_health_csv, parse_strength_csv
from openwear_coach.models import StrengthSet
from openwear_coach.storage import Database


HEALTH_CSV = """date,metric,value,unit
2026-08-13,hrv_ms,48,ms
2026-08-14,hrv_ms,52,ms
2026-08-14,sleep_hours,7.5,h
"""

STRENGTH_CSV = """date,session_id,exercise,set_index,reps,weight_kg,rir
2026-08-14,s1,Bench Press,1,8,60,2
2026-08-14,s1,Bench Press,2,6,65,1
"""


class StorageAndImportTests(unittest.TestCase):
    def test_round_trip_and_idempotent_upsert(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "openwear.db")
            health = parse_health_csv(HEALTH_CSV)
            strength = parse_strength_csv(STRENGTH_CSV)

            self.assertEqual(database.upsert_health_samples(health), 3)
            self.assertEqual(database.upsert_health_samples(health), 3)
            self.assertEqual(database.upsert_strength_sets(strength), 2)
            self.assertEqual(database.upsert_strength_sets(strength), 2)

            coverage = database.data_coverage()
            self.assertEqual(coverage["health"]["records"], 3)
            self.assertEqual(coverage["strength"]["sets"], 2)
            self.assertEqual(coverage["strength"]["sessions"], 1)
            self.assertEqual(coverage["health"]["first_date"], "2026-08-13")
            self.assertEqual(coverage["health"]["last_date"], "2026-08-14")
            self.assertEqual(coverage["storage"], "local_sqlite")
            self.assertNotIn(str(database.path), str(coverage))

            sets = database.strength_sets(
                "2026-08-01", "2026-08-31", "bench_press"
            )
            self.assertEqual(len(sets), 2)
            self.assertEqual(sets[1].weight_kg, 65.0)
            self.assertEqual(
                database.metric_baseline("hrv_ms", "2026-08-14"), 50.0
            )

            exported = database.export_data("2026-08-13", "2026-08-14")
            self.assertEqual(len(exported["health_samples"]), 3)
            self.assertEqual(len(exported["strength_sets"]), 2)
            self.assertEqual(exported["strength_sets"][0]["source"], "user_import")

    def test_strength_identity_includes_date_and_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "openwear.db")
            first = StrengthSet("2026-08-14", "s1", "bench_press", 1, 8, 60, 2)
            later = StrengthSet("2026-08-15", "s1", "bench_press", 1, 6, 65, 1)

            database.upsert_strength_sets([first], source="garmin")
            database.upsert_strength_sets([later], source="garmin")
            database.upsert_strength_sets([first], source="apple_health")

            with database.connection() as connection:
                rows = connection.execute(
                    """
                    SELECT date, source FROM strength_sets
                    ORDER BY date, source
                    """
                ).fetchall()
            self.assertEqual(
                [(row["date"], row["source"]) for row in rows],
                [
                    ("2026-08-14", "apple_health"),
                    ("2026-08-14", "garmin"),
                    ("2026-08-15", "garmin"),
                ],
            )
            self.assertEqual(database.data_coverage()["strength"]["sessions"], 3)
            self.assertEqual(
                [item.source for item in database.strength_sets("2026-08-14", "2026-08-15")],
                ["apple_health", "garmin", "garmin"],
            )

    def test_exact_strength_replay_updates_payload_without_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "openwear.db")
            original = StrengthSet("2026-08-14", "s1", "squat", 1, 5, 100, 3)
            corrected = StrengthSet("2026-08-14", "s1", "squat", 1, 6, 102.5, 2)

            database.upsert_strength_sets([original], source="garmin")
            database.upsert_strength_sets([corrected], source="garmin")
            database.upsert_strength_sets([corrected], source="garmin")

            with database.connection() as connection:
                rows = connection.execute(
                    "SELECT * FROM strength_sets"
                ).fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["date"], "2026-08-14")
            self.assertEqual(rows[0]["source"], "garmin")
            self.assertEqual(rows[0]["session_id"], "s1")
            self.assertEqual(rows[0]["exercise"], "squat")
            self.assertEqual(rows[0]["set_index"], 1)
            self.assertEqual(rows[0]["reps"], 6)
            self.assertEqual(rows[0]["weight_kg"], 102.5)
            self.assertEqual(rows[0]["rir"], 2)

    def test_migrates_legacy_strength_identity_without_data_loss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "openwear.db"
            with closing(sqlite3.connect(path)) as connection:
                with connection:
                    connection.executescript(
                        """
                        CREATE TABLE strength_sets (
                            date TEXT NOT NULL,
                            session_id TEXT NOT NULL,
                            exercise TEXT NOT NULL,
                            set_index INTEGER NOT NULL,
                            reps INTEGER NOT NULL,
                            weight_kg REAL NOT NULL,
                            rir REAL,
                            source TEXT NOT NULL DEFAULT 'user_import',
                            PRIMARY KEY (session_id, exercise, set_index)
                        );
                        INSERT INTO strength_sets VALUES
                            ('2026-08-14', 's1', 'squat', 1, 5, 100, 2, 'legacy_a'),
                            ('2026-08-15', 's2', 'deadlift', 1, 3, 140, NULL, 'legacy_b');
                        """
                    )

            database = Database(path)

            with database.connection() as connection:
                primary_key = tuple(
                    row["name"]
                    for row in sorted(
                        (
                            row
                            for row in connection.execute(
                                "PRAGMA table_info(strength_sets)"
                            )
                            if row["pk"]
                        ),
                        key=lambda row: row["pk"],
                    )
                )
                rows = connection.execute(
                    "SELECT * FROM strength_sets ORDER BY date"
                ).fetchall()

            self.assertEqual(
                primary_key,
                ("date", "source", "session_id", "exercise", "set_index"),
            )
            self.assertEqual(len(rows), 2)
            self.assertEqual(
                dict(rows[0]),
                {
                    "date": "2026-08-14",
                    "session_id": "s1",
                    "exercise": "squat",
                    "set_index": 1,
                    "reps": 5,
                    "weight_kg": 100.0,
                    "rir": 2.0,
                    "source": "legacy_a",
                },
            )
            self.assertEqual(rows[1]["source"], "legacy_b")
            self.assertIsNone(rows[1]["rir"])

    def test_rejects_non_iso_dates(self) -> None:
        invalid = "date,metric,value,unit\n14/08/2026,hrv_ms,52,ms\n"
        with self.assertRaisesRegex(ValueError, "invalid ISO date"):
            parse_health_csv(invalid)

    def test_rejects_invalid_rir(self) -> None:
        invalid = (
            "date,session_id,exercise,set_index,reps,weight_kg,rir\n"
            "2026-08-14,s1,bench_press,1,8,60,11\n"
        )
        with self.assertRaisesRegex(ValueError, "rir must be between 0 and 10"):
            parse_strength_csv(invalid)


if __name__ == "__main__":
    unittest.main()
