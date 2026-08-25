# Pipeline fix queue

## INC-20260825-0917-cover-wrong-face-hall
status: fixed
fixed_at: 2026-08-25
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B11
article_dir: articles/B11-on-smotrit-moi-istorii-i-molchit
severity: high
category: identity
fix_summary:
- Permanent host canon: `shared/cover-host-canon.md` + SOUL Visual + blog-hero + cover skill.
- Identity-fail (чужое лицо / брюнетка / шов) = HARD reject, rebuild whole canvas; do not ship.
- Hall no longer redraws article covers. Agent only. Side-by-side ref check + `cover-host-gate`.
files_changed:
- `shared/cover-host-canon.md`
- `shared/SOUL.md`
- `scripts/excalibur_blog_cover_host_gate.py`
- `skills/cover-excalibur-blog/SKILL.md`
checks_run:
- `python3 -m unittest tests.test_cover_host_canon`
commit: pending

### What went wrong
- Rebuild without hard ref check produced a foreign face (brunette, vertical seam) that went to Dzen. Vladimir caught it.

## INC-20260825-0637-cover-host-still-life
status: fixed
fixed_at: 2026-08-25
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B11
article_dir: articles/B11-on-smotrit-moi-istorii-i-molchit
severity: medium
category: prompt
fix_summary:
- scene_hint must say FACE visible LARGE left wearing [outfit]; garment-as-object blocked in write-batch.
- Still-life allowed only as inline. Living canon + gate so the rule cannot vanish.
files_changed:
- `shared/cover-host-canon.md`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `memory/cover/blog-hero.json`
checks_run:
- `python3 -m unittest tests.test_cover_host_canon`
commit: pending

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
- fixed in cover-host-canon + write-batch still-life lock + cover-host-gate

## INC-20260825-0645-cover-kie-500
status: open
run_date: 2026-08-25
role: excalibur-blog-cover
topic_id: B11
article_dir: articles/B11-on-smotrit-moi-istorii-i-molchit
severity: blocker
category: api

### What went wrong
- Owner-directed Hall redo: new FACE-visible batch written (`quad-mcp-batch.json` unchanged after write).
- First createTask `feda9ecd82859254cfba59fdc6642c92` terminal failCode=500 Internal Error.
- Script max-1 recreate `1514a2d546bddeca2df2bef0c1391ae2` also failCode=500. Retries exhausted.
- No new canvas URL. Old still-life `cover.png` remains. Cover did not invent a third createTask.

### How the agent recovered this run
- Stopped with KIE API BLOCKER. Apply/split/credit not re-run.
- Batch left ready for Director same-batch re-run of `excalibur_blog_kie_gpt_image2_api.py` when Kie healthy, then Cover apply-only.

### Durable fix needed before next run
- Same approved 500×2 path: Director same-batch re-run, Cover apply-only. Do not raise Cover retries or switch to MCP.

### Suggested files to inspect/change
- `shared/kie-gpt-image-api-contract.md`
- `articles/B11-on-smotrit-moi-istorii-i-molchit/cover/quad-mcp-batch.json`

### Secrets
- none recorded

### Fixer resolution
- pending
