"""Kie GPT Image 2 poll / resume helpers (INC-20260831-1508)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_kie_gpt_image2_api import (  # noqa: E402
    DEFAULT_MAX_CREATE_RETRIES,
    DEFAULT_MAX_WAIT_SECONDS,
    KiePollWindowExhausted,
    KieRetryableFail,
    classify_record_info,
    existing_success_result,
    infer_resume_create_retries,
    is_cover_create_exhausted,
    poll_until_result,
    poll_window_exhausted_resume_cmd,
    refuse_cover_third_create,
    resolve_resume_task_id,
)


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def monotonic(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += float(seconds)


class KiePollResumeTest(unittest.TestCase):
    def test_default_max_wait_covers_2k_past_900(self) -> None:
        self.assertGreaterEqual(DEFAULT_MAX_WAIT_SECONDS, 1500)

    def test_infer_resume_retries_first_job_keeps_one(self) -> None:
        self.assertEqual(infer_resume_create_retries({}), DEFAULT_MAX_CREATE_RETRIES)
        self.assertEqual(
            infer_resume_create_retries({"create_attempt": 1, "state": "poll_window_exhausted"}),
            1,
        )

    def test_infer_resume_retries_recreate_is_zero(self) -> None:
        self.assertEqual(
            infer_resume_create_retries(
                {"create_attempt": 2, "retry_of": {"retry_kind": "server_500"}}
            ),
            0,
        )
        self.assertEqual(infer_resume_create_retries({"create_attempts": 2}), 0)

    def test_resolve_resume_reads_task_record(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "kie-image-task.json"
            path.write_text('{"task_id": "abc123", "create_attempt": 1}\n', encoding="utf-8")
            task_id, record = resolve_resume_task_id(
                explicit_task_id="",
                resume=True,
                task_record_path=path,
            )
            self.assertEqual(task_id, "abc123")
            self.assertEqual(record.get("create_attempt"), 1)

    def test_resolve_resume_without_record_raises(self) -> None:
        import tempfile

        from excalibur_blog_kie_gpt_image2_api import KieApiError

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.json"
            with self.assertRaises(KieApiError) as ctx:
                resolve_resume_task_id(
                    explicit_task_id="",
                    resume=True,
                    task_record_path=path,
                )
            self.assertIn("--resume", str(ctx.exception))
            self.assertIn("no new create", str(ctx.exception))

    def test_resume_cmd_recreate_locks_retries_zero(self) -> None:
        first = poll_window_exhausted_resume_cmd("memory/blog/articles/B28-x")
        self.assertIn("--resume", first)
        self.assertNotIn("--max-create-retries 0", first)
        redo = poll_window_exhausted_resume_cmd("memory/blog/articles/B28-x", recreate=True)
        self.assertIn("--max-create-retries 0", redo)

    def test_late_poll_extend_then_success(self) -> None:
        clock = FakeClock()
        replies = [
            {"state": "generating"},
            {"state": "generating"},
            {"state": "generating"},
            {
                "state": "success",
                "resultJson": '{"resultUrls":["https://cdn.example/quad.png"]}',
            },
        ]

        def fake_query(**_kwargs):
            return replies.pop(0)

        with (
            patch("excalibur_blog_kie_gpt_image2_api.query_task", side_effect=fake_query),
            patch("excalibur_blog_kie_gpt_image2_api.time.monotonic", clock.monotonic),
            patch("excalibur_blog_kie_gpt_image2_api.time.sleep", clock.sleep),
        ):
            data = poll_until_result(
                record_url="https://example/record",
                api_key="test",
                task_id="job-1",
                poll_interval=1,
                max_wait=1,
                late_poll_extend=2,
            )
        self.assertEqual(data["state"], "success")
        self.assertEqual(replies, [])

    def test_late_poll_exhausted_raises_specific(self) -> None:
        clock = FakeClock()

        def always_generating(**_kwargs):
            return {"state": "generating"}

        with (
            patch(
                "excalibur_blog_kie_gpt_image2_api.query_task",
                side_effect=always_generating,
            ),
            patch("excalibur_blog_kie_gpt_image2_api.time.monotonic", clock.monotonic),
            patch("excalibur_blog_kie_gpt_image2_api.time.sleep", clock.sleep),
        ):
            with self.assertRaises(KiePollWindowExhausted) as ctx:
                poll_until_result(
                    record_url="https://example/record",
                    api_key="test",
                    task_id="job-still",
                    poll_interval=1,
                    max_wait=1,
                    late_poll_extend=1,
                )
        self.assertEqual(ctx.exception.task_id, "job-still")
        self.assertEqual(ctx.exception.last_state, "generating")
        self.assertIn("--task-id job-still", str(ctx.exception))
        self.assertIn("--max-create-retries 0", str(ctx.exception))

    def test_final_recordinfo_late_500_is_retryable(self) -> None:
        clock = FakeClock()
        replies = [
            {"state": "generating"},
            {"state": "generating"},
            {"state": "fail", "failCode": 500, "failMsg": "try again later"},
        ]

        def fake_query(**_kwargs):
            return replies.pop(0)

        with (
            patch("excalibur_blog_kie_gpt_image2_api.query_task", side_effect=fake_query),
            patch("excalibur_blog_kie_gpt_image2_api.time.monotonic", clock.monotonic),
            patch("excalibur_blog_kie_gpt_image2_api.time.sleep", clock.sleep),
        ):
            with self.assertRaises(KieRetryableFail) as ctx:
                poll_until_result(
                    record_url="https://example/record",
                    api_key="test",
                    task_id="job-late-500",
                    poll_interval=1,
                    max_wait=1,
                    late_poll_extend=0,
                )
        self.assertEqual(ctx.exception.task_id, "job-late-500")
        self.assertEqual(str(ctx.exception.fail_code), "500")

    def test_cover_create_exhausted_refuses_third_without_director_flag(self) -> None:
        exhausted = {
            "state": "fail",
            "create_attempts": 2,
            "retry_kind": "server_500",
            "failCode": 500,
            "cover_create_exhausted": True,
        }
        self.assertTrue(is_cover_create_exhausted(exhausted))
        self.assertTrue(
            is_cover_create_exhausted(
                {
                    "state": "fail",
                    "create_attempt": 2,
                    "retry_kind": "server_500",
                    "failCode": 500,
                }
            )
        )
        msg = refuse_cover_third_create(
            exhausted, director_same_batch=False, resume=False, task_id=""
        )
        self.assertIsNotNone(msg)
        assert msg is not None
        self.assertIn("third createTask", msg)
        self.assertIn("--director-same-batch", msg)
        self.assertIn("B30", msg)
        self.assertIsNone(
            refuse_cover_third_create(
                exhausted, director_same_batch=True, resume=False, task_id=""
            )
        )
        self.assertFalse(is_cover_create_exhausted({"state": "success", "create_attempts": 3}))

    def test_existing_success_skips_create_apply_only(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            result_path = Path(tmp) / "quad-mcp-result.json"
            result_path.write_text(
                '{"url": "https://cdn.example/quad.png"}\n', encoding="utf-8"
            )
            data = existing_success_result(
                result_path, {"state": "success", "create_attempts": 3}
            )
            self.assertIsNotNone(data)
            assert data is not None
            self.assertEqual(data["url"], "https://cdn.example/quad.png")
            self.assertIsNone(
                existing_success_result(
                    result_path, {"state": "fail", "create_attempts": 2}
                )
            )

    def test_docs_annotate_b30_director_same_batch(self) -> None:
        contract = (ROOT / "shared/kie-gpt-image-api-contract.md").read_text(encoding="utf-8")
        self.assertIn("B30", contract)
        self.assertIn("--director-same-batch", contract)
        self.assertIn("apply-only", contract)
        cover = (ROOT / "skills/cover-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("B30", cover)
        self.assertIn("--director-same-batch", cover)
        director = (ROOT / "skills/director-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("--director-same-batch", director)
        self.assertIn("B30", director)

    def test_classify_success_and_generating(self) -> None:
        self.assertIsNone(classify_record_info({"state": "generating"}, "t"))
        data = classify_record_info(
            {"state": "success", "resultJson": '{"resultUrls":["https://x"]}'},
            "t",
        )
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data["state"], "success")


if __name__ == "__main__":
    unittest.main()
