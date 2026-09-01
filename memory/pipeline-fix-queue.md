# Pipeline fix queue

Durable incident memory for Excalibur BLOG. Agents append; Fixer resolves.

## INC-20260901-1350-cover-tenant-style-local-ref
status: open
run_date: 2026-09-01
role: excalibur-blog-cover
topic_id: B31
article_dir: memory/blog/articles/B31-on-otkladyvaet-otnosheniya-na-osen
severity: medium
category: script

### What went wrong
- `excalibur_blog_quad_manifest.py` always writes `style_file` = pink-cat collage, ignoring `shared/tenant-config.json` `cover_files.style_preset` (`quad-style-victoria-studio.json`).
- `excalibur_blog_cover_quad_prompt.py` sets `prefer_local_reference` only for situational cat hero. Host-reference tenant with `style.prefer_local_reference: true` and local `Виктория.png` got `prefer_local_reference: false`.
- Same prompt script hardcodes highlight `hot-pink #FF1493` and `bold condensed Cyrillic`, which this tenant forbids (gold `#C4A574`, editorial display).

### How the agent recovered this run
- After `--merge`, Cover rewrote `style_file` to `memory/cover/quad-style-victoria-studio.json`.
- After `--write-batch`, Cover patched batch: `prefer_local_reference: true`, `local_reference: memory/cover/assets/Виктория.png`, hair lock phrase, gold/editorial type. Did not raise Kie retries.

### Durable fix needed before next run
- Manifest must take `style_file` from tenant `cover_files.style_preset`.
- Prompt/batch must honor `style.prefer_local_reference` + `style.local_reference` for host_reference (upload `Виктория.png`, never latin aliases).
- Highlight/sticky colors and hook typeface must come from `cover-design-code.json`, not hardcoded pink/bold condensed.

### Suggested files to inspect/change
- `scripts/excalibur_blog_quad_manifest.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `shared/tenant-config.json`
- `memory/cover/quad-style-victoria-studio.json`

### Secrets
- none recorded

### Fixer resolution
- pending
