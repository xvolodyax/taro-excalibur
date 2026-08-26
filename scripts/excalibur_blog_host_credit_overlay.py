#!/usr/bin/env python3
"""Pillow host-credit overlay for Victoria frames.

Reads the living canon from ``memory/cover/blog-hero.json`` (and
``cover-design-code.json``). Stamps the exact credit after the image exists.
Never ask GPT Image / Kie to paint these letters. Never sign Alena.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Exact on-image line. Guillemets only around the team name. No wrapping quotes, no URL.
CANON_VICTORIA_CREDIT = "Виктория - таролог команды «ТАРО СЕЙЧАС»"

_FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/macos/Inter-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/croscore/Arimo-Regular.ttf",
)


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _fold(value: str) -> str:
    return (value or "").casefold().replace("ё", "е")


def _name_matches(identity: str, needles: list[str] | tuple[str, ...]) -> bool:
    hay = _fold(identity)
    if not hay:
        return False
    return any(_fold(str(n)) and _fold(str(n)) in hay for n in needles if str(n).strip())


def collect_host_identity(
    *,
    hero: dict[str, Any] | None = None,
    slot: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    host_name: str = "",
) -> str:
    parts: list[str] = []
    for blob in (slot or {}, manifest or {}, hero or {}):
        for key in ("host_name", "host_id", "name_ru", "hero_id", "face_host"):
            val = str(blob.get(key) or "").strip()
            if val:
                parts.append(val)
    if host_name.strip():
        parts.insert(0, host_name.strip())
    return " ".join(parts)


def normalize_host_credit_text(text: str) -> str:
    """Force the on-image line: no wrapping quotes, no extra guillemets, no site."""
    raw = (text or "").strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
        raw = raw[1:-1].strip()
    if raw.startswith("«Виктория") and raw.endswith("»") and raw.count("«") >= 2:
        raw = raw[1:-1].strip()
    compact = raw.replace(" ", "").replace("«", "").replace("»", "").replace('"', "")
    canon_compact = CANON_VICTORIA_CREDIT.replace(" ", "").replace("«", "").replace("»", "")
    if compact == canon_compact or (
        "тарологкоманды" in compact.casefold() and "таросейчас" in compact.casefold()
    ):
        return CANON_VICTORIA_CREDIT
    return raw


def _spec_from_mapping(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    text = normalize_host_credit_text(str(raw.get("text") or ""))
    if not text:
        return None
    return {**raw, "text": text}


def resolve_credit_spec(
    hero: dict[str, Any] | None = None,
    design_code: dict[str, Any] | None = None,
) -> dict[str, Any]:
    hero = hero or {}
    design_code = design_code or {}
    spec = _spec_from_mapping(hero.get("credit_overlay"))
    if spec is None:
        overlays = design_code.get("host_credit_overlays") or []
        if isinstance(overlays, list):
            for item in overlays:
                spec = _spec_from_mapping(item)
                if spec is not None:
                    break
    if spec is None:
        spec = {
            "text": CANON_VICTORIA_CREDIT,
            "apply_when_name_matches": ["Виктория", "Victoria", "Viktoria"],
            "never_apply_when_name_matches": ["Алёна", "Алена", "Alena"],
            "apply_to": ["cover", "any_host_face"],
            "never_ask_image_model": True,
            "no_banner": True,
            "no_plate": True,
            "no_url": True,
            "style": "minimal_modern",
            "placement": "bottom_left",
        }
    spec = {**spec, "text": normalize_host_credit_text(str(spec.get("text") or "")) or CANON_VICTORIA_CREDIT}
    return spec


def decide_host_credit(
    *,
    hero: dict[str, Any] | None = None,
    design_code: dict[str, Any] | None = None,
    slot_key: str = "cover",
    slot: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    host_name: str = "",
    cover_mode: str = "",
) -> dict[str, Any]:
    """Return apply/skip verdict. Alena never gets the Victoria line."""
    hero = hero or {}
    slot = slot or {}
    spec = resolve_credit_spec(hero, design_code)
    text = normalize_host_credit_text(str(spec.get("text") or CANON_VICTORIA_CREDIT))
    identity = collect_host_identity(
        hero=hero, slot=slot, manifest=manifest, host_name=host_name
    )
    never = spec.get("never_apply_when_name_matches") or ["Алёна", "Алена", "Alena"]
    apply_when = spec.get("apply_when_name_matches") or ["Виктория", "Victoria", "Viktoria"]
    mode = (cover_mode or hero.get("cover_mode") or "").strip().lower()

    if _name_matches(identity, never):
        return {"apply": False, "text": text, "reason": "alena_excluded"}

    inline_like = slot_key.startswith("inline")
    has_face = bool(slot.get("has_host_face") or slot.get("host_name") or slot.get("face_host"))
    if inline_like and not has_face:
        return {"apply": False, "text": text, "reason": "inline_without_host_face"}

    if mode in {"illustrative"} and not _name_matches(identity, apply_when) and not has_face:
        return {"apply": False, "text": text, "reason": "illustrative_no_victoria"}

    if _name_matches(identity, apply_when):
        return {"apply": True, "text": text, "reason": "victoria_named"}

    if slot_key == "cover" and mode in {"", "unset", "host_reference"}:
        # Tenant default host on a face cover is Victoria unless named otherwise.
        return {"apply": True, "text": text, "reason": "victoria_default_cover"}

    if has_face:
        return {"apply": True, "text": text, "reason": "host_face_frame"}

    return {"apply": False, "text": text, "reason": "no_victoria_face"}


def load_credit_canon(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root or project_root()
    hero_path = root / "memory/cover/blog-hero.json"
    design_path = root / "memory/cover/cover-design-code.json"
    hero = load_json(hero_path) if hero_path.is_file() else {}
    design = load_json(design_path) if design_path.is_file() else {}
    return hero, design


def _pick_font_path() -> str | None:
    for rel in _FONT_CANDIDATES:
        if Path(rel).is_file():
            return rel
    return None


def _load_font(size: int):
    from PIL import ImageFont

    path = _pick_font_path()
    if not path:
        raise RuntimeError(
            "HOST CREDIT BLOCKER: no Cyrillic TTF (Inter/Noto/DejaVu/Liberation)"
        )
    return ImageFont.truetype(path, size=size)


def _region_luma(image, box: tuple[int, int, int, int]) -> float:
    from PIL import ImageStat

    crop = image.crop(box).convert("L")
    if crop.size[0] == 0 or crop.size[1] == 0:
        return 255.0
    return float(ImageStat.Stat(crop).mean[0])


def stamp_credit_on_image(path: Path, text: str) -> dict[str, Any]:
    """Draw a small modern credit. No banner, no plate, no URL."""
    from PIL import Image, ImageDraw

    text = normalize_host_credit_text(text)
    if text != CANON_VICTORIA_CREDIT and "ален" in _fold(text):
        raise ValueError("refusing to stamp Alena with a host-credit line")

    with Image.open(path) as src:
        img = src.convert("RGBA")
        width, height = img.size
        font_size = max(13, int(round(height * 0.026)))
        font = _load_font(font_size)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = max(8, int(round(width * 0.028))) - bbox[0]
        y = max(8, height - int(round(height * 0.034)) - text_h) - bbox[1]
        sample = (
            max(0, x),
            max(0, y),
            min(width, x + text_w + 2),
            min(height, y + text_h + 2),
        )
        luma = _region_luma(img, sample)
        if luma >= 145:
            fill = (20, 24, 33, 228)
            shadow = (255, 255, 255, 70)
        else:
            fill = (248, 248, 248, 235)
            shadow = (0, 0, 0, 88)
        draw.text((x + 1, y + 1), text, font=font, fill=shadow)
        draw.text((x, y), text, font=font, fill=fill)
        img.convert("RGB").save(path, format="PNG", optimize=True)

    return {
        "applied": True,
        "text": text,
        "file": str(path),
        "style": "minimal_modern",
        "placement": "bottom_left",
        "font_size_px": font_size,
        "no_banner": True,
        "no_plate": True,
    }


def apply_host_credit(
    path: Path,
    *,
    hero: dict[str, Any] | None = None,
    design_code: dict[str, Any] | None = None,
    slot_key: str = "cover",
    slot: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    host_name: str = "",
    cover_mode: str = "",
    root: Path | None = None,
) -> dict[str, Any]:
    if hero is None or design_code is None:
        loaded_hero, loaded_design = load_credit_canon(root)
        hero = hero if hero is not None else loaded_hero
        design_code = design_code if design_code is not None else loaded_design
    verdict = decide_host_credit(
        hero=hero,
        design_code=design_code,
        slot_key=slot_key,
        slot=slot,
        manifest=manifest,
        host_name=host_name,
        cover_mode=cover_mode,
    )
    if not verdict["apply"]:
        return {**verdict, "applied": False, "file": str(path)}
    stamped = stamp_credit_on_image(path, verdict["text"])
    return {**verdict, **stamped}


def main() -> int:
    ap = argparse.ArgumentParser(description="Stamp Victoria host credit onto a finished PNG")
    ap.add_argument("--image", default="", help="Path to a finished frame PNG")
    ap.add_argument(
        "--article-dir",
        default="",
        help="Article folder; defaults image to cover/cover.png when --image is omitted",
    )
    ap.add_argument("--host", default="", help="Host name on this frame (Виктория / Алёна)")
    ap.add_argument("--slot", default="cover")
    args = ap.parse_args()
    if args.image:
        path = Path(args.image)
    elif args.article_dir:
        article_dir = Path(args.article_dir)
        path = article_dir / "cover" / "cover.png"
        if not path.is_file():
            path = article_dir / "cover.png"
    else:
        print("❌ HOST CREDIT BLOCKER: pass --image or --article-dir", file=sys.stderr)
        return 1
    if not path.is_file():
        print(f"❌ HOST CREDIT BLOCKER: image not found: {path}", file=sys.stderr)
        return 1
    try:
        result = apply_host_credit(path, slot_key=args.slot, host_name=args.host)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        print(f"❌ HOST CREDIT BLOCKER: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("applied") or result.get("apply") is False else 1


if __name__ == "__main__":
    raise SystemExit(main())
