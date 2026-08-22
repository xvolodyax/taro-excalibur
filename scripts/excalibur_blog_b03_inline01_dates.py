#!/usr/bin/env python3
"""Rebuild B03 inline-01 from article.html numbers, then restitch the 2K quad.

Owner-requested fact fix: Kie drew 17.08.1990 with both methods = 8.
Canon date from article.html: 17.06.1995 → parts 2, stream 11.
Does not rewrite article.html. Does not publish.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from image_validate import validate_image_file

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "memory/blog/articles/B03-shodyatsya-li-vashi-daty-v-otnosheniyah"
COVER = ARTICLE / "cover"
CANVAS = COVER / "canvas-quad.png"
INLINE = COVER / "inline-01.png"
GATE = COVER / "inline-01-facts-gate.json"

DATE = "17.06.1995"
PARTS_FINAL = 2
STREAM_FINALS = 11
BG = (255, 255, 255)
INK = (26, 20, 20)
ACCENT = (139, 58, 58)
LINE = (210, 210, 210)
BOX = (248, 248, 248)
BOX_EDGE = (30, 24, 24)

FONTS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
FONTS_REG = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = FONTS if bold else FONTS_REG
    for path in paths:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def center_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> None:
    x0, y0, x1, y1 = xy
    tw, th = text_size(draw, text, fnt)
    draw.text((x0 + (x1 - x0 - tw) // 2, y0 + (y1 - y0 - th) // 2), text, font=fnt, fill=fill)


def rounded(draw: ImageDraw.ImageDraw, xy, fill, outline, radius: int = 10, width: int = 2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, x0: int, y: int, x1: int) -> None:
    draw.line((x0, y, x1 - 8, y), fill=INK, width=3)
    draw.polygon([(x1, y), (x1 - 12, y - 6), (x1 - 12, y + 6)], fill=INK)


def draw_panel(width: int = 2048, height: int = 1152) -> Image.Image:
    if PARTS_FINAL == STREAM_FINALS:
        raise SystemExit("refusing to draw identical finals — thesis breaks")
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    title_f = font(42, bold=True)
    label_f = font(28, bold=True)
    body_f = font(26)
    small_f = font(22)
    num_f = font(48, bold=True)
    circle_f = font(56, bold=True)

    title = "КАК ОДНА ДАТА РОЖДЕНИЯ ДАЁТ ДВА РАЗНЫХ ЧИСЛА"
    tw, th = text_size(draw, title, title_f)
    draw.text(((width - tw) // 2, 36), title, font=title_f, fill=INK)

    top = 118
    bottom = height - 40
    gutter = 22
    cols = [28]
    # date | parts | stream | two numbers
    widths = [300, 610, 610, 400]
    x = 28
    for w in widths:
        cols.append(x + w)
        x += w + gutter

    # vertical rules between methods and result
    for gx in (cols[2] - gutter // 2, cols[3] - gutter // 2):
        draw.line((gx, top + 10, gx, bottom - 10), fill=LINE, width=2)

    # --- col 0: one date ---
    x0, x1 = cols[0], cols[1]
    center_text(draw, (x0, top, x1, top + 48), "одна дата", label_f, ACCENT)
    cal = (x0 + 40, top + 90, x1 - 40, top + 320)
    rounded(draw, cal, BOX, BOX_EDGE, radius=16)
    # calendar header
    draw.rectangle((cal[0], cal[1], cal[2], cal[1] + 54), fill=ACCENT)
    center_text(draw, (cal[0], cal[1], cal[2], cal[1] + 54), "июнь", font(24, bold=True), (255, 255, 255))
    center_text(draw, (cal[0], cal[1] + 70, cal[2], cal[3] - 20), DATE, font(36, bold=True), INK)
    arrow(draw, x1 - 8, (top + bottom) // 2, cols[1] + 16)

    # --- col 1: parts ---
    p0, p1 = cols[1], cols[2]
    center_text(draw, (p0, top, p1, top + 48), "сложение по частям", label_f, ACCENT)
    lines = [
        "день  1 + 7 = 8",
        "месяц  6",
        "год  1 + 9 + 9 + 5 = 24  →  6",
        "8 + 6 + 6 = 20  →  2",
    ]
    y = top + 80
    for line in lines:
        box = (p0 + 16, y, p1 - 16, y + 70)
        rounded(draw, box, BOX, BOX_EDGE, radius=10)
        center_text(draw, box, line, body_f, INK)
        y += 86
    fin1 = (p0 + 180, y + 10, p1 - 180, y + 130)
    draw.ellipse(fin1, outline=INK, width=4)
    center_text(draw, fin1, str(PARTS_FINAL), num_f, INK)

    # --- col 2: stream ---
    s0, s1 = cols[2], cols[3]
    center_text(draw, (s0, top, s1, top + 48), "сплошной поток цифр", label_f, ACCENT)
    stream_lines = [
        "1 + 7 + 0 + 6 + 1 + 9 + 9 + 5",
        "= 38  →  11",
        "мастер-число, не сводить к 2",
    ]
    y = top + 100
    for i, line in enumerate(stream_lines):
        box = (s0 + 16, y, s1 - 16, y + 78)
        rounded(draw, box, BOX, BOX_EDGE, radius=10)
        fill = ACCENT if i == 2 else INK
        fnt = small_f if i == 2 else body_f
        center_text(draw, box, line, fnt, fill)
        y += 94
    fin2 = (s0 + 180, y + 10, s1 - 180, y + 130)
    draw.ellipse(fin2, outline=ACCENT, width=5)
    center_text(draw, fin2, str(STREAM_FINALS), num_f, ACCENT)

    # --- col 3: two different numbers ---
    r0, r1 = cols[3], cols[4]
    center_text(draw, (r0, top, r1, top + 70), "два разных числа", label_f, ACCENT)
    c1 = (r0 + 90, top + 140, r1 - 90, top + 360)
    c2 = (r0 + 90, top + 430, r1 - 90, top + 650)
    draw.ellipse(c1, outline=INK, width=6)
    draw.ellipse(c2, outline=ACCENT, width=6)
    center_text(draw, c1, str(PARTS_FINAL), circle_f, INK)
    center_text(draw, c2, str(STREAM_FINALS), circle_f, ACCENT)
    mid_y = (c1[3] + c2[1]) // 2
    draw.line((r0 + 70, mid_y, r1 - 70, mid_y), fill=LINE, width=2)

    return img


def stitch_canvas(panel_1024: Image.Image) -> None:
    canvas = Image.open(CANVAS).convert("RGB")
    if canvas.size != (2048, 1152):
        raise SystemExit(f"unexpected canvas size {canvas.size}, need 2048x1152")
    if panel_1024.size != (1024, 576):
        panel_1024 = panel_1024.resize((1024, 576), Image.Resampling.LANCZOS)
    canvas.paste(panel_1024, (1024, 0))
    # keep white seam look: 4px white crosshair at mechanical center
    draw = ImageDraw.Draw(canvas)
    draw.line((0, 576, 2048, 576), fill=BG, width=4)
    draw.line((1024, 0, 1024, 1152), fill=BG, width=4)
    canvas.save(CANVAS, format="PNG", optimize=True)


def write_gate(status: str, errors: list[str]) -> None:
    payload = {
        "gate": "inline-01-facts",
        "status": status,
        "date": DATE,
        "parts_final": PARTS_FINAL,
        "stream_final": STREAM_FINALS,
        "must_differ": True,
        "source": "article.html 17 июня 1995",
        "errors": errors,
    }
    GATE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_drawn(panel: Image.Image) -> list[str]:
    errors: list[str] = []
    if PARTS_FINAL == STREAM_FINALS:
        errors.append("finals are identical")
    if {PARTS_FINAL, STREAM_FINALS} != {2, 11}:
        errors.append("finals must be 2 and 11")
    if DATE != "17.06.1995":
        errors.append("date must be 17.06.1995")
    errors.extend(validate_image_file(INLINE) if INLINE.is_file() else ["inline-01 missing"])
    errors.extend(validate_image_file(CANVAS) if CANVAS.is_file() else ["canvas missing"])
    # old wrong date must not be encoded as the only calendar string
    _ = panel
    return errors


def main() -> int:
    hi = draw_panel(2048, 1152)
    cell = hi.resize((1024, 576), Image.Resampling.LANCZOS)
    stitch_canvas(cell)
    return 0


if __name__ == "__main__":
    try:
        hi = draw_panel(2048, 1152)
        cell = hi.resize((1024, 576), Image.Resampling.LANCZOS)
        stitch_canvas(cell)
        print(f"OK canvas patched={CANVAS}")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        write_gate("BLOCK", [str(exc)])
        print(f"BLOCK: {exc}", file=sys.stderr)
        sys.exit(1)
