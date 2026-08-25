#!/usr/bin/env python3
"""Living canon + per-article identity checklist for the Victoria cover.

Durable rule: shared/cover-host-canon.md
After every cover gen the agent opens the ref and the frame side by side,
fills cover/cover-host-gate.json, then this script must PASS before the
PNG may enter the article package.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CANON_CREDIT = "Виктория - таролог команды «ТАРО СЕЙЧАС»"

LIVING_CANON: dict[str, tuple[str, ...]] = {
    "shared/cover-host-canon.md": (
        "виктория.png",
        "victoria.png",
        "Натюрморт",
        "шов",
        "Холл",
        CANON_CREDIT,
        "Kie GPT Image 2",
        "белый пиджак",
    ),
    "shared/SOUL.md": (
        "cover-host-canon.md",
        "Виктория всегда в кадре",
        "Холл не перерисовывает",
        CANON_CREDIT,
    ),
    "memory/cover/blog-hero.json": (
        "victoria.png",
        "still_life_rule",
        "hall_redraw",
        "identity_fail_is",
        "hard_reject_rebuild_whole_canvas",
        "long STRAIGHT light-blonde",
    ),
    "memory/cover/cover-design-code.json": (
        "cover-host-canon.md",
        "не шов по лицу",
        "Холл не перерисовывает",
        "FACE visible LARGE left wearing",
    ),
    "skills/cover-excalibur-blog/SKILL.md": (
        "cover-host-canon.md",
        "Identity-fail",
        "HARD reject",
        "Холл обложку",
    ),
    ".cursor/skills/cover-excalibur-blog/SKILL.md": (
        "cover-host-canon.md",
        "Identity-fail",
        "HARD reject",
        "Холл обложку",
    ),
}

CHECKLIST_TRUE = (
    "compared_side_by_side",
    "victoria_face_visible",
    "hair_match",
    "eyes_match",
    "bone_match",
    "no_face_seam",
    "not_brunette",
    "not_alena",
    "credit_applied",
)
CHECKLIST_FALSE = ("still_life_only",)
REQUIRED_REF_SUBSTR = "виктория.png"


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def living_canon_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for rel, needles in LIVING_CANON.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"missing living canon file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing required phrase {needle!r}")
    return errors


def load_checklist(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def checklist_errors(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["cover-host-gate.json must be an object"]
    for key in CHECKLIST_TRUE:
        if data.get(key) is not True:
            errors.append(f"{key} must be true (open ref and frame side by side)")
    for key in CHECKLIST_FALSE:
        if data.get(key) is not False:
            errors.append(f"{key} must be false — still-life is inline-only")
    ref = str(data.get("ref_path") or "")
    if REQUIRED_REF_SUBSTR not in ref and "victoria.png" not in ref:
        errors.append("ref_path must point at виктория.png / victoria.png")
    return errors


def validate(
    root: Path,
    *,
    article_dir: Path | None = None,
    require_checklist: bool = False,
) -> dict:
    errors = living_canon_errors(root)
    checklist_path: Path | None = None
    if article_dir is not None:
        checklist_path = article_dir / "cover" / "cover-host-gate.json"
        if checklist_path.is_file():
            try:
                errors.extend(checklist_errors(load_checklist(checklist_path)))
            except json.JSONDecodeError as exc:
                errors.append(f"cover-host-gate.json is not JSON: {exc}")
        elif require_checklist:
            errors.append("cover/cover-host-gate.json missing — fill after side-by-side check")
    return {
        "status": "PASS" if not errors else "BLOCK",
        "errors": errors,
        "checklist": str(checklist_path) if checklist_path else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--article-dir", default="", help="Article dir with cover/cover-host-gate.json")
    ap.add_argument(
        "--require-checklist",
        action="store_true",
        help="FAIL if cover-host-gate.json is missing (use after a cover gen)",
    )
    ap.add_argument(
        "-o",
        "--output",
        default="",
        help="Optional JSON report path (relative to article-dir when set)",
    )
    args = ap.parse_args()
    root = project_root()
    article_dir = Path(args.article_dir) if args.article_dir else None
    if article_dir is not None and not article_dir.is_absolute():
        article_dir = root / article_dir
    verdict = validate(
        root,
        article_dir=article_dir,
        require_checklist=bool(args.require_checklist or args.article_dir),
    )
    if args.output:
        out = Path(args.output)
        if article_dir is not None and not out.is_absolute():
            out = article_dir / out
        out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cover-host-gate {verdict['status']}")
    for err in verdict["errors"]:
        print(f"  - {err}")
    return 0 if verdict["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
