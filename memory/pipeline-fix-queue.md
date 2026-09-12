# Pipeline fix queue

## INC-20260912-1610-director-openai-ip-not-authorized
status: open
run_date: 2026-09-12
role: excalibur-blog-director
topic_id: n/a
article_dir: n/a
severity: blocker
category: api
slot: день
date: 2026-09-12

### What went wrong
- Слот день 2026-09-12. Setup complete. `needs_scout`. Текстовый канон этого прогона: только OpenAI API `gpt-5.5` (ключ Владимира), stamp `written_by: openai-api-gpt-5.5`. Gemini и модели каталога Cursor как автор H1/тела/meta запрещены.
- `OPENAI_API_KEY` в env есть. Probe `POST https://api.openai.com/v1/chat/completions` model `gpt-5.5` вернул HTTP 401, `code=ip_not_authorized`, message «Your IP is not authorized to make this request.»
- По правилу слота: FAIL сразу, без подмены текстом Cursor/Gemini, без Scout→Publish.

### How the agent recovered this run
- Не восстанавливал. Статья не писалась. Scout / Research / Title / Writer / Sol / Description / Cover / Publish не запускались.
- Fallback на inherit/default/Gemini не применялся.

### Durable fix needed before next run
- Человек: добавить egress IP этого Cloud Agent / environment в allowlist ключа OpenAI (или снять IP restriction). Пока 401 `ip_not_authorized` — следующий слот тоже FAIL.
- Код не чинит IP-allowlist. Не менять текстовый канон на Gemini «чтобы прогнать слот».

### Suggested files to inspect/change
- Cloud Secrets / OpenAI project IP allowlist (вне репо)
- `memory/setup/status.json` (setup уже complete — не причина)

### Secrets
- none recorded

### Fixer resolution
status: needs-human
note: IP allowlist OpenAI. Fixer не подменяет автора текста.

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
status: fixed
fixed_at: 2026-09-09
fix_summary:
- `cover_quad_prompt.py` sets `prefer_local_reference` for host_reference (Виктория.png), not only cat-hero.
- `kie_gpt_image2_api.py` + `site_base.py`: PUBLIC_SITE_URL fallback from tenant-config; percent-encode Cyrillic media paths.
- Art canon 2026-09-09 landed in the same pass (Flare 2K, one job). Live articles not redrawn.
files_changed:
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_site_base.py`
- `scripts/excalibur_blog_art_canon.py`
checks_run:
- `python3 -m unittest tests/test_art_pipeline_2k_flare.py tests/test_cover_text.py`
commit: pending

## INC-20260909-art-one-2k-flare
status: fixed
run_date: 2026-09-09
role: fixer / art-canon
severity: high
category: prompt-contract
### What went wrong
- Risk of four separate 1K gens and stale `gpt-image-2-image-to-image`.
- Kie resolution fallback was `1K` if batch omitted resolution.
### Durable fix
- ONE `gpt-image-2-5-flare-image-to-image` at 2K; 2×2 white-gutter canvas; slice cover+inline-01..03.
- Cover cell: Victoria age 33, B14 Cyrillic cover-text ON image, brand line, no red frame.
- Inlines: no Victoria face. Do not redraw live articles.
files_changed:
- `scripts/excalibur_blog_art_canon.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `shared/blog-cover-quad-canvas-contract.md`
- `shared/kie-gpt-image-api-contract.md`
- cover skills/agents + tenant cover JSON
checks_run:
- `python3 -m unittest tests/test_art_pipeline_2k_flare.py`
commit: pending
