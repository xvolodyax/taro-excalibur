#!/usr/bin/env python3
"""Split 2x2 quad canvas into cover + 3 inline images for Excalibur BLOG."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QUADRANT_ORDER = ("top_left", "top_right", "bottom_left", "bottom_right")
DEFAULT_SLOT_MAP = {
    "cover": "top_left",
    "inline_1": "top_right",
    "inline_2": "bottom_left",
    "inline_3": "bottom_right",
}
INLINE_FILES = {
    "inline_1": "inline-01.png",
    "inline_2": "inline-02.png",
    "inline_3": "inline-03.png",
}
PANEL_ASPECT = 16 / 9
RECOMMENDED_CANVAS = (2048, 1152)  # 2×2 grid of 1024×576 (16:9 each)
DEFAULT_OUTPUT_SIZE = (1200, 675)
WHITE_THRESHOLD = 235
MIN_GUTTER_RUN = 2
GUTTER_SEARCH_RADIUS = 80
GUTTER_WHITE_FRACTION = 0.92
# White meme-collage panels often fool gutter_detect (false bands away from center).
# Accept gutter cut only when close to geometric mid + almost no aspect crop needed.
GUTTER_MAX_CENTER_OFFSET_PX = 28
GUTTER_MAX_ASPECT_CROP_LOSS = 0.02
SPLIT_MODES = ("auto", "mechanical", "gutter")


from excalibur_repo_paths import repo_relative


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_pillow():
    try:
        from PIL import Image  # noqa: F401

        return True
    except ImportError:
        print("❌ QUAD SPLIT BLOCKER: install Pillow — pip install Pillow", file=sys.stderr)
        return False


def extract_h2_titles(article_html: Path) -> list[str]:
    if not article_html.is_file():
        return []
    text = article_html.read_text(encoding="utf-8")
    titles: list[str] = []
    for match in re.finditer(r"<h2[^>]*>(.*?)</h2>", text, flags=re.I | re.S):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = re.sub(r"\s+", " ", title).strip()
        if not title:
            continue
        if title.lower() in {"частые вопросы", "faq"}:
            break
        titles.append(title)
    return titles


def default_manifest(article_dir: Path, canvas_rel: str) -> dict[str, Any]:
    """Structural stub only — never invent scene_hint/alt/hook prose."""
    meta_path = article_dir / "article.meta.json"
    meta = load_json(meta_path) if meta_path.is_file() else {}
    h2s = extract_h2_titles(article_dir / "article.html")
    topic_id = meta.get("topic_id") or article_dir.name.split("-")[0]

    slots: dict[str, Any] = {
        "cover": {
            "quadrant": DEFAULT_SLOT_MAP["cover"],
            "alt": "",
            "scene_hint": "",
            "meme_caption_ru": "",
        }
    }
    for idx, slot_key in enumerate(("inline_1", "inline_2", "inline_3"), start=1):
        h2 = h2s[idx - 1] if idx - 1 < len(h2s) else f"Секция {idx}"
        slots[slot_key] = {
            "quadrant": DEFAULT_SLOT_MAP[slot_key],
            "h2_anchor": h2,
            "alt": "",
            "scene_hint": "",
        }

    return {
        "topic_id": topic_id,
        "canvas_file": canvas_rel,
        "layout": "2x2",
        "style_preset": "taro-seichas",
        "cover_hook": "",
        "cover_hook_highlight": "",
        "slots": slots,
    }


def parse_size(spec: str) -> tuple[int, int]:
    rw, rh = spec.lower().split("x")
    return int(rw), int(rh)


def validate_canvas_grid(width: int, height: int) -> list[str]:
    errors: list[str] = []
    panel_w = width // 2
    panel_h = height // 2
    if panel_w < 320 or panel_h < 180:
        errors.append(f"canvas too small for 2x2 16:9 panels: {width}x{height}")
    ratio = panel_w / panel_h if panel_h else 0
    if abs(ratio - PANEL_ASPECT) > 0.02:
        errors.append(
            f"each panel must be 16:9, got {panel_w}x{panel_h} "
            f"(ratio {ratio:.3f}). Recommended canvas: {RECOMMENDED_CANVAS[0]}x{RECOMMENDED_CANVAS[1]}"
        )
    return errors


def quadrant_box(width: int, height: int, name: str) -> tuple[int, int, int, int]:
    half_w = width // 2
    half_h = height // 2
    if name == "top_left":
        return (0, 0, half_w, half_h)
    if name == "top_right":
        return (half_w, 0, width, half_h)
    if name == "bottom_left":
        return (0, half_h, half_w, height)
    if name == "bottom_right":
        return (half_w, half_h, width, height)
    raise ValueError(f"unknown quadrant: {name}")


def _find_gutter_band(white_fracs: list[float], center: int) -> tuple[int, int] | None:
    lo = max(0, center - GUTTER_SEARCH_RADIUS)
    hi = min(len(white_fracs), center + GUTTER_SEARCH_RADIUS)
    best: tuple[int, int] | None = None
    best_score = -1.0
    i = lo
    while i < hi:
        if white_fracs[i] >= GUTTER_WHITE_FRACTION:
            j = i
            while j < hi and white_fracs[j] >= GUTTER_WHITE_FRACTION:
                j += 1
            run_len = j - i
            if run_len >= MIN_GUTTER_RUN:
                mid = (i + j) / 2
                dist = abs(mid - center)
                score = run_len * 10 - dist
                if score > best_score:
                    best = (i, j)
                    best_score = score
            i = j
        else:
            i += 1
    return best


def center_crop_to_aspect(box: tuple[int, int, int, int], aspect: float = PANEL_ASPECT) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    if width <= 0 or height <= 0:
        return box
    current = width / height
    if abs(current - aspect) <= 0.01:
        return box
    if current > aspect:
        new_w = int(round(height * aspect))
        pad = (width - new_w) // 2
        return (left + pad, top, left + pad + new_w, bottom)
    new_h = int(round(width / aspect))
    pad = (height - new_h) // 2
    return (left, top + pad, right, top + pad + new_h)


def _aspect_crop_loss(box: tuple[int, int, int, int], aspect: float = PANEL_ASPECT) -> float:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    if width <= 0 or height <= 0:
        return 1.0
    cropped = center_crop_to_aspect(box, aspect=aspect)
    cw = cropped[2] - cropped[0]
    ch = cropped[3] - cropped[1]
    return 1.0 - (cw * ch) / (width * height)


def _gutter_midpoint(band: tuple[int, int]) -> float:
    return (band[0] + band[1]) / 2.0


def _gutter_quality_ok(
    width: int,
    height: int,
    h_gutter: tuple[int, int],
    v_gutter: tuple[int, int],
    boxes: dict[str, tuple[int, int, int, int]],
) -> tuple[bool, dict[str, Any]]:
    """Reject false gutters on white collage canvases (clip heads/stickers)."""
    h_mid = _gutter_midpoint(h_gutter)
    v_mid = _gutter_midpoint(v_gutter)
    h_offset = abs(h_mid - height / 2)
    v_offset = abs(v_mid - width / 2)
    losses = {name: _aspect_crop_loss(box) for name, box in boxes.items()}
    max_loss = max(losses.values()) if losses else 1.0
    info: dict[str, Any] = {
        "h_center_offset_px": round(h_offset, 2),
        "v_center_offset_px": round(v_offset, 2),
        "max_aspect_crop_loss": round(max_loss, 4),
        "per_panel_crop_loss": {k: round(v, 4) for k, v in losses.items()},
    }
    if h_offset > GUTTER_MAX_CENTER_OFFSET_PX or v_offset > GUTTER_MAX_CENTER_OFFSET_PX:
        info["reject_reason"] = "gutter_too_far_from_center"
        return False, info
    if max_loss > GUTTER_MAX_ASPECT_CROP_LOSS:
        info["reject_reason"] = "aspect_crop_loss_too_high"
        return False, info
    info["reject_reason"] = None
    return True, info


def detect_quadrant_boxes(
    source,
    *,
    split_mode: str = "auto",
) -> tuple[dict[str, tuple[int, int, int, int]], dict[str, Any]]:
    import numpy as np

    mode = (split_mode or "auto").strip().lower()
    if mode not in SPLIT_MODES:
        raise ValueError(f"split_mode must be one of {SPLIT_MODES}, got {split_mode!r}")

    arr = np.array(source.convert("RGB"))
    height, width = arr.shape[:2]
    mechanical = {name: quadrant_box(width, height, name) for name in QUADRANT_ORDER}
    mechanical_meta: dict[str, Any] = {
        "split_mode": "mechanical_center",
        "h_gutter_px": None,
        "v_gutter_px": None,
        "requested_mode": mode,
    }

    if mode == "mechanical":
        return mechanical, mechanical_meta

    row_white = [(arr[y].min(axis=1) > WHITE_THRESHOLD).mean() for y in range(height)]
    col_white = [(arr[:, x].min(axis=1) > WHITE_THRESHOLD).mean() for x in range(width)]

    h_gutter = _find_gutter_band(row_white, height // 2)
    v_gutter = _find_gutter_band(col_white, width // 2)

    if not (h_gutter and v_gutter):
        mechanical_meta["fallback_reason"] = "gutter_bands_not_found"
        return mechanical, mechanical_meta

    h0, h1 = h_gutter
    v0, v1 = v_gutter
    gutter_boxes = {
        "top_left": (0, 0, v0, h0),
        "top_right": (v1, 0, width, h0),
        "bottom_left": (0, h1, v0, height),
        "bottom_right": (v1, h1, width, height),
    }
    ok, quality = _gutter_quality_ok(width, height, h_gutter, v_gutter, gutter_boxes)
    gutter_meta: dict[str, Any] = {
        "split_mode": "gutter_detect",
        "h_gutter_px": {"start": h0, "end": h1},
        "v_gutter_px": {"start": v0, "end": v1},
        "requested_mode": mode,
        "gutter_quality": quality,
    }

    if mode == "gutter":
        if not ok:
            gutter_meta["quality_warn"] = quality.get("reject_reason")
        return gutter_boxes, gutter_meta

    if ok:
        return gutter_boxes, gutter_meta

    mechanical_meta["fallback_reason"] = quality.get("reject_reason") or "gutter_quality_failed"
    mechanical_meta["rejected_gutter"] = {
        "h_gutter_px": gutter_meta["h_gutter_px"],
        "v_gutter_px": gutter_meta["v_gutter_px"],
        "gutter_quality": quality,
    }
    return mechanical, mechanical_meta


def validate_panel_boxes(boxes: dict[str, tuple[int, int, int, int]]) -> list[str]:
    errors: list[str] = []
    for name in QUADRANT_ORDER:
        left, top, right, bottom = boxes[name]
        panel_w = right - left
        panel_h = bottom - top
        if panel_w < 320 or panel_h < 180:
            errors.append(f"{name} too small after split: {panel_w}x{panel_h}")
    return errors


def resolve_quadrant(slot: dict[str, Any], slot_key: str) -> str:
    q = slot.get("quadrant")
    if q:
        return str(q)
    return DEFAULT_SLOT_MAP[slot_key]


def split_canvas(
    canvas_path: Path,
    cover_dir: Path,
    manifest: dict[str, Any],
    output_size: tuple[int, int] | None,
    *,
    split_mode: str = "auto",
) -> dict[str, Any]:
    from PIL import Image

    with Image.open(canvas_path) as source:
        source = source.convert("RGBA")
        width, height = source.size
        if width < 2 or height < 2:
            raise ValueError(f"canvas too small: {width}x{height}")

        grid_errors = validate_canvas_grid(width, height)
        if grid_errors:
            raise ValueError("; ".join(grid_errors))

        quadrant_boxes, split_meta = detect_quadrant_boxes(source, split_mode=split_mode)
        panel_errors = validate_panel_boxes(quadrant_boxes)
        if panel_errors:
            raise ValueError("; ".join(panel_errors))

        outputs: dict[str, Any] = {}
        slots = manifest.get("slots") or {}

        for slot_key in ("cover", "inline_1", "inline_2", "inline_3"):
            slot = slots.get(slot_key) or {}
            quadrant = resolve_quadrant(slot, slot_key)
            raw_box = quadrant_boxes[quadrant]
            box = center_crop_to_aspect(raw_box)
            crop = source.crop(box)

            if output_size:
                crop = crop.resize(output_size, Image.Resampling.LANCZOS)

            out_name = "cover.png" if slot_key == "cover" else INLINE_FILES[slot_key]
            out_path = cover_dir / out_name
            crop.save(out_path, format="PNG", optimize=True)
            outputs[slot_key] = {
                "file": f"cover/{out_name}",
                "quadrant": quadrant,
                "box_px": {"left": box[0], "top": box[1], "right": box[2], "bottom": box[3]},
                "raw_box_px": {"left": raw_box[0], "top": raw_box[1], "right": raw_box[2], "bottom": raw_box[3]},
                "size_px": list(crop.size),
                "aspect_ratio": "16:9",
                "alt": slot.get("alt") or "",
                "h2_anchor": slot.get("h2_anchor"),
            }

        sample_box = quadrant_boxes["top_left"]
        return {
            "source_canvas": repo_relative(canvas_path, project_root()),
            "source_size_px": [width, height],
            "panel_size_px": [sample_box[2] - sample_box[0], sample_box[3] - sample_box[1]],
            "split_meta": split_meta,
            "output_size_px": list(output_size) if output_size else None,
            "outputs": outputs,
        }


def build_registry(article_dir: Path, manifest: dict[str, Any], split_info: dict[str, Any]) -> dict[str, Any]:
    meta_path = article_dir / "article.meta.json"
    meta = load_json(meta_path) if meta_path.is_file() else {}
    style = manifest.get("style_preset") or "quad_canvas"

    assets = []
    for slot_key, item in split_info["outputs"].items():
        role = "cover" if slot_key == "cover" else "inline"
        slot_meta = (manifest.get("slots") or {}).get(slot_key) or {}
        assets.append(
            {
                "role": role,
                "slot": slot_key,
                "file": item["file"],
                "alt": item.get("alt") or "",
                "h2_anchor": item.get("h2_anchor"),
                "visual_type": slot_meta.get("visual_type") or ("cover_editorial_hero" if slot_key == "cover" else None),
                "aspect_ratio": "16:9",
            }
        )

    return {
        "topic_id": manifest.get("topic_id") or meta.get("topic_id"),
        "slug": meta.get("slug"),
        "cover_family": meta.get("cover_family") or "brand_collage",
        "style_preset": style,
        "pipeline": manifest.get("pipeline") or "quad_canvas_1x_mcp",
        "file": "cover/cover.png",
        "alt": split_info["outputs"]["cover"].get("alt") or meta.get("h1") or "",
        "aspect_ratio": "16:9",
        "canvas_source": manifest.get("canvas_file", "cover/canvas-quad.png"),
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "assets": assets,
    }


_H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.I | re.S)


def _normalize_h2_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def nearest_preceding_h2(html: str, pos: int) -> str | None:
    """Return plain text of the nearest <h2> before ``pos``."""
    matches = list(_H2_RE.finditer(html, 0, pos))
    if not matches:
        return None
    return _normalize_h2_text(matches[-1].group(1))


def _figure_src_alt(figure_html: str) -> tuple[str, str]:
    src_m = re.search(r'<img\b[^>]*\bsrc="([^"]*)"', figure_html, re.I)
    alt_m = re.search(r'<img\b[^>]*\balt="([^"]*)"', figure_html, re.I)
    return (src_m.group(1) if src_m else "", alt_m.group(1) if alt_m else "")


def _slot_figure_pattern(slot_key: str) -> re.Pattern[str]:
    return re.compile(
        rf'<figure\s+(?=[^>]*\bclass="inline-(?:quad|visual)")(?=[^>]*\bdata-slot="{re.escape(slot_key)}")'
        rf"[^>]*>[\s\S]*?</figure>\s*",
        re.I,
    )


def _remove_slot_figures(html: str, slot_key: str) -> tuple[str, int, list[str]]:
    """Remove all inline figures for ``slot_key``. Returns (html, count, preceding_h2_list)."""
    pattern = _slot_figure_pattern(slot_key)
    preceding: list[str] = []
    count = 0
    parts: list[str] = []
    last = 0
    for match in pattern.finditer(html):
        h2 = nearest_preceding_h2(html, match.start())
        if h2:
            preceding.append(h2)
        count += 1
        parts.append(html[last : match.start()])
        last = match.end()
    parts.append(html[last:])
    return "".join(parts), count, preceding


def inject_figures(article_html: Path, split_info: dict[str, Any], dry_run: bool) -> list[str]:
    """Insert or relocate inline <figure> tags after manifest h2_anchor.

    If a figure for the slot already exists under the correct H2 with matching
    src/alt, skip. On H2/src/alt mismatch — remove and rewrite (never silent skip).
    """
    if not article_html.is_file():
        return ["article.html not found — skip inject"]

    html = article_html.read_text(encoding="utf-8")
    changes: list[str] = []

    for slot_key in ("inline_1", "inline_2", "inline_3"):
        item = split_info["outputs"][slot_key]
        src = item["file"]
        alt = item.get("alt") or ""
        h2 = item.get("h2_anchor")
        if not h2:
            continue
        target_h2_norm = _normalize_h2_text(h2)
        figure = (
            f'\n<figure class="inline-quad" data-slot="{slot_key}">\n'
            f'  <img src="{src}" alt="{alt}" loading="lazy">\n'
            f"</figure>\n"
        )
        pattern = re.compile(rf"(<h2[^>]*>\s*{re.escape(h2)}\s*</h2>)", re.I | re.S)
        existing = list(_slot_figure_pattern(slot_key).finditer(html))

        if existing:
            all_ok = True
            for match in existing:
                prev_h2 = nearest_preceding_h2(html, match.start())
                fig_src, fig_alt = _figure_src_alt(match.group(0))
                if prev_h2 != target_h2_norm or fig_src != src or fig_alt != alt:
                    all_ok = False
                    break
            if all_ok and len(existing) == 1:
                changes.append(f"skip {slot_key}: already correct under H2 — {h2}")
                continue
            html, removed, prev_list = _remove_slot_figures(html, slot_key)
            prev_note = ", ".join(prev_list) if prev_list else "(no H2)"
            if not pattern.search(html):
                changes.append(
                    f"removed {slot_key} from wrong H2 [{prev_note}] but target H2 not found — {h2}"
                )
                continue
            html = pattern.sub(r"\1" + figure, html, count=1)
            changes.append(
                f"moved {slot_key} → H2 — {h2} (was under [{prev_note}]; removed={removed})"
            )
            continue

        if not pattern.search(html):
            changes.append(f"skip {slot_key}: H2 not found — {h2}")
            continue
        html = pattern.sub(r"\1" + figure, html, count=1)
        changes.append(f"injected {slot_key} after H2 — {h2}")

    if not dry_run and any(not c.startswith("skip ") for c in changes):
        article_html.write_text(html, encoding="utf-8", newline="\n")
    return changes


def create_demo_canvas(path: Path, style_label: str) -> None:
    from PIL import Image, ImageDraw

    width, height = RECOMMENDED_CANVAS
    panel_w = width // 2
    panel_h = height // 2
    img = Image.new("RGB", (width, height), "#FAFAF7")
    draw = ImageDraw.Draw(img)
    colors = ["#E85D4C", "#1A1A2E", "#FFD93D", "#6C5CE7"]
    labels = ["COVER 16:9", "INLINE 1 16:9", "INLINE 2 16:9", "INLINE 3 16:9"]
    boxes = [
        (0, 0, panel_w, panel_h),
        (panel_w, 0, width, panel_h),
        (0, panel_h, panel_w, height),
        (panel_w, panel_h, width, height),
    ]
    for box, color, label in zip(boxes, colors, labels):
        draw.rectangle(box, fill=color)
        draw.text((box[0] + 32, box[1] + 32), label, fill="white")
        draw.text((box[0] + 32, box[1] + 72), style_label[:36], fill="white")
    draw.line([(panel_w, 0), (panel_w, height)], fill="#FFFFFF", width=6)
    draw.line([(0, panel_h), (width, panel_h)], fill="#FFFFFF", width=6)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")


def main() -> int:
    ap = argparse.ArgumentParser(description="Split 2x2 cover canvas into cover + 3 inline PNGs")
    ap.add_argument("--article-dir", required=True, help="memory/blog/articles/<id>-<slug>")
    ap.add_argument("--canvas", default="", help="Path to canvas-quad.png (default: cover/canvas-quad.png)")
    ap.add_argument("--manifest", default="", help="cover/quad-manifest.json (auto-generated if missing)")
    ap.add_argument(
        "--output-size",
        default="1200x675",
        help="Resize ALL 4 panels to this 16:9 size (default 1200x675, empty=keep native panel crop)",
    )
    ap.add_argument(
        "--cover-resize",
        default="",
        help=argparse.SUPPRESS,
    )
    ap.add_argument("--inject-html", action="store_true", help="Insert <figure> after matched H2 in article.html")
    ap.add_argument(
        "--split-mode",
        choices=list(SPLIT_MODES),
        default="auto",
        help=(
            "auto=gutter only if near center and low aspect-crop loss; "
            "else mechanical 50/50 (default). mechanical|gutter force mode."
        ),
    )
    ap.add_argument(
        "--demo-canvas",
        action="store_true",
        help=f"Create placeholder {RECOMMENDED_CANVAS[0]}x{RECOMMENDED_CANVAS[1]} quad canvas (4×16:9)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not require_pillow():
        return 2

    root = project_root()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = root / article_dir
    cover_dir = article_dir / "cover"
    cover_dir.mkdir(parents=True, exist_ok=True)

    canvas_rel = args.canvas or "cover/canvas-quad.png"
    canvas_path = Path(canvas_rel)
    if not canvas_path.is_absolute():
        canvas_path = article_dir / canvas_path

    if args.demo_canvas:
        create_demo_canvas(canvas_path, "taro-seichas")
        print(f"OK demo canvas={canvas_path}")

    if not canvas_path.is_file():
        print(f"❌ QUAD SPLIT BLOCKER: canvas not found: {canvas_path}", file=sys.stderr)
        return 1

    manifest_path = Path(args.manifest) if args.manifest else cover_dir / "quad-manifest.json"
    if not manifest_path.is_absolute():
        manifest_path = article_dir / manifest_path

    if manifest_path.is_file():
        manifest = load_json(manifest_path)
    else:
        print(
            "❌ QUAD SPLIT BLOCKER: missing cover/quad-manifest.json — "
            "Cover agent must invent cover_hook + scene_hint + alt first "
            "(no auto prose templates)",
            file=sys.stderr,
        )
        return 1

    missing_alt = [
        key
        for key in ("cover", "inline_1", "inline_2", "inline_3")
        if not ((manifest.get("slots") or {}).get(key) or {}).get("alt")
    ]
    if missing_alt:
        print(f"❌ QUAD SPLIT BLOCKER: missing alt in manifest slots: {', '.join(missing_alt)}", file=sys.stderr)
        return 1

    size_spec = (args.cover_resize or args.output_size or "").strip()
    output_size = parse_size(size_spec) if size_spec else None
    if output_size:
        ow, oh = output_size
        if abs((ow / oh) - PANEL_ASPECT) > 0.02:
            print(
                f"❌ QUAD SPLIT BLOCKER: --output-size must be 16:9, got {ow}x{oh}",
                file=sys.stderr,
            )
            return 1

    if args.dry_run:
        print(f"DRY RUN canvas={canvas_path} manifest={manifest_path}")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    try:
        split_info = split_canvas(
            canvas_path,
            cover_dir,
            manifest,
            output_size,
            split_mode=args.split_mode,
        )
    except ValueError as exc:
        print(f"❌ QUAD SPLIT BLOCKER: {exc}", file=sys.stderr)
        return 1
    registry = build_registry(article_dir, manifest, split_info)
    save_json(cover_dir / "cover-registry.json", registry)

    report = {
        "agent": "excalibur-blog-cover-quad-split",
        "status": "PASS",
        "manifest": str(manifest_path.relative_to(article_dir)).replace("\\", "/"),
        "split": split_info,
    }
    if args.inject_html:
        article_path = article_dir / "article.html"
        inject_log = inject_figures(article_path, split_info, dry_run=False)
        report["html_inject"] = inject_log
        inject_errors = [
            item
            for item in inject_log
            if "H2 not found" in item or "article.html not found" in item
        ]
        if article_path.is_file():
            injected_html = article_path.read_text(encoding="utf-8")
            for slot_key in ("inline_1", "inline_2", "inline_3"):
                count = len(list(_slot_figure_pattern(slot_key).finditer(injected_html)))
                if count != 1:
                    inject_errors.append(
                        f"{slot_key} figure count after inject={count} (need exactly 1)"
                    )
        if inject_errors:
            report["status"] = "BLOCK"
            report["errors"] = inject_errors
    save_json(cover_dir / "quad-split-report.json", report)

    if report["status"] != "PASS":
        for error in report.get("errors") or []:
            print(f"❌ INLINE INJECT BLOCKER: {error}", file=sys.stderr)
        return 1

    print(f"OK cover={cover_dir / 'cover.png'}")
    for slot_key in ("inline_1", "inline_2", "inline_3"):
        print(f"OK {slot_key}={cover_dir / INLINE_FILES[slot_key]}")
    print(f"OK registry={cover_dir / 'cover-registry.json'}")
    print(f"OK report={cover_dir / 'quad-split-report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
