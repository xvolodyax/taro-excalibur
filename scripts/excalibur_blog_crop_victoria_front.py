#!/usr/bin/env python3
"""Crop the top-left frontal close-up from victoria-sheet.png.

The 12-up sheet is a source only. Kie i2i must use victoria-sheet-front.png.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "memory/cover/assets/victoria-sheet.png"
FRONT = ROOT / "memory/cover/assets/victoria-sheet-front.png"
# Detected gutters on the 1280×720 Karuselka sheet: y=0–5 / 233–237, x=0–6 / 319.
BOX = (7, 6, 319, 233)


def crop_front(sheet: Path = SHEET, dest: Path = FRONT) -> Path:
    im = Image.open(sheet).convert("RGB")
    crop = im.crop(BOX)
    dest.parent.mkdir(parents=True, exist_ok=True)
    crop.save(dest, format="PNG", optimize=True)
    return dest


def main() -> int:
    if not SHEET.is_file():
        print(f"missing source sheet: {SHEET}")
        return 1
    path = crop_front()
    im = Image.open(path)
    print(f"OK {path} {im.size} {path.stat().st_size} {im.format}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
