# Pipeline fix queue

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
