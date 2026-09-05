"""One-window subagent chain + Gemini text model policy."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_subagent_hook import decide  # noqa: E402


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("unclosed YAML frontmatter")
    data: dict[str, str] = {}
    key: str | None = None
    chunks: list[str] = []
    for line in text[4:end].splitlines():
        if line.startswith(" ") and key:
            chunks.append(line.strip())
            continue
        if ":" in line and not line.startswith(" "):
            if key is not None:
                data[key] = " ".join(chunks).strip().strip("\"'")
            key, rest = line.split(":", 1)
            key = key.strip()
            chunks = [rest.strip().lstrip("|").strip()]
    if key is not None:
        data[key] = " ".join(chunks).strip().strip("\"'")
    return data


class SubagentChainPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(
            (ROOT / "shared/pipeline-model-policy.json").read_text(encoding="utf-8")
        )
        cls.text_agents = set(cls.policy["text_agents"])
        cls.inherit_agents = set(cls.policy["inherit_agents"])
        cls.expected = cls.text_agents | cls.inherit_agents

    def test_policy_lists_are_disjoint_and_complete(self) -> None:
        self.assertFalse(self.text_agents & self.inherit_agents)
        files = {p.stem for p in (ROOT / "agents").glob("excalibur-blog-*.md")}
        self.assertEqual(files, self.expected)
        self.assertEqual(self.policy["text_model"], "gemini-3.8-flash")
        self.assertEqual(self.policy["text_model_id"], "gemini-3.8-flash")
        self.assertEqual(self.policy["reasoning_effort"], "low")
        self.assertEqual(self.policy["model_params"]["reasoning_effort"], "low")
        self.assertEqual(self.policy["text_model_slug"], "gemini-3.8-flash")
        self.assertEqual(self.policy["reasoning_effort_override"], "high")
        self.assertIn("Vladimir", self.policy["reasoning_effort_override_rule"])
        self.assertFalse(self.policy["text_fallback_allowed"])
        self.assertEqual(self.policy["text_fallback_action"], "FAIL")
        anti = self.policy["anti_burn"]
        self.assertEqual(anti["writer_body_passes"], 1)
        self.assertFalse(anti["enricher_allowed"])
        self.assertFalse(anti["read_loop_allowed"])
        self.assertEqual(anti["after_package_pass"], "EXIT")

    def test_agent_models_match_policy(self) -> None:
        for name in sorted(self.expected):
            fm = parse_frontmatter(
                (ROOT / "agents" / f"{name}.md").read_text(encoding="utf-8")
            )
            want = (
                "gemini-3.8-flash"
                if name in self.text_agents
                else "inherit"
            )
            self.assertEqual(fm.get("model"), want, name)
            if name in self.text_agents:
                self.assertEqual(fm.get("reasoning_effort"), "low", name)
            self.assertEqual(fm.get("is_background"), "false", name)

    def test_specialists_forbid_nested_task(self) -> None:
        for name in sorted(self.expected - set(self.policy["orchestrators"])):
            body = (ROOT / "agents" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("## Цепочка (HARD)", body, name)
            self.assertIn("Task(excalibur-blog-*)", body, name)
            self.assertIn("/in-cloud", body, name)

    def test_writer_does_not_launch_sol(self) -> None:
        writer = (ROOT / "agents/excalibur-blog-writer.md").read_text(encoding="utf-8")
        self.assertIn("вызываешь `Task(excalibur-blog-sol)`", writer)
        self.assertIn("**не**", writer)
        self.assertNotIn("накладывает **Sol** (`Task(excalibur-blog-sol)`)", writer)

    def test_cover_skill_does_not_task_cover_text(self) -> None:
        skill = (ROOT / "skills/cover-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Не вызывай `Task(excalibur-blog-cover-text)`", skill)
        self.assertNotIn("`Task(excalibur-blog-cover-text)` →", skill)

    def test_specialist_skills_disable_auto_invoke(self) -> None:
        skip = {"director-excalibur-blog", "setup-excalibur-blog"}
        for skill in (ROOT / "skills").glob("*/SKILL.md"):
            if skill.parent.name in skip:
                text = skill.read_text(encoding="utf-8")
                self.assertNotIn("disable-model-invocation: true", text.split("---", 2)[1])
                continue
            fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
            self.assertEqual(fm.get("disable-model-invocation"), "true", skill.parent.name)

    def test_docs_and_canon_files_exist(self) -> None:
        for rel in (
            "docs/cursor/README.md",
            "docs/cursor/SOURCE.md",
            "docs/cursor/subagents.md",
            "docs/cursor/automations.md",
            "docs/cursor/agents-window.md",
            "docs/cursor/models.md",
            "docs/cursor/hooks-and-skills.md",
            "shared/subagent-chain.md",
            "shared/pipeline-model-policy.json",
            ".cursor/hooks.json",
            "scripts/excalibur_blog_subagent_hook.py",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)
        source = (ROOT / "docs/cursor/SOURCE.md").read_text(encoding="utf-8")
        self.assertIn("https://cursor.com/docs/subagents", source)
        self.assertIn("https://cursor.com/docs/cloud-agent/automations", source)
        chain = (ROOT / "shared/subagent-chain.md").read_text(encoding="utf-8")
        self.assertNotIn("WAIT.", chain)
        canon = json.loads((ROOT / "shared/pipeline-canon.json").read_text(encoding="utf-8"))
        self.assertEqual(canon["text_model"], "gemini-3.8-flash")
        self.assertEqual(canon["reasoning_effort"], "low")
        self.assertEqual(canon["anti_burn"]["after_package_pass"], "EXIT")
        self.assertIn("PASS", (ROOT / "shared/subagent-chain.md").read_text(encoding="utf-8"))
        self.assertIn("EXIT", (ROOT / "shared/subagent-chain.md").read_text(encoding="utf-8"))

    def test_plugin_trees_match(self) -> None:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/excalibur_blog_sync_cursor_trees.py")],
            check=True,
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        pairs = (
            ("agents", ".cursor/agents"),
            ("skills", ".cursor/skills"),
            ("rules", ".cursor/rules"),
        )
        for src_name, dest_name in pairs:
            src = ROOT / src_name
            dest = ROOT / dest_name
            src_files = sorted(p.relative_to(src) for p in src.rglob("*") if p.is_file())
            dest_files = sorted(p.relative_to(dest) for p in dest.rglob("*") if p.is_file())
            self.assertEqual(src_files, dest_files, (src_name, dest_name))
            for rel in src_files:
                self.assertEqual(
                    (src / rel).read_bytes(),
                    (dest / rel).read_bytes(),
                    f"{src_name}/{rel}",
                )


class SubagentHookTest(unittest.TestCase):
    def _run(self, payload: dict) -> dict:
        return decide(payload)

    def test_denies_cloud_environment(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "excalibur-blog-writer",
                    "environment": "cloud",
                },
            }
        )
        self.assertEqual(out["permission"], "deny")
        self.assertIn("cloud", out["agent_message"].lower())

    def test_denies_task_director(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {"subagent_type": "excalibur-blog-director"},
            }
        )
        self.assertEqual(out["permission"], "deny")

    def test_denies_background_pipeline_agent(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "excalibur-blog-sol",
                    "run_in_background": True,
                },
            }
        )
        self.assertEqual(out["permission"], "deny")

    def test_denies_nested_task_from_writer_transcript(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as fh:
            fh.write("---\nname: excalibur-blog-writer\n---\nYou are writer\n")
            path = fh.name
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "transcript_path": path,
                "tool_input": {"subagent_type": "excalibur-blog-sol"},
            }
        )
        self.assertEqual(out["permission"], "deny")
        self.assertIn("специалист", out["agent_message"].lower())

    def test_allows_director_to_launch_writer(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "excalibur-blog-writer",
                    "model": "gemini-3.8-flash",
                },
            }
        )
        self.assertEqual(out["permission"], "allow")

    def test_denies_text_role_fallback_to_inherit_or_default(self) -> None:
        for fallback_model in ["inherit", "default"]:
            out = self._run(
                {
                    "hook_event_name": "preToolUse",
                    "tool_name": "Task",
                    "tool_input": {
                        "subagent_type": "excalibur-blog-writer",
                        "model": fallback_model,
                    },
                }
            )
            self.assertEqual(out["permission"], "deny")
            self.assertIn("fallback", out["agent_message"].lower())
            self.assertIn("fail only", out["agent_message"].lower())

    def test_denies_unsupported_model_for_text_role(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "excalibur-blog-title",
                    "model": "gpt-4o",
                },
            }
        )
        self.assertEqual(out["permission"], "deny")
        self.assertIn("запрещена", out["agent_message"].lower())

    def test_allows_gemini_slug_for_text_role(self) -> None:
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {
                    "subagent_type": "excalibur-blog-title",
                    "model": "gemini-3.8-flash-high",
                },
            }
        )
        self.assertEqual(out["permission"], "allow")

    def test_allows_setup_to_launch_voice(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as fh:
            fh.write("---\nname: excalibur-blog-setup\n---\nSetup chat\n")
            path = fh.name
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "transcript_path": path,
                "tool_input": {
                    "subagent_type": "excalibur-blog-setup-voice",
                    "model": "gemini-3.8-flash",
                },
            }
        )
        self.assertEqual(out["permission"], "allow")

    def test_allows_builtin_explore_from_specialist(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as fh:
            fh.write("---\nname: excalibur-blog-research\n---\n")
            path = fh.name
        out = self._run(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "transcript_path": path,
                "tool_input": {"subagent_type": "explore"},
            }
        )
        self.assertEqual(out["permission"], "allow")

    def test_denies_best_of_n(self) -> None:
        out = self._run(
            {
                "hook_event_name": "subagentStart",
                "subagent_type": "best-of-n-runner",
            }
        )
        self.assertEqual(out["permission"], "deny")

    def test_hook_cli_reads_stdin(self) -> None:
        payload = json.dumps(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Task",
                "tool_input": {"subagent_type": "excalibur-blog-director"},
            }
        )
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/excalibur_blog_subagent_hook.py")],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["permission"], "deny")


class TokenBurnDefaultsTest(unittest.TestCase):
    """No default reasoning_effort=high for article writers; high is override-only."""

    WRITER_PATHS = (
        "agents/excalibur-blog-writer.md",
        "agents/excalibur-blog-sol.md",
        "agents/excalibur-blog-title.md",
        "agents/excalibur-blog-description.md",
        "agents/excalibur-blog-cover-text.md",
        "shared/pipeline-model-policy.json",
        "shared/pipeline-canon.json",
    )

    def test_no_default_reasoning_effort_high_for_article_writers(self) -> None:
        for rel in self.WRITER_PATHS:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"(?m)^reasoning_effort:\s*high\s*$",
                f"default YAML high left in {rel}",
            )
            self.assertNotRegex(
                text,
                r'"reasoning_effort":\s*"high"',
                f"default JSON high left in {rel}",
            )

    def test_policy_default_is_low_override_is_high(self) -> None:
        policy = json.loads(
            (ROOT / "shared/pipeline-model-policy.json").read_text(encoding="utf-8")
        )
        self.assertEqual(policy["reasoning_effort"], "low")
        self.assertEqual(policy["reasoning_effort_override"], "high")
        self.assertIn("override", policy["reasoning_effort_override_rule"].lower())

    def test_writer_and_director_exit_after_pass(self) -> None:
        writer = (ROOT / "agents/excalibur-blog-writer.md").read_text(encoding="utf-8")
        director = (ROOT / "agents/excalibur-blog-director.md").read_text(encoding="utf-8")
        chain = (ROOT / "shared/subagent-chain.md").read_text(encoding="utf-8")
        for blob in (writer, director, chain):
            self.assertIn("EXIT", blob)
            self.assertIn("один", blob.lower())


if __name__ == "__main__":
    unittest.main()
