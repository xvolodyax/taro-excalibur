# Pipeline fix queue

## INC-20260920-0917-director-openai-ip-not-authorized
status: open
run_date: 2026-09-20
role: excalibur-blog-director
slot: утро
severity: blocker
category: env

### What went wrong
- Cloud probe `scripts/chat_completions.py --model gpt-5.5` → HTTP 401 `ip_not_authorized` («Your IP is not authorized to make this request.»).
- Ключ Владимира на месте (`OPENAI_API_KEY` sk-proj, len 164). Egress: `3.23.186.103`, `18.223.85.25`.
- Текст статьи / H1 / Sol / description / cover-text с Cloud писать нельзя: канон `written_by: openai-api-gpt-5.5`, fallback на Gemini / inherit / Cursor model запрещён.
- Scout / research / cover / publish не стартовали (anti-burn + явный EXIT на 401).
- Self-hosted workers: 0. `/workspace/openai-fallback/` недоступен.
- Утренней 20.09 на сайте ещё нет (newest live = вечер 19.09).

### How the agent recovered this run
- FAIL ONLY + EXIT. Статья не начата. LIVE не трогали (GET listing only).
- Восстановлены `scripts/chat_completions.py` + `tests/test_chat_completions.py` (пропали с main после art-pipeline).
- Журнал live H1/slug: `memory/blog/journal/site_live_titles.jsonl` (seed с listing, Jaccard≥0.45 / same slug = hard-block для бокса).
- Пометка: бокс-catch-up должен дожать слот утро 20.09 сам.

### Durable fix needed before next run
- Разрешить egress IP Cloud в OpenAI project / IP allowlist ключа Владимира, либо писать текст только с бокса, где IP уже в allowlist.
- Не крутить Cloud Scout/Writer при повторном 401: сразу EXIT.

### Suggested files to inspect/change
- `scripts/chat_completions.py`
- OpenAI project IP allowlist (вне репо)

### Secrets
- none recorded

### Fixer resolution
status: open

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
