# Pipeline fix queue

## INC-20260906-0715-cover-prompt-budget-host-local-ref
status: open
run_date: 2026-09-06
role: excalibur-blog-cover
topic_id: B42
article_dir: memory/blog/articles/B42-on-stavit-usloviya-v-otnosheniyah
severity: medium
category: script

### What went wrong
- After `--write-batch` the victoria-studio identity prefix plus long B42 H2/TEXT LOCK lines made the MCP prompt 3646 chars (max 3500). Scene hints were already in range; emptying them is forbidden.
- `excalibur_blog_quad_manifest.py --merge` still writes `style_file` pink-cat / `style_preset` tenant_unset. Cover had to override to `victoria-studio` before batch.
- `PUBLIC_SITE_URL` still unset (same cluster as INC-20260905-1935). Prompt script honored `prefer_local_reference` only for cat-hero, so host i2i would expand `{{SITE_BASE}}` and exit before createTask.

### How the agent recovered this run
- Reclaimed shared prompt text (shorter TEXT LANGUAGE LOCK; gold highlight / editorial type when design-code forbids `#FF1493`). Did not empty scene_hint.
- Set manifest `style_file` to `memory/cover/quad-style-victoria-studio.json`.
- Prompt script now sets `prefer_local_reference` + `local_reference` for host when the style asks; Kie skips live expand if that flag is set and uploads `Виктория.png` before the one billed createTask.

### Durable fix needed before next run
- Manifest merge should take tenant `style_preset` from `shared/tenant-config.json`, not pink-cat default.
- Keep host `prefer_local_reference` in prompt/Kie scripts; inject `PUBLIC_SITE_URL` in Cloud env.

### Suggested files to inspect/change
- `scripts/excalibur_blog_quad_manifest.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `shared/tenant-config.json`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260905-1935-cover-public-site-url-unset
status: open
run_date: 2026-09-05
role: excalibur-blog-cover
topic_id: B41
article_dir: memory/blog/articles/B41-on-napisal-edu-i-propal
severity: high
category: env

### What went wrong
- `excalibur_blog_kie_gpt_image2_api.py` exited before `createTask`: batch `input_urls` keep `{{SITE_BASE}}`, but `PUBLIC_SITE_URL` / `WP_SITE_URL` / `WP_HOME` were unset in Cloud env.
- Cyrillic filename in the hosted hero path also failed a raw HEAD (`UnicodeEncodeError`), so a WP-only first fetch is brittle.

### How the agent recovered this run
- Set `PUBLIC_SITE_URL` at runtime from `shared/tenant-config.json` `public_site_url` (not written into artifacts).
- Set batch `prefer_local_reference` + `local_reference` to `memory/cover/assets/Виктория.png` so the first billed `createTask` uses a File Upload of the canon face, not a live-host fetch.
- Did not start a second billed create.

### Durable fix needed before next run
- Inject `PUBLIC_SITE_URL` (or `WP_SITE_URL`) into Cloud Secrets/env for Cover.
- `cover_quad_prompt.py` should honor style `prefer_local_reference` + `local_reference` for `host_reference` (not only cat-hero), so Cyrillic `Виктория.png` uploads on first create.
- URL-encode Cyrillic media filenames when expanding `{{SITE_BASE}}` for HEAD/GET.

### Suggested files to inspect/change
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_site_base.py`
- `memory/cover/quad-style-victoria-studio.json`

### Secrets
- none recorded

### Fixer resolution
- pending
