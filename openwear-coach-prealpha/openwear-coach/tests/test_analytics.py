from __future__ import annotations

import unittest

from openwear_coach.analytics import (
    estimated_one_rep_max,
    normalized_recovery_components,
    readiness_score,
    session_volume,
    summarize_strength_sets,
)
from openwear_coach.models import StrengthSet


class AnalyticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sets = [
            StrengthSet("2026-08-14", "s1", "bench_press", 1, 8, 60.0, 2.0),
            StrengthSet("2026-08-14", "s1", "bench_press", 2, 6, 65.0, 1.0),
        ]

    def test_epley_estimated_one_rep_max(self) -> None:
        self.assertEqual(estimated_one_rep_max(60.0, 8), 76.0)
        self.assertEqual(estimated_one_rep_max(100.0, 1), 100.0)

    def test_session_summary(self) -> None:
        self.assertEqual(session_volume(self.sets), 870.0)
        summary = summarize_strength_sets(self.sets)
        self.assertEqual(summary["set_count"], 2)
        self.assertEqual(summary["rep_count"], 14)
        self.assertEqual(summary["top_estimated_1rm_kg"], 78.0)
        self.assertEqual(summary["average_rir"], 1.5)

    def test_readiness_reports_missing_data_and_reweights(self) -> None:
        result = readiness_score(
            {
                "sleep": 80.0,
                "body_battery": 60.0,
                "stress": None,
                "hrv": None,
                "resting_hr": None,
            }
        )
        self.assertEqual(result["coverage"], 0.6)
        self.assertAlmostEqual(result["score"], 71.7, places=1)
        self.assertIn("hrv", result["missing"])

    def test_component_normalization(self) -> None:
        components = normalized_recovery_components(
            sleep_hours=8.0,
            body_battery=72.0,
            stress=20.0,
            hrv_ms=50.0,
            hrv_baseline_ms=50.0,
            resting_hr_bpm=55.0,
            resting_hr_baseline_bpm=55.0,
        )
        self.assertEqual(components["sleep"], 100.0)
        self.assertEqual(components["stress"], 80.0)
        self.assertAlmostEqual(components["hrv"], 50.0)
        self.assertAlmostEqual(components["resting_hr"], 50.0)


if __name__ == "__main__":
    unittest.main()

