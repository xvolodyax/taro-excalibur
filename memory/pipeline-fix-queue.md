# Pipeline fix queue

## INC-20260823-0630-cover-prefer-local-site-base
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B05
article_dir: memory/blog/articles/B05-chto-on-skryvaet-v-otnosheniyah-i-skazhet-li-pravdu
severity: high
category: script

### What went wrong
- First Kie run failed before createTask: batch `input_urls` keep git-safe `{{SITE_BASE}}`, Cloud env has no `PUBLIC_SITE_URL` / `WP_SITE_URL`, and `batch_mcp_args` required live expand even when `prefer_local_reference` is true.
- Tenant path is local Victoria PNG + File Upload. Catbox is forbidden. No billed task was created.

### How the agent recovered this run
- `expand_input_urls(..., allow_unexpanded=True)` when `prefer_local_reference` is set; File Upload still replaces `input_urls` before createTask.
- Batch file stays git-safe (`{{SITE_BASE}}` / local path). No live host written.

### Durable fix needed before next run
- Keep the skip: prefer_local File Upload must not require a live site URL.
- Document in Kie contract that local-ref tenants can generate without `PUBLIC_SITE_URL`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `shared/kie-gpt-image-api-contract.md`
- `tests/test_kie_prefer_local_site_base.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260823-0632-cover-host-still-life
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B05
article_dir: memory/blog/articles/B05-chto-on-skryvaet-v-otnosheniyah-i-skazhet-li-pravdu
severity: medium
category: prompt

### What went wrong
- First billed 2K i2i kept the hook, dusty-blue linen shirt, face-down phone and enamel medallion, but painted a clothing still-life instead of Victoria face LARGE left.
- Extra invented subtitle under the hook. Split cells were not crooked; owner allowed canvas redo only for crooked split, not host-miss quality.

### How the agent recovered this run
- First pass: no quality-redo. Director then authorized one full canvas rebuild. Second billed gen: Victoria FACE LARGE left, she WEARS the dusty-blue linen shirt; Pillow credit applied.

### Durable fix needed before next run
- First-try cover lock: face is the large subject; the linen shirt is worn, not a folded prop that replaces the host.
- Keep topic metaphor tiny (phone/medallion) so it cannot outrank the face.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `memory/cover/blog-hero.json`
- `memory/cover/quad-style-taro-seichas.json`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260823-0637-cover-gutter-still-off
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B05
article_dir: memory/blog/articles/B05-chto-on-skryvaet-v-otnosheniyah-i-skazhet-li-pravdu
severity: medium
category: prompt

### What went wrong
- Director-approved one full 2K redo: host face is now on cover.png. Split still chose mechanical_center because auto gutter was `gutter_too_far_from_center` (h offset ~29px, v offset ~38px).
- Mechanical 50/50 panels are complete (no bleed of face into inline). No third billed gen.

### How the agent recovered this run
- Kept mechanical split PASS. Wrote incident as directed after the one allowed redo.

### Durable fix needed before next run
- First-try prompt must lock thin white gutters exactly on 1024/576 and keep all panel content inside its quadrant so auto gutter can accept.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_cover_quad_split.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260823-1332-cover-gutter-mechanical-b06
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B06
article_dir: memory/blog/articles/B06-chto-govorit-chislo-sudby-o-nem-v-otnosheniyah
severity: low
category: prompt

### What went wrong
- First billed 2K i2i for B06: Victoria FACE LARGE left, terracotta cardigan worn (not still-life, not B05 dusty-blue linen). Split still chose mechanical_center: auto gutter `gutter_too_far_from_center` (h offset ~24.5px, v offset ~38.5px). Same class as INC-20260823-0637.
- Mechanical 50/50 panels complete; face did not bleed into inline. Director-allowed full redo not used.

### How the agent recovered this run
- Kept mechanical split PASS. Pillow credit on cover only. No second billed gen.

### Durable fix needed before next run
- Same as INC-20260823-0637: first-try prompt must lock thin white gutters exactly on 1024/576 so auto gutter can accept.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_cover_quad_split.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260823-1654-cover-gutter-bleed-b07
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B07
article_dir: memory/blog/articles/B07-karta-dnya-napishet-li-on-segodnya-vecherom
severity: high
category: prompt


### What went wrong
- First billed 2K i2i: canvas 2688x1520 (not 2048x1152). Auto gutter `gutter_too_far_from_center` (h offset ~74px, v offset ~39.5px). Split fell back to mechanical_center.
- Mechanical 50/50 cut above the painted horizontal gutter: Victoria arms + tiny phone from the cover bled into the top of inline_2. Inline then has a person — cell is not a clean 2x2.

### How the agent recovered this run
- Owner-directed full-canvas redo: one new billed gen on the same batch (not a single-panel patch, not a face beauty-redo). Redo canvas is 2048x1152.
- Auto still rejected gutter (`gutter_too_far_from_center`, h offset ~57px). Mechanical 50/50 again bled the cover host into inline_2.
- No third billed gen. Forced `--split-mode gutter` on the redo canvas so panels follow the painted seams; inline_2 then has no person. Pillow credit on cover.png only.

### Durable fix needed before next run
- First-try prompt must lock thin white gutters exactly on canvas center and keep all cover content inside the top-left quadrant so auto gutter can accept and mechanical 50/50 cannot slice the host into inline.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_cover_quad_split.py`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260824-0635-cover-prompt-budget-b08
status: open
run_date: 2026-08-24
role: excalibur-blog-cover
topic_id: B08
article_dir: memory/blog/articles/B08-chto-on-reshil-za-vyhodnye-i-vernetsya-li-v-dialog
severity: medium
category: prompt

### What went wrong
- Cover scene_hints were already short (cover 134, inline 134–141) but `--write-batch` still failed at 3527/3500.
- Shared headline lock still carried SaaS leftover phrases (`«время»` / traffic, `TOKEN BURN RATE`) that ate the last ~40 chars.

### How the agent recovered this run
- Reclaimed those leftover phrases in `scripts/excalibur_blog_cover_quad_prompt.py` (tenant-neutral: do not rewrite hook; forbid extra English headlines).
- Batch rebuilt at 3475/3500; `jobs.length=1`; git-safe `{{SITE_BASE}}` + `prefer_local_reference` to `memory/cover/assets/виктория.png`.
- Did not empty scene_hints and did not start Kie until budget PASS.

### Durable fix needed before next run
- Keep SaaS-specific example strings out of the shared cover prompt lock so tenant scene_hints (~80–140 / ~100–220) fit under 3500.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`

### Secrets
- none recorded

### Fixer resolution
- pending
