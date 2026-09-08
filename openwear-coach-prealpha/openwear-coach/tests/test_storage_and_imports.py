from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openwear_coach.importers import parse_health_csv, parse_strength_csv
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

