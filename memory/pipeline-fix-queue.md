# Pipeline fix queue

## INC-20260825-0637-cover-host-still-life
status: open
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B11
article_dir: articles/B11-on-smotrit-moi-istorii-i-molchit
severity: medium
category: prompt

### What went wrong
- First-try 2K i2i (one billed createTask) returned a valid 2048×1152 quad with gutters on center (offset 1.0 / 1.5 px). Split PASS.
- Cover panel painted a still-life of a dusty-olive blouse + muted phone instead of Victoria face from `memory/cover/assets/виктория.png`.
- Cover `scene_hint` was short (125 chars) and named the blouse as a scene object (`dusty-olive blouse` + `tiny muted phone`). Model treated outfit as flat-lay props, not clothing on the host.

### How the agent recovered this run
- No quality-redo (INC-20260724-2120). Gutters were on 1024/576 — canvas redo not triggered.
- Pillow credit stamped on `cover.png`: `Виктория - таролог команды «ТАРО СЕЙЧАС»`.
- Split + three H2 `<figure>` injects kept.

### Durable fix needed before next run
- Cover `scene_hint` must lock a visible face wearing the new outfit: `Victoria FACE visible LARGE left wearing dusty-olive blouse` — never list the garment as a still-life subject.
- Keep topic prop `tiny`/`small` right; do not let outfit + phone become equal-weight still-life.

### Suggested files to inspect/change
- `memory/cover/blog-hero.json` (`prompt_fragment` / `outfit_rule`)
- `scripts/excalibur_blog_cover_quad_prompt.py` (cover TEXT LOCK / scene line)
- `skills/cover-excalibur-blog/SKILL.md`

### Secrets
- none recorded

### Fixer resolution
- pending
