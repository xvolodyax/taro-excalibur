# Pipeline fix queue

## INC-20260828-1750-cover-host-local-expand
status: open
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
- pending
