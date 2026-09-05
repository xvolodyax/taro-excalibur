"""HARD: face ref is only Виктория.png. Latin aliases must not be the canon path."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON_REL = "memory/cover/assets/Виктория.png"
CANON_NAME = "Виктория.png"

LATIN_NAMES = (
    "viktoriaref.png",
    "victoria-sheet.png",
    "victoria.png",
)
LATIN_STEMS = (
    "viktoriaref",
    "victoria-sheet",
    "victoria_ref",
)

# Lines that *assign* a latin file as the live face (not a ban list).
CANON_ASSIGN = re.compile(
    r"""
    (?:
        CANON_FACE_(?:NAME|REL)
        | DEFAULT_LOCAL_REFERENCE
        | "reference_image"
        | "local_reference"
        | "reference_url_hosted"
        | "reference_url_source"
    )
    \s*[=:]\s*
    ["'][^"']*(?:viktoriaref|victoria-sheet|victoria\.png|victoria_ref)
    """,
    re.IGNORECASE | re.VERBOSE,
)

SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    "node_modules",
    "canvases",
    ".cursor/canvases",
}
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".json",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".html",
}


class CoverFaceFilenameCanonTest(unittest.TestCase):
    def test_owner_drop_matches_canon_bytes(self) -> None:
        inbox = ROOT / "cover-refs" / CANON_NAME
        canon = ROOT / CANON_REL
        self.assertTrue(inbox.is_file(), inbox)
        self.assertTrue(canon.is_file(), canon)
        self.assertEqual(inbox.name, CANON_NAME)
        self.assertEqual(inbox.read_bytes(), canon.read_bytes())

    def test_latin_files_absent(self) -> None:
        for folder in (ROOT / "memory/cover", ROOT / "cover-refs"):
            if not folder.is_dir():
                continue
            for path in folder.rglob("*"):
                if not path.is_file():
                    continue
                name = path.name
                if name == CANON_NAME:
                    continue
                low = name.lower()
                self.assertNotIn(low, {n.lower() for n in LATIN_NAMES})
                self.assertFalse(low.startswith("victoria_ref"), name)

    def test_pointers_use_cyrillic(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        self.assertEqual(hero["reference_image"], CANON_REL)
        self.assertTrue(str(hero.get("reference_url_hosted") or "").endswith(CANON_NAME))
        style = json.loads(
            (ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(encoding="utf-8")
        )
        self.assertEqual(style["local_reference"], CANON_REL)
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_identity_gate import CANON_FACE_NAME, CANON_FACE_REL
        from excalibur_blog_cover_quad_prompt import (
            CANON_FACE_NAME as PROMPT_NAME,
            CANON_FACE_REL as PROMPT_REL,
        )
        from excalibur_blog_kie_gpt_image2_api import DEFAULT_LOCAL_REFERENCE

        self.assertEqual(CANON_FACE_NAME, CANON_NAME)
        self.assertEqual(CANON_FACE_REL, CANON_REL)
        self.assertEqual(PROMPT_NAME, CANON_NAME)
        self.assertEqual(PROMPT_REL, CANON_REL)
        self.assertEqual(DEFAULT_LOCAL_REFERENCE, CANON_REL)

    def test_no_latin_canon_assignments(self) -> None:
        hits: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES or part == ".git" for part in path.parts):
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            rel = str(path.relative_to(ROOT))
            for i, line in enumerate(text.splitlines(), 1):
                if CANON_ASSIGN.search(line):
                    hits.append(f"{rel}:{i}:{line.strip()}")
        self.assertEqual(hits, [], "latin aliases still assigned as canon:\n" + "\n".join(hits))

    def test_blog_hero_reference_png_not_the_face(self) -> None:
        """Generic skeleton name must not remain the default local face."""
        defaults = (
            (ROOT / "scripts/excalibur_blog_kie_gpt_image2_api.py").read_text(encoding="utf-8"),
            (ROOT / "scripts/excalibur_blog_hero_reference_url.py").read_text(encoding="utf-8"),
        )
        for src in defaults:
            self.assertNotIn("blog-hero-reference.png", src)


if __name__ == "__main__":
    unittest.main()
