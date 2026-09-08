from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from openwear_coach.apple_health import parse_apple_health
from openwear_coach.cli import main
from openwear_coach.storage import Database


def record(kind="StepCount", value="100", source="Connect", start="2026-09-01 08:00:00 +0100", end="2026-09-01 09:00:00 +0100", unit="count"):
    return (f'<Record type="HKQuantityTypeIdentifier{kind}" sourceName="{source}" '
            f'startDate="{start}" endDate="{end}" value="{value}" unit="{unit}"/>')


class AppleHealthTests(unittest.TestCase):
    def parse(self, xml):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "export.xml"
            path.write_text(xml)
            return parse_apple_health(path, "Connect", "2026-09-01", "2026-09-02")

    def test_source_filter_and_duplicate_removal(self):
        samples, receipt = self.parse("<HealthData>" + record() * 2 + record(source="iPhone") + "</HealthData>")
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].value, 100)
        self.assertEqual(receipt["metrics"], ["steps"])

    def test_overlap_rejected_without_double_counting(self):
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            self.parse("<HealthData>" + record() + record(value="200") + "</HealthData>")

    def test_external_entity_is_rejected(self):
        xml = '<!DOCTYPE HealthData [<!ENTITY xxe SYSTEM "file:///private.txt">]><HealthData>&xxe;</HealthData>'
        with self.assertRaisesRegex(ValueError, "XML rejected"):
            self.parse(xml)

    def test_waking_date_and_sleep_stage_omission(self):
        sleep = ('<Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Connect" '
                 'startDate="2026-08-31 23:00:00 +0100" endDate="2026-09-01 07:00:00 +0100" '
                 'value="HKCategoryValueSleepAnalysisAsleepUnspecified"/>')
        stage = sleep.replace("AsleepUnspecified", "AsleepCore")
        samples, receipt = self.parse("<HealthData>" + sleep + stage + "</HealthData>")
        self.assertEqual(samples[0].date, "2026-09-01")
        self.assertEqual(samples[0].value, 8)
        self.assertEqual(receipt["omitted_selected_records"], 1)

    def test_no_hrv_or_ordinary_hr_substitution(self):
        with self.assertRaisesRegex(ValueError, "No supported samples"):
            self.parse("<HealthData>" + record(kind="HeartRate", unit="count/min", value="65") + "</HealthData>")

    def test_cli_dry_run_and_replay(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "export.xml"
            path.write_text("<HealthData>" + record() + "</HealthData>")
            args = ["--db", str(root / "test.db"), "import-apple-health", str(path),
                    "--source-name", "Connect", "--start", "2026-09-01", "--end", "2026-09-02"]
            with redirect_stdout(StringIO()):
                main(args + ["--dry-run"])
                self.assertFalse((root / "test.db").exists())
                main(args)
                main(args)
            self.assertEqual(Database(root / "test.db").data_coverage()["health"]["records"], 1)
