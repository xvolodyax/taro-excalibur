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
