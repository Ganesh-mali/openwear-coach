#!/bin/sh
# One-time packaging on a Mac already signed into iCloud. No credentials here.
set -eu
cd "$(dirname "$0")"
python3 build_shortcut.py
mkdir -p ../dist/shortcut
python3 -c "import plistlib,pathlib; p=pathlib.Path('OpenWear Check-in.unsigned.plist'); pathlib.Path('../dist/input.shortcut').write_bytes(plistlib.dumps(plistlib.loads(p.read_bytes()),fmt=plistlib.FMT_BINARY))"
/usr/bin/shortcuts sign --mode anyone --input ../dist/input.shortcut --output '../dist/shortcut/OpenWear Check-in.shortcut'
printf '%s\n' 'Signed file: dist/shortcut/OpenWear Check-in.shortcut. Transfer to iPhone and test before daily use.'
