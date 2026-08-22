# Pipeline fix queue

Durable incident memory for Excalibur BLOG. See `shared/pipeline-incident-fix-contract.md`.

## INC-20260822-0812-cover-hero-url-catbox
status: open
run_date: 2026-08-22
role: excalibur-blog-cover
topic_id: B02
article_dir: memory/blog/articles/B02-chto-on-chuvstvuet
severity: low
category: script

### What went wrong
- Skill step 1 still runs `excalibur_blog_hero_reference_url.py`, which tries catbox then 0x0.
- Catbox returned HTTP 412; 0x0 timed out on TLS. Script exited HERO BLOCKER.
- Tenant canon is local Victoria via `prefer_local_reference` + File Upload. Hosted catbox URL is forbidden for production hero.

### How the agent recovered this run
- Left `blog-hero.json` unchanged (`reference_url_hosted` empty, source local Victoria).
- Built batch with `prefer_local_reference=true` and `local_reference=memory/cover/assets/виктория.png`.
- Kie uploaded the local sheet once and created the single billed task.

### Durable fix needed before next run
- `excalibur_blog_hero_reference_url.py` should no-op / print OK when `prefer_local_reference` and the local Victoria file exist.
- Cover skill step 1 should say: skip remote host if local Victoria + prefer_local is the tenant path.

### Suggested files to inspect/change
- `scripts/excalibur_blog_hero_reference_url.py`
- `skills/cover-excalibur-blog/SKILL.md`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260822-1325-cover-prompt-credit-budget
status: open
run_date: 2026-08-22
role: excalibur-blog-cover
topic_id: B03
article_dir: memory/blog/articles/B03-shodyatsya-li-vashi-daty-v-otnosheniyah
severity: low
category: prompt

### What went wrong
- B03 cover-text sticky plus the long shared «Do not paint host credit… Pillow overlays…» lock pushed `build_prompt` to 3531–3683 chars after scene_hints were already in the 80–140 / 100–220 band.
- Skill says reclaim shared style/ban/Inline-all text, do not empty `scene_hint`.

### How the agent recovered this run
- Left cover/inline `scene_hint` informative (olive shirt + checking; cover-text labels).
- Compacted the shared credit lock to «No host credit, byline, site or URL on canvas — Pillow stamps Victoria after split.»
- Updated `tests/test_host_credit_overlay.py` assertions to the short lock.
- Batch rebuilt at 3447 chars. Hero URL step reused INC-20260822-0812: local Victoria + `prefer_local_reference`, no catbox.

### Durable fix needed before next run
- Keep the credit lock short. Next tenant sticky + long H2 TEXT LOCKs will blow 3500 again if the essay returns.
- `hero_reference_url.py` still needs the no-op from INC-20260822-0812.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `tests/test_host_credit_overlay.py`
- `scripts/excalibur_blog_hero_reference_url.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260822-1645-cover-textlock-budget
status: open
run_date: 2026-08-22
role: excalibur-blog-cover
topic_id: B04
article_dir: memory/blog/articles/B04-chto-budet-etim-vecherom-v-otnosheniyah
severity: low
category: prompt

### What went wrong
- After INC-20260822-1325 short credit lock, B04 still hit COVER PROMPT BLOCKER at 3512 chars.
- Cover-text labels + long H2 TEXT LOCKs ×3 blew the 3500 budget while scene_hint stayed in 80–140 / 100–220.

### How the agent recovered this run
- Kept scene_hint informative (cream denim jacket + quiet knowing; cover-text labels).
- Compacted repeated TEXT LOCK suffix: «Every letter in Cyrillic, exactly as written.» → «Exact Cyrillic as written.»
- Batch rebuilt at 3455 chars. Hero path reused INC-20260822-0812: prefer_local + local Victoria, no catbox.

### Durable fix needed before next run
- Keep TEXT LOCK wrapper short. Next long hook/sticky/H2 set will blow 3500 again if the essay returns.
- `hero_reference_url.py` still needs the no-op from INC-20260822-0812.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_hero_reference_url.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260822-1652-cover-gutter-bleed-redo
status: open
run_date: 2026-08-22
role: excalibur-blog-cover
topic_id: B04
article_dir: memory/blog/articles/B04-chto-budet-etim-vecherom-v-otnosheniyah
severity: medium
category: qa

### What went wrong
- First B04 canvas: auto split rejected gutter (h offset 58px, crop_loss 0.13). Mechanical 50/50 left a cream jacket/table strip on `inline-02`.
- Owner-directed full-canvas redo (one billed job) with gutters ON center 1024/576. New canvas still painted cover table below y=576; auto again rejected gutter (h offset 47.5px, crop_loss 0.136). Mechanical cut left ~18px cream bleed on `inline-02`.

### How the agent recovered this run
- One Kie redo only (task ac3b5a8dc74f0c6d062eef8dbde2c427). No second billed gen.
- After apply+credit, Pillow filled rows 0–17 of `inline-02` with #FFFFFF. Did not regenerate one panel.
- Inline-01/03 tops were already white. No faces on inlines.

### Durable fix needed before next run
- Prompt must keep host/table inside top-left (content must not cross y=576 / x=1024).
- Split may need a post-cut bleed trim when mechanical fallback leaves a foreign cream band.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_cover_quad_split.py`

### Secrets
- none recorded

### Fixer resolution
- pending
