# Pipeline fix queue

## INC-20260827-1305-cover-prompt-budget-victoria
status: open
run_date: 2026-08-27
role: excalibur-blog-cover
topic_id: B16
article_dir: memory/blog/articles/B16-lichnoe-chislo-dnya-lomaet-ozhidanie-otveta
severity: medium
category: script

### What went wrong
- Cover `--write-batch` failed `COVER PROMPT BLOCKER` at 4252 chars (max 3500) while agent `scene_hint` already sat in the 80–140 / 100–220 band.
- Tenant `quad-style-victoria-studio.json` prefix + type/hair locks were stacked on the old Cursor-era shared ban / TEXT LANGUAGE / TOKEN BURN RATE / long inline TEXT LOCK boilerplate.

### How the agent recovered this run
- Reclaimed shared extras in `scripts/excalibur_blog_cover_quad_prompt.py` (compact caps + shorter host_reference locks). Hair lock phrase kept. Prompt landed at 3237.
- Did not empty scene_hint.

### Durable fix needed before next run
- Keep tenant style prefix compact enough that host_reference + 4 short hints stay under 3500 without Cover emptying prose.
- Fixer: confirm compact caps still leave `hair color copied exactly from reference photo, same root depth, do not lighten, no platinum` intact in the built prompt.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `memory/cover/quad-style-victoria-studio.json`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260827-1750-cover-site-base-env
status: open
run_date: 2026-08-27
role: excalibur-blog-cover
topic_id: B17
article_dir: memory/blog/articles/B17-karta-dnya-esli-on-prochital-i-molchit
severity: medium
category: env

### What went wrong
- First `excalibur_blog_kie_gpt_image2_api.py` call failed before createTask: batch `input_urls` keep git-safe `{{SITE_BASE}}`, but Cloud env had no `PUBLIC_SITE_URL` / `WP_SITE_URL`. Script cannot expand the placeholder.
- Tenant `public_site_url` already exists in `shared/tenant-config.json`; Cover must not write a live host into committed batch.

### How the agent recovered this run
- Set `PUBLIC_SITE_URL` for the shell from tenant `public_site_url` (runtime only).
- Set batch `prefer_local_reference` to `memory/cover/assets/victoria.png` (same as B16) so File Upload carries the face lock without rewriting committed `{{SITE_BASE}}` urls.
- One billed create after that setup. No MCP fallback.

### Durable fix needed before next run
- `expand_input_urls` should fall back to tenant `public_site_url` when env is unset, still keeping artifacts as `{{SITE_BASE}}`.
- Or Cloud Secrets must include `PUBLIC_SITE_URL` for Cover/Kie runs.

### Suggested files to inspect/change
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_site_base.py`
- `shared/tenant-config.json`

### Secrets
- none recorded

### Fixer resolution
- pending
