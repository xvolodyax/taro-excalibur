# Pipeline fix queue

Durable incident memory. Do not put secrets, tokens, or live hosts here.

## INC-20260825-1328-cover-host-prompt-locks
status: open
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B12
article_dir: articles/B12-lichnoe-chislo-goda-etim-letom
severity: high
category: prompt

### What went wrong
- Style prefix still said `GREEN eyes with slight light-brown near pupil` — the B11 brown-iris miss.
- `cover_quad_prompt.py` set `prefer_local_reference` only for situational cat hero, so TARO host batch would skip local `виктория.png`.
- Shared collage/hot-pink locks ate the 3500 budget and painted the wrong accent.

### How the agent recovered this run
- Rewrote style prefix/tail/ban to GREEN iris + faint hazel ring only, NEVER brown eyes.
- Honor `style.prefer_local_reference` + `local_reference` for host mode.
- Tenant accent `#8B3A3A` for highlight; compact TEXT LOCK so hints stay.
- First Kie create never started: `batch_mcp_args` required `PUBLIC_SITE_URL` to expand `{{SITE_BASE}}` even when `prefer_local_reference` would replace `input_urls` via File Upload. Skip expand when local ref is set.

### Durable fix needed before next run
- Host-mode batch must always upload `виктория.png` via prefer_local_reference.
- Never write `light-brown eyes` / `brown near the pupil` into a Kie prompt.

### Suggested files to inspect/change
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `memory/cover/quad-style-taro-seichas.json`

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260825-1658-cover-early-cta-h2-credit-cli
status: fixed
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B13
article_dir: articles/B13-chto-govorit-karta-dnya-esli-on-zovet-segodnya-vecherom
severity: medium
category: script

### What went wrong
- `excalibur_blog_quad_manifest.py` wired inline_1 to the early CTA H2 «Сразу к делу» (first H2 in article.html). B13 canon skips that heading and the final CTA; inline anchors are the three mid-article H2s.
- Director/Cover runbook called `excalibur_blog_host_credit_overlay.py --article-dir …`, but the script only accepts `--image`.

### How the agent recovered this run
- After `--merge`, remapped `h2_anchor` + visual_type to the three mid H2s and kept Cover-text labels on those slots.
- Stamped credit with `--image cover/cover.png --host Виктория --slot cover`. Exact line: Виктория - таролог команды «ТАРО СЕЙЧАС».

### Durable fix needed before next run
- Manifest should skip early-act heading «Сразу к делу» and the closer CTA H2 when picking inline anchors.
- Credit CLI should accept `--article-dir` (default image `cover/cover.png`) or the runbook must say `--image`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_quad_manifest.py`
- `scripts/excalibur_blog_host_credit_overlay.py`
- `.cursor/skills/cover-excalibur-blog/SKILL.md`

### Secrets
- none recorded

### Fixer resolution
- pending
