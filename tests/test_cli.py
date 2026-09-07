from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from openwear_coach.cli import main, write_project_pack
from openwear_coach.models import HealthSample, StrengthSet
from openwear_coach.storage import Database


class FileWorkflowTests(unittest.TestCase):
    def test_dry_run_then_import_replay_and_pack(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "data.db"
            csv = root / "health.csv"
            csv.write_text("\ufeffdate,metric,value,unit\n2026-09-01,sleep_hours,8,h\n", encoding="utf-8")
            args = ["--db", str(db_path), "import-health", str(csv), "--source", "garmin_manual"]
            with redirect_stdout(StringIO()):
                self.assertEqual(main(args + ["--dry-run"]), 0)
                self.assertFalse(db_path.exists())
                main(args)
                main(args)
            database = Database(db_path)
            self.assertEqual(database.data_coverage()["health"]["records"], 1)
            output = write_project_pack(database, "2026-09-01", "2026-09-02", root / "pack")
            data = json.loads((output / "coach-data.json").read_text())
            self.assertEqual(data["health_samples"][0]["source"], "garmin_manual")
            self.assertFalse(data["automatic_garmin_sync"])
            self.assertEqual(len(list(output.iterdir())), 4)
            with self.assertRaises(FileExistsError):
                write_project_pack(database, "2026-09-01", "2026-09-02", output)

    def test_strength_source_and_date_bounded_pack(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv = root / "strength.csv"
            csv.write_text("date,session_id,exercise,set_index,reps,weight_kg\n2026-09-01,s1,squat,1,5,80\n")
            with redirect_stdout(StringIO()):
                main(["--db", str(root / "data.db"), "import-strength", str(csv), "--source", "garmin_manual"])
            database = Database(root / "data.db")
            self.assertEqual(database.strength_sets("2026-09-01", "2026-09-01")[0].source, "garmin_manual")
            for start, end in [("2026-09-02", "2026-09-01"), ("2026-10-01", "2026-10-02")]:
                with self.assertRaises(ValueError):
                    write_project_pack(database, start, end, root / "pack")
                self.assertFalse((root / "pack").exists())

    def test_invalid_file_is_atomic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv = root / "bad.csv"
            csv.write_text("date,metric,value,unit\n2026-09-01,sleep_hours,8,h\n2026-09-02,sleep_hours,nan,h\n")
            with self.assertRaises(SystemExit) as error:
                main(["--db", str(root / "data.db"), "import-health", str(csv), "--source", "manual"])
            self.assertEqual(error.exception.code, 2)
            self.assertFalse((root / "data.db").exists())

    def test_stale_baseline_is_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "data.db")
            database.upsert_health_samples([
                HealthSample(f"2026-01-{day:02d}", "hrv_ms", 50, "ms") for day in range(1, 9)
            ])
            self.assertIsNone(database.metric_baseline("hrv_ms", "2026-09-01"))
            self.assertEqual(database.metric_baseline("hrv_ms", "2026-01-09"), 50)

    def test_strength_invalid_batch_does_not_partially_write(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "data.db")
            good = StrengthSet("2026-09-01", "s1", "squat", 1, 5, 80)
            for bad in [float("nan"), float("inf"), -1]:
                with self.assertRaises(ValueError):
                    database.upsert_strength_sets([good, StrengthSet("2026-09-01", "s1", "squat", 2, 5, bad)])
            self.assertEqual(database.data_coverage()["strength"]["sets"], 0)


if __name__ == "__main__":
    unittest.main()
