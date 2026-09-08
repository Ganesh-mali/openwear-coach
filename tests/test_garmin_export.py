import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from openwear_coach.garmin_export import read_garmin_export


class GarminExportTests(unittest.TestCase):
    def test_only_selected_fields_without_profile_or_identifiers(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "export.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("DI_CONNECT/wellness/UDSFile_test.json", json.dumps([
                    {"calendarDate": "2026-09-01", "totalSteps": 1000,
                     "restingHeartRate": 60, "userProfilePK": "PRIVATE-ID"}]))
                archive.writestr("DI_CONNECT/sleep/test_sleepData.json", json.dumps([
                    {"retro": True}, {"calendarDate": "2026-09-01", "deepSleepSeconds": 3600,
                     "lightSleepSeconds": 18000, "remSleepSeconds": 3600, "userNote": "PRIVATE-NOTE"}]))
                archive.writestr("DI_CONNECT/user_profile.json", '{"email":"PRIVATE-EMAIL"}')
            samples = read_garmin_export(path)
            self.assertEqual(len(samples), 3)
            self.assertNotIn("PRIVATE", str(samples))
            self.assertEqual(next(x.value for x in samples if x.metric == "sleep_hours"), 7)

    def test_conflicting_duplicates_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "export.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("DI_CONNECT/UDSFile_test.json", json.dumps([
                    {"calendarDate": "2026-09-01", "totalSteps": 100},
                    {"calendarDate": "2026-09-01", "totalSteps": 200}]))
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                read_garmin_export(path)
