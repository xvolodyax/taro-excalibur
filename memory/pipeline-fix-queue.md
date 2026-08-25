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
