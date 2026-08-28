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

### Follow-up 2026-08-28 B19
- Eye lock phrase was added after the B16 reclaim; `--write-batch` failed again at 3999/3500 with short scene_hint.
- Reclaimed host_reference extras again (shorter TEXT LOCK / language lock / prefix compact 380; gold highlight, not pink). Exact hair + eye phrases kept.

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

## INC-20260828-0635-cover-site-base-env
status: open
run_date: 2026-08-28
role: excalibur-blog-cover
topic_id: B18
article_dir: memory/blog/articles/B18-paren-propal-posle-blizosti
severity: medium
category: env

### What went wrong
- Same gap as INC-20260827-1750: Cloud env has no `PUBLIC_SITE_URL` / `WP_SITE_URL`, while committed batch keeps git-safe `{{SITE_BASE}}`.
- Kie `expand_input_urls` still cannot expand without env; tenant `public_site_url` is already in `shared/tenant-config.json`.

### How the agent recovered this run
- Set `PUBLIC_SITE_URL` for the shell from tenant `public_site_url` (runtime only).
- Set batch `prefer_local_reference` to `memory/cover/assets/victoria.png` so File Upload carries the face lock without rewriting committed `{{SITE_BASE}}` urls.
- One billed create after that setup. No MCP fallback. Not a quality-redo.

### Durable fix needed before next run
- Same as INC-20260827-1750: `expand_input_urls` should fall back to tenant `public_site_url` when env is unset, still keeping artifacts as `{{SITE_BASE}}`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_site_base.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260828-1031-cover-victoria-sheet-missing
status: resolved
run_date: 2026-08-28
role: excalibur-blog-cover
topic_id: B19
article_dir: memory/blog/articles/B19-chislo-imeni-pokazyvaet-ego-ton-v-pare
severity: blocker
category: env

### What went wrong
- CANON LOCK 2026-08-28: Cover i2i may use only `memory/cover/assets/victoria-sheet.png`.
- That file is not on disk. `memory/cover/assets/` has README + `.gitkeep` only.
- `blog-hero.json` already records `png_on_disk: false`.
- Commit that locked the sheet also dropped the previous face file; no replacement PNG was added.
- Owner rule: STOP if the sheet is missing. Do not i2i from another face. Do not invent a face.

### How the agent recovered this run
- Stopped before manifest batch / Kie createTask.
- Did not substitute another face-ref.
- Did not generate a face from memory.
- Did not publish. Hall publishes.
- Wrote Cover fragment `status: BLOCKER` and listed the missing file.

### Follow-up 2026-08-28T10:40 (owner re-attach)
- Owner re-attached the same sheet. Platform advertised `/workspace/cover-refs/victoria-sheet.png`.
- Directory `cover-refs/` was created empty. `Read` = file not found. `inotify` 45s = no write.
- `Task(excalibur-blog-cover)` with `file_attachments` failed: `Failed to read attachment: /workspace/cover-refs/victoria-sheet.png`.
- Google Drive (connected): no `victoria-sheet.png`. WP `{{SITE_BASE}}/wp-content/uploads/excalibur/victoria-sheet.png` = 404.
- Cursor agent UI download: session not logged in.
- Still did not restore `victoria.png` / Alena / `character-sheet-2k`. Still no Kie. Text pack untouched.

### Durable fix needed before next run
- Chat-attach of PNG on this Cloud VM does **not** land a binary. Do not rely on `cover-refs/` or `image_files`.
- Owner must put the bytes on a channel the VM can read:
  1. `git add` + push `memory/cover/assets/victoria-sheet.png` on this branch, or
  2. upload that exact filename to the connected Google Drive, or
  3. bake the file into the environment snapshot.
- Then Cover re-runs: copy once to assets (no second face file) → identity gate → `--write-batch` → one Kie i2i → split/inject.
- Do not restore deleted alternate face files.

### Suggested files to inspect/change
- `memory/cover/assets/victoria-sheet.png`
- `memory/cover/blog-hero.json`
- `memory/cover/assets/README.md`

### Secrets
- none recorded

### Fixer resolution
- 2026-08-28: pulled Karuselka `cursor/carousel-2026-08-28-daa5` `carusel-memory/references/victoria-sheet.png` (250844 JPEG-in-.png). Rewrapped to real PNG 1280×720 / 829343 bytes at `memory/cover/assets/victoria-sheet.png`. Chat-attach is not the source. Cover may run. No second face file.
