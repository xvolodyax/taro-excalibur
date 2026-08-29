# Pipeline fix queue

## INC-20260828-1750-cover-host-local-expand
status: fixed
run_date: 2026-08-28
role: excalibur-blog-cover
topic_id: B20
article_dir: memory/blog/articles/B20-karta-dnya-esli-on-otmenil-svidanie
severity: medium
category: script

### What went wrong
- `quad_manifest.py` still defaults `style_file` to pink-cat collage; Cover had to set `victoria-studio` by hand.
- First `--write-batch` blew 3500 chars because host_reference reused cat-era ban/essay + pink highlight, and identity-gate opener was missing.
- First Kie CLI exit (no `createTask`) required `PUBLIC_SITE_URL` to expand git-safe `{{SITE_BASE}}` even when `prefer_local_reference` would upload `viktoriaref.png`.

### How the agent recovered this run
- Overrode style in `quad-manifest.json`; reclaimed host_reference prompt (identity opener + gold + local `viktoriaref`).
- Patched Kie script to skip SITE_BASE expand when prefer_local is set.
- One billed create after the pre-task expand fix. Face verdict left to Hall.

### Durable fix needed before next run
- Manifest should inherit `tenant-config.cover_files.style_preset`.
- Identity opener + prefer_local `viktoriaref` must be default for `cover_mode=host_reference`.
- Kie must not require `PUBLIC_SITE_URL` when local face upload is already requested.

### Suggested files to inspect/change
- `scripts/excalibur_blog_quad_manifest.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`

### Secrets
- none recorded

### Fixer resolution
- status: fixed
- fixed_at: 2026-08-29
- fix_summary: B21 Cover landed remaining durable scripts. Manifest already inherits tenant style_preset (victoria-studio). Prompt builder starts with viktoriaref identity opener + hair lock, gold highlight, prefer_local batch. Kie skips SITE_BASE expand when prefer_local upload is set.
- files_changed:
  - `scripts/excalibur_blog_cover_quad_prompt.py`
  - `scripts/excalibur_blog_kie_gpt_image2_api.py`
- checks_run:
  - `python3 -m unittest tests.test_cover_identity tests.test_cover_text`
  - B21 Kie create_attempts=1 + split PASS
- commit: 95ae9b3

## INC-20260829-0034-title-robot-h1
status: fixed
run_date: 2026-08-29
role: excalibur-blog-title
topic_id: B20
article_dir: memory/blog/articles/B20-karta-dnya-esli-on-otmenil-svidanie
severity: medium
category: prompt

### What went wrong
- Owner: B20 H1 «Карта дня возвращает твой вечер, если он отменил свидание без новой даты» звучит топорно, как робот.
- Title skill требовал «сильный глагол» → агент клеил слоган («возвращает вечер») и канцелярит («без новой даты»).
- Человечный эталон владельца: «Карта дня, если он отменил свидание и не назвал новое время».

### How the agent recovered this run
- Durable contract rewrite (this fix). B20 body not retitled in the same change unless owner asks.

### Fixer resolution
- status: fixed
- fixed_at: 2026-08-29
- fix_summary:
  - Title skill/agent: spoken H1 over slogan verb; эталон владельца в контракте.
  - article-style + bad-outputs: тот же эталон/антиэталон.
  - Тест `test_title_prefers_spoken_h1_over_slogan_verb`.
- files_changed:
  - `skills/title-excalibur-blog/SKILL.md`
  - `agents/excalibur-blog-title.md`
  - `shared/article-style.md`
  - `shared/soul-examples/bad-outputs.md`
  - `shared/pipeline-canon.json`
  - `tests/test_title_subject.py`
- checks_run:
  - `python3 -m unittest tests.test_title_subject tests.test_title_lead_agents tests.test_subagent_chain_and_models`
- commit: pending
