"""Create a private, minimal initial ChatGPT history pack without uploading it."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from openwear_coach.cli import write_project_pack
from openwear_coach.garmin_export import read_garmin_export
from openwear_coach.storage import Database

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("archive", type=Path)
parser.add_argument("--out", required=True, type=Path)
args = parser.parse_args()
samples = read_garmin_export(args.archive)
with TemporaryDirectory() as folder:
    db = Database(Path(folder) / "history.db")
    db.upsert_health_samples(samples, "garmin_official_export")
    write_project_pack(db, min(x.date for x in samples), max(x.date for x in samples), args.out)
print(f"Prepared {len(samples)} dated observations locally; no upload. Review {args.out / 'coach-data.json'}")
