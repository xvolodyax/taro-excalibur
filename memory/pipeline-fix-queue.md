# Pipeline fix queue

Durable incident memory. Append-only until Fixer marks `status: fixed`.

## INC-20260829-1753-cover-prompt-budget
status: open
run_date: 2026-08-29
role: excalibur-blog-cover
topic_id: B23
article_dir: memory/blog/articles/B23-on-zashel-v-set-i-molchit
severity: medium
category: script

### What went wrong
- `--write-batch` failed with COVER PROMPT BLOCKER: prompt 4355 chars vs max 3500.
- Cover/inline `scene_hint` were already in the documented band; overflow came from shared style prefix + hook-type lock + per-panel TEXT LOCK wrappers on the victoria-studio tenant.

### How the agent recovered this run
- Reclaimed shared lock text in `scripts/excalibur_blog_cover_quad_prompt.py` (compact caps, shorter TEXT LANGUAGE / TEXT LOCK / COVER TEXT LOCK wrappers).
- Did not empty `scene_hint`. Prompt landed at 3394. Identity gate PASS. One billed Kie gen after that.

### Durable fix needed before next run
- Keep tenant style prefix + TEXT LOCK under the 3500 budget without asking Cover to delete scene_hint.
- Add a unit check that victoria-studio + 4 short hints + 4 labels stays ≤3500.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `tests/test_cover_text.py`

### Secrets
- none recorded

### Fixer resolution
- pending
