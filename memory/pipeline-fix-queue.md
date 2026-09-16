# Pipeline fix queue

## INC-20260916-0918-director-openai-ip-not-authorized
status: open
run_date: 2026-09-16
role: excalibur-blog-director
slot: morning-0900-relations
topic_id: (not started — blocked at preflight text API)
severity: blocker
category: env

### What went wrong
- Slot **утро 09:00 MSK / острый запрос / сайт upload→approve→publish** for 2026-09-16. Дзен по RSS сам. Hall только будильник — H1 не задан.
- `OPENAI_API_KEY` present in Cloud Secrets (164 chars, `sk-proj…`). `OPENAI_BASE_URL` unset.
- Director restored `scripts/chat_completions.py` and probed once: `POST https://api.openai.com/v1/chat/completions` `model=gpt-5.5` → **401** `ip_not_authorized`.
- Cloud egress IP this run: `3.18.66.46`. Same blocker as evening slots 11–15.09.
- TEXT CANON (hard): body/H1/description/cover-text **only** via OpenAI API gpt-5.5; stamp `written_by: openai-api-gpt-5.5`. Gemini / Cursor catalog forbidden. **401 → FAIL + EXIT.**

### How the agent recovered this run
- Did **not** fall back to Gemini, inherit, or Director-written prose.
- Did **not** start Scout / Research / Title / Writer / Sol / Cover / Kie / Publish.
- Did **not** touch live anti-dup GET: id107 свекровь, id109 развод, id111 давление родных на свадьбу (blog index), stories приворот/сглаз — all HTTP 200 where checked.
- Box draft pack `/workspace/openai-fallback/packs/2026-09-16-morning/` not present in Cloud workspace.

### Durable fix needed before next Cloud run
- Whitelist Cursor Cloud Agent egress IP(s) on OpenAI project **or** approved relay/`OPENAI_BASE_URL` for Cloud Agents.
- Re-run morning slot only after `python3 scripts/chat_completions.py --user ping` returns 200 for `gpt-5.5`.

### Secrets
- `OPENAI_API_KEY` configured; IP whitelist missing

### Fixer resolution
- pending — env/API blocker, cannot fix in repo code

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
