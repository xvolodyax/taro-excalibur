"""Scout --check-query must catch Cyrillic queries vs Latin ledger/live slugs.

INC-20260727-0805: «автопостинг вк» previously returned NO CANNIBALIZATION while
WP13778 /avtoposting-vk-make-google-sheets/ was already published.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_scout_helper import (  # noqa: E402
    check_overlap,
    load_published_title_topic_ids,
    load_reserved_topic_ids,
    next_b_topic_id,
    normalize_and_tokenize,
    transliterate_ru,
)


class ScoutHelperQuerySlugCoverTests(unittest.TestCase):
    def test_transliterate_avtoposting(self) -> None:
        self.assertEqual(transliterate_ru("автопостинг"), "avtoposting")
        self.assertEqual(normalize_and_tokenize("автопостинг вк"), {"avtop", "vk"})
        self.assertEqual(
            normalize_and_tokenize("avtoposting-vk-make-google-sheets"),
            {"avtop", "vk", "make", "googl", "sheet"},
        )

    def test_vk_autoposting_covers_ledger_slug(self) -> None:
        topics = [
            {
                "topic_id": "WP13778",
                "primary_query": "avtoposting vk make google sheets",
                "slug": "avtoposting-vk-make-google-sheets",
                "priority": "published",
            }
        ]
        warnings = check_overlap("автопостинг вк", topics, {"WP13778"})
        critical = [w for w in warnings if w["severity"] == "CRITICAL"]
        self.assertTrue(critical, warnings)
        self.assertTrue(
            any("SLUG KEYWORD COVER" in w["message"] for w in critical),
            critical,
        )
        self.assertEqual(critical[0]["topic_id"], "WP13778")

    def test_unrelated_query_no_slug_cover(self) -> None:
        topics = [
            {
                "topic_id": "WP13778",
                "primary_query": "avtoposting vk make google sheets",
                "slug": "avtoposting-vk-make-google-sheets",
                "priority": "published",
            }
        ]
        warnings = check_overlap("cookie баннер на сайт", topics, set())
        self.assertFalse(
            any("SLUG KEYWORD COVER" in str(w.get("message") or "") for w in warnings),
            warnings,
        )

    def test_exact_primary_still_critical(self) -> None:
        topics = [
            {
                "topic_id": "B25",
                "primary_query": "ai агенты для бизнеса",
                "slug": "ai-agenty-dlya-biznesa",
                "priority": "published",
            }
        ]
        warnings = check_overlap("ai агенты для бизнеса", topics, {"B25"})
        self.assertTrue(
            any("EXACT MATCH" in w["message"] for w in warnings if w["severity"] == "CRITICAL"),
            warnings,
        )

    def test_suggest_next_reads_published_titles_not_only_dated_ledger(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shared = root / "shared"
            shared.mkdir(parents=True)
            (shared / "published-articles.md").write_text(
                "# ledger\n\n"
                "| topic_id | slug | status | permalink |\n"
                "|----------|------|--------|-----------|\n"
                "| B23 | live-slug | live | /live-slug/ |\n",
                encoding="utf-8",
            )
            (shared / "published-titles.md").write_text(
                "| topic_id | slug | title | status |\n"
                "|----------|------|-------|--------|\n"
                "| B12 | old | Старый | live |\n"
                "| B31 | autumn | Осень | quality_review |\n",
                encoding="utf-8",
            )
            ids = load_published_title_topic_ids(root)
            self.assertEqual(ids, {"B12", "B31"})
            reserved = load_reserved_topic_ids(root)
            self.assertIn("B12", reserved)
            self.assertIn("B31", reserved)
            self.assertEqual(next_b_topic_id(reserved), "B32")

    def test_next_b_topic_id_empty_is_b01(self) -> None:
        self.assertEqual(next_b_topic_id(set()), "B01")
        self.assertEqual(next_b_topic_id({"LIVE", "WP13778"}), "B01")
        self.assertEqual(next_b_topic_id({"B09", "B1"}), "B10")


if __name__ == "__main__":
    unittest.main()
