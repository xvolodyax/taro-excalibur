# Pipeline fix queue

Durable incident memory for Excalibur BLOG. Agents append; Fixer resolves.

## INC-20260901-1405-publish-false-409-example-b31
status: open
run_date: 2026-09-01
role: excalibur-blog-publish
topic_id: B31
article_dir: memory/blog/articles/B31-on-otkladyvaet-otnosheniya-na-osen
severity: high
category: env

### What went wrong
- After GATE PASS Director uploaded with `SITE_PUBLISH_TOKEN`: upload 201 `article_id=41`.
- Approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» while H2 «Практика: чеклист шагов…» and a September chat scene are already in the body.
- SITE token GET/POST quality-pass and PATCH status → 403. skip_quality_review / force ignored.
- Live GET 404. Same checker as B27 INC-0650 / B29 INC-2035 / B30 INC-0700.
- Hall prompt said site is upload-only and has no example gate. Checker still lives outside this repo.

### How the agent recovered this run
- Did not rewrite Sol. Did not add «Возьмём:» / «Сцена» / «например» / «кейс» / ярлык «конкретный пример».
- `director_next=false_example_409_no_body_edit`.

### Durable fix needed before next run
- Site quality checker (вне репо) must stop blocking approve on «конкретный пример» when practice H2 + scene exist; or SITE token needs quality-pass.
- Do not treat this 409 as a Writer/Sol rewrite.

### Suggested files to inspect/change
- `shared/excalibur-site-publish-contract.md`
- `scripts/excalibur_blog_site_publish.py`
- site admin quality checker (вне репо)

### Secrets
- none recorded

### Fixer resolution
- pending

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
- Kie `batch_mcp_args` expands `{{SITE_BASE}}` before local upload and errors if `PUBLIC_SITE_URL` is unset. This run exported the tenant public base only in the process env so prefer_local upload could run. Committed batch stayed on placeholders.

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
