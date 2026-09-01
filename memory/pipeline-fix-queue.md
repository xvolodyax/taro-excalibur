# Pipeline fix queue

Durable incident memory for Excalibur BLOG. Agents append; Fixer resolves.

## INC-20260901-1431-metrika-credentials-b31
status: open
run_date: 2026-09-01
role: excalibur-blog-content-learner
topic_id: B31
article_dir: memory/blog/articles/B31-on-otkladyvaet-otnosheniya-na-osen
severity: blocker
category: credentials

### What went wrong
- Content-learner обязателен `python3 scripts/excalibur_blog_metrika_fetch.py --days 30 --ingest`.
- Exit 2: `METRIKA CREDENTIALS BLOCKER`.
- В env нет `YANDEX_METRIKA_OAUTH_TOKEN` и `YANDEX_METRIKA_COUNTER_ID`.
- Нет `memory/site.env.local` и `.env`. `.cursor/environment.json` секреты Metrika не задаёт.
- `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывались.
- Тот же корневой gap, что INC-20260901-0659-metrika-credentials-b30, INC-20260831-2040-metrika-credentials-b29, INC-20260831-1526-metrika-credentials-b28, INC-20260831-0709-metrika-credentials-b27 и INC-20260830-1936-metrika-credentials-b26 (все open).

### How the agent recovered this run
- Evidence gate SKIP (нет `content-evidence-report.json`) — не BLOCK, report не invent'ился.
- Lesson `LESSON-20260901-1431-B31-day-autumn-deadline` записан как low-confidence (process + SKIP), без causal Metrika.
- Durable apply нет. `article.html` и Writer/Sol prompt не трогали.
- Пайплайн не FAIL: Metrika BLOCKER зафиксирован; слот B31 в `quality_review` (upload 201 `article_id=41`, approve 409, live 404). Тело не правили.

### Durable fix needed before next run
- Положить в Cloud Secrets (не в git): `YANDEX_METRIKA_OAUTH_TOKEN` (OAuth, `metrika:read`) и `YANDEX_METRIKA_COUNTER_ID`.
- Документация: `shared/yandex-metrika-contract.md`, имена в `.env.example`.
- После секретов: тот же fetch `--days 30 --ingest`; не invent rows.

### Suggested files to inspect/change
- `shared/yandex-metrika-contract.md`
- `.env.example`
- Cloud Secrets / environment (вне репо)

### Secrets
- none recorded

### Fixer resolution
- pending

## INC-20260901-1405-publish-false-409-example-b31
status: needs-human
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
status: needs-human
fixed_at: 2026-09-01
reason:
- Durable fix is the site quality checker (вне репо). Approve 409 «Нет конкретного примера или разбора ситуации» при H2 практике + сцене в теле — тот же ложный гейт, что B27/B29/B30.
- В репо нет гейта «конкретный пример». `shared/excalibur-site-publish-contract.md` уже говорит: не лечить телом, не «Возьмём:», `director_next=false_example_409_no_body_edit`.
- SITE token GET quality / force-approve → 403. Это не обход 409.
needed_decision_or_secret:
- Site admin: перестать блокировать approve по «конкретный пример», когда practice H2 + сцена уже есть; или выдать SITE token quality-pass.
- Не помечать «починили сайт». Тело B31 / Sol не трогать.
files_changed: none
checks_run:
- queue + publish-contract re-read; no repo patch
commit: n/a

## INC-20260901-1350-cover-tenant-style-local-ref
status: fixed
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
status: fixed
fixed_at: 2026-09-01
fix_summary:
- `quad_manifest.py` берёт `style_file` / `style_id` из `tenant-config.cover_files.style_preset`; пустой preset → прежний pink-cat fallback.
- `cover_quad_prompt.py`: `prefer_local_reference` + `local_reference` из style (host_reference / Виктория.png), не только situational cat; highlight/sticky/typeface из cover-design-code (золото #C4A574, editorial); пустой design-code → hot-pink / bold condensed.
- `kie_gpt_image2_api.batch_mcp_args` не разворачивает `{{SITE_BASE}}`, если batch `prefer_local_reference` (upload локального файла дальше).
- Статья B31 / `article.html` / слог не трогались.
files_changed:
- `scripts/excalibur_blog_quad_manifest.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_cover_identity_gate.py`
- `tests/test_quad_manifest.py`
- `tests/test_cover_identity.py`
- `memory/pipeline-fix-queue.md`
checks_run:
- `python3 -m py_compile` quad_manifest + cover_quad_prompt + kie + identity_gate
- `python3 -m json.tool` tenant-config + victoria style + cover-design-code
- `python3 -m unittest tests.test_quad_manifest` — 4/4 ok
- `python3 -m unittest tests.test_cover_identity` — tenant/local-ref/gold/hair/kie-prefer-local ok; pre-existing `is_playground_blank_fail` import still missing (не этот INC)
commit: pending-parent-commit
