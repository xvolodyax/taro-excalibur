# Pipeline fix queue

## INC-20260827-1305-cover-prompt-budget
status: open
run_date: 2026-08-27
role: excalibur-blog-cover
topic_id: B15
article_dir: memory/blog/articles/B15-on-revnuet-ili-eto-ne-lyubov
severity: medium
category: prompt

### What went wrong
- Tenant victoria-studio style prefix + typography locks + triple TEXT LOCK essays pushed the quad prompt to 4395 chars (max 3500) while cover/inline scene_hint were already inside 80–140 / 100–220.

### How the agent recovered this run
- Reclaimed shared style/ban/TEXT LOCK boilerplate in `scripts/excalibur_blog_cover_quad_prompt.py` (did not empty scene_hint). Prompt 3236 / 3500. Hair lock phrase kept.

### Durable fix needed before next run
- Keep compact caps on tenant style_prefix / inline suffix so host_reference + hair lock still fits under 3500 on first `--write-batch`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `memory/cover/quad-style-victoria-studio.json`

### Secrets
- none recorded

### Fixer resolution
- pending
