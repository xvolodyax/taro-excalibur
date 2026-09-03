# Pipeline fix queue

Durable incident memory for Excalibur BLOG. Agents append; Fixer resolves.

## INC-20260903-0707-metrika-credentials-b36
status: needs-human
run_date: 2026-09-03
role: excalibur-blog-content-learner
topic_id: B36
article_dir: memory/blog/articles/B36-on-sidit-ryadom-i-molchit
severity: blocker
category: credentials

### What went wrong
- Тот же Cloud Secrets gap, что INC-20260902-2016-metrika-credentials-b35 (B26–B35). Секреты Metrika не в Cloud.

### How the agent recovered this run
- Цифры не invent. Тело B36 / Sol не трогали. Слот PUBLISHED `article_id=48`, live 200.

### Durable fix needed before next run
- Cloud Secrets (не git): `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID`. Затем тот же fetch `--days 30 --ingest`.

### Suggested files to inspect/change
- Cloud Secrets / environment (вне репо)
- `shared/yandex-metrika-contract.md`

### Secrets
- none recorded

### Fixer resolution
status: needs-human
fixed_at: 2026-09-03
reason:
- Секреты вне репо. Не invent. Не чинили setup заново (пустой origin/main → restore B35 ожидаем).
needed_decision_or_secret:
- Положить Metrika OAuth + counter id в Cloud Secrets.
files_changed: none (этот INC — указатель на тот же gap)
checks_run:
- queue: B26–B35 metrika → needs-human; не десятый полный дубль
commit: 02c3043

## INC-20260902-2016-metrika-credentials-b35
status: needs-human
run_date: 2026-09-02
role: excalibur-blog-content-learner
topic_id: B35
article_dir: memory/blog/articles/B35-on-predlagaet-druzhbu-posle-rasstavaniya
severity: blocker
category: credentials

### What went wrong
- Content-learner обязателен `python3 scripts/excalibur_blog_metrika_fetch.py --days 30 --ingest`.
- Exit 2: `METRIKA CREDENTIALS BLOCKER`.
- В env нет `YANDEX_METRIKA_OAUTH_TOKEN` и `YANDEX_METRIKA_COUNTER_ID`.
- Нет `memory/site.env.local` и `.env`. `.cursor/environment.json` секреты Metrika не задаёт.
- `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывались.
- Тот же корневой gap, что INC-20260902-1455-metrika-credentials-b34, INC-20260902-0650-metrika-credentials-b33, INC-20260901-1945-metrika-credentials-b32, INC-20260901-1431-metrika-credentials-b31, INC-20260901-0659-metrika-credentials-b30, INC-20260831-2040-metrika-credentials-b29, INC-20260831-1526-metrika-credentials-b28, INC-20260831-0709-metrika-credentials-b27 и INC-20260830-1936-metrika-credentials-b26 (все open). Известный gap: секреты не в Cloud.

### How the agent recovered this run
- Evidence gate SKIP (нет `content-evidence-report.json`) — не BLOCK, report не invent'ился.
- Lesson `LESSON-20260902-2016-B35-evening-offers-friendship` записан как low-confidence (process + SKIP), без causal Metrika.
- Durable apply нет. `article.html` и Writer/Sol prompt не трогали.
- Пайплайн не FAIL: Metrika BLOCKER зафиксирован; слот B35 `PUBLISHED` + live 200 + `article_id=47`. Тело не правили.

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
status: needs-human
fixed_at: 2026-09-03
reason:
- Тот же Cloud Secrets gap. B36 Fixer: не invent; указатель INC-20260903-0707.
needed_decision_or_secret:
- `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` в Cloud Secrets.
files_changed: none
checks_run:
- B36 pointer added; older metrika left needs-human
commit: n/a

## INC-20260902-1455-metrika-credentials-b34
status: needs-human
run_date: 2026-09-02
role: excalibur-blog-content-learner
topic_id: B34
article_dir: memory/blog/articles/B34-ego-chislo-mesyaca-ne-delaet-shag
severity: blocker
category: credentials

### What went wrong
- Content-learner обязателен `python3 scripts/excalibur_blog_metrika_fetch.py --days 30 --ingest`.
- Exit 2: `METRIKA CREDENTIALS BLOCKER`.
- В env нет `YANDEX_METRIKA_OAUTH_TOKEN` и `YANDEX_METRIKA_COUNTER_ID`.
- Нет `memory/site.env.local` и `.env`. `.cursor/environment.json` секреты Metrika не задаёт.
- `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывались.
- Тот же корневой gap, что INC-20260902-0650-metrika-credentials-b33, INC-20260901-1945-metrika-credentials-b32, INC-20260901-1431-metrika-credentials-b31, INC-20260901-0659-metrika-credentials-b30, INC-20260831-2040-metrika-credentials-b29, INC-20260831-1526-metrika-credentials-b28, INC-20260831-0709-metrika-credentials-b27 и INC-20260830-1936-metrika-credentials-b26 (все open). Известный gap: секреты не в Cloud.

### How the agent recovered this run
- Evidence gate SKIP (нет `content-evidence-report.json`) — не BLOCK, report не invent'ился.
- Lesson `LESSON-20260902-1455-B34-month-number-no-step` записан как low-confidence (process + SKIP), без causal Metrika.
- Durable apply нет. `article.html` и Writer/Sol prompt не трогали.
- Пайплайн не FAIL: Metrika BLOCKER зафиксирован; слот B34 `PUBLISHED` + live 200 + `article_id=45`. Тело не правили.

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
status: needs-human
fixed_at: 2026-09-03
reason:
- Тот же Cloud Secrets gap (B26–B36). B36 Fixer: не invent.
needed_decision_or_secret:
- `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` в Cloud Secrets.
files_changed: none
commit: n/a

## INC-20260902-0650-metrika-credentials-b33
status: needs-human
run_date: 2026-09-02
role: excalibur-blog-content-learner
topic_id: B33
article_dir: memory/blog/articles/B33-on-pishet-kazhdyj-den-no-ne-zovet
severity: blocker
category: credentials

### What went wrong
- Content-learner обязателен `python3 scripts/excalibur_blog_metrika_fetch.py --days 30 --ingest`.
- Exit 2: `METRIKA CREDENTIALS BLOCKER`.
- В env нет `YANDEX_METRIKA_OAUTH_TOKEN` и `YANDEX_METRIKA_COUNTER_ID`.
- Нет `memory/site.env.local` и `.env`. `.cursor/environment.json` секреты Metrika не задаёт.
- `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывались.
- Тот же корневой gap, что INC-20260901-1945-metrika-credentials-b32, INC-20260901-1431-metrika-credentials-b31, INC-20260901-0659-metrika-credentials-b30, INC-20260831-2040-metrika-credentials-b29, INC-20260831-1526-metrika-credentials-b28, INC-20260831-0709-metrika-credentials-b27 и INC-20260830-1936-metrika-credentials-b26 (все open).

### How the agent recovered this run
- Evidence gate SKIP (нет `content-evidence-report.json`) — не BLOCK, report не invent'ился.
- Lesson `LESSON-20260902-0650-B33-morning-writes-daily-no-invite` записан как low-confidence (process + SKIP), без causal Metrika.
- Durable apply нет. `article.html` и Writer/Sol prompt не трогали.
- Пайплайн не FAIL: Metrika BLOCKER зафиксирован; слот B33 `approved` + publish 500 directory EACCES + live 404 (`director_next=needs_human_publish_dir_eacces`). Тело не правили. INC-0645 already fixed в скрипте.

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
status: needs-human
fixed_at: 2026-09-03
reason:
- Тот же Cloud Secrets gap. B36 Fixer: не invent.
needed_decision_or_secret:
- `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` в Cloud Secrets.
files_changed: none
commit: n/a

## INC-20260902-0645-publish-dir-eacces-b33
status: fixed
run_date: 2026-09-02
role: excalibur-blog-publish
topic_id: B33
article_dir: memory/blog/articles/B33-on-pishet-kazhdyj-den-no-ne-zovet
severity: blocker
category: site-permissions

### What went wrong
- GATE PASS. `SITE_PUBLISH_TOKEN` сам: upload 201 `article_id=43`, first approve **200**, `quality_score=100`, warnings пустые.
- `POST …/publish` → 500: «Не удалось создать каталог публикации» (EACCES). Каталог slug на диске сайта не создан.
- Live GET 404. Это не sitemap EACCES (контракт B23: sitemap + live 200 = live_ok).
- Resume `--resume-article-id 43`: API всё ещё `status=approved`; повторный approve 409 «проверка качества» — не example-gate; publish снова 500 тот же EACCES.
- Тело / Sol не трогали. «Возьмём:» не писали. Hall / Дзен Студия не звали.

### How the agent recovered this run
- Зафиксировано в `site-publish-result.json` + site-publish-log. Ledger `approved_eacces`.
- `director_next=needs_human_publish_dir_eacces`. Пайплайн не invent live URL.

### Durable fix needed before next run
- На сервере: права www на каталог блога (создавать slug). Это вне репо.
- Скрипт: publish 500 directory EACCES → `publish_dir_eacces=true`, не путать с sitemap skip; resume не слать approve, если API уже `approved`.
- Не учить Writer/Sol лечить EACCES текстом.

### Suggested files to inspect/change
- `scripts/excalibur_blog_site_publish.py`
- `shared/excalibur-site-publish-contract.md`
- `tests/test_site_publish.py`

### Secrets
- none recorded

### Fixer resolution
status: fixed
fixed_at: 2026-09-02
fix_summary:
- Publish 500 «каталог публикации» / directory EACCES → `publish_dir_eacces=true`.
- sitemap + live 200 = `live_ok`; directory EACCES + live 404 = `verdict=needs_human` (`director_next=needs_human_publish_dir_eacces`). Не invent live URL.
- Resume: GET статьи; если API `status=approved` — не POST approve (`approve_skipped=already_approved`).
- Контракт: directory EACCES ≠ sitemap EACCES; не лечить телом / «Возьмём:».
- Тело B33 / Writer / Sol skill не трогали. Старые Metrika INC не чинили (секретов нет).
- Права www на каталог блога по-прежнему вне репо.
files_changed:
- `scripts/excalibur_blog_site_publish.py`
- `shared/excalibur-site-publish-contract.md`
- `tests/test_site_publish.py`
- `memory/pipeline-fix-queue.md`
checks_run:
- `python3 -m py_compile scripts/excalibur_blog_site_publish.py tests/test_site_publish.py`
- `test_publish_dir_eacces_live_404_needs_human` ok
- `test_resume_already_approved_skips_approve` ok
- `test_publish_sitemap_eacces_still_live` ok (не путает с dir EACCES)
- `test_dir_eacces_detector_not_sitemap` ok
commit: cbab9ae

## INC-20260901-1945-metrika-credentials-b32
status: needs-human
run_date: 2026-09-01
role: excalibur-blog-content-learner
topic_id: B32
article_dir: memory/blog/articles/B32-on-pishet-tolko-nochyu-dnem-molchit
severity: blocker
category: credentials

### What went wrong
- Content-learner обязателен `python3 scripts/excalibur_blog_metrika_fetch.py --days 30 --ingest`.
- Exit 2: `METRIKA CREDENTIALS BLOCKER`.
- В env нет `YANDEX_METRIKA_OAUTH_TOKEN` и `YANDEX_METRIKA_COUNTER_ID`.
- Нет `memory/site.env.local` и `.env`. `.cursor/environment.json` секреты Metrika не задаёт.
- `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывались.
- Тот же корневой gap, что INC-20260901-1431-metrika-credentials-b31, INC-20260901-0659-metrika-credentials-b30, INC-20260831-2040-metrika-credentials-b29, INC-20260831-1526-metrika-credentials-b28, INC-20260831-0709-metrika-credentials-b27 и INC-20260830-1936-metrika-credentials-b26 (все open).

### How the agent recovered this run
- Evidence gate SKIP (нет `content-evidence-report.json`) — не BLOCK, report не invent'ился.
- Lesson `LESSON-20260901-1945-B32-evening-night-only-chat` записан как low-confidence (process + SKIP), без causal Metrika.
- Durable apply нет. `article.html` и Writer/Sol prompt не трогали.
- Пайплайн не FAIL: Metrika BLOCKER зафиксирован; слот B32 в `quality_review` (upload 201 `article_id=42`, approve 409, live 404). Тело не правили.

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
status: needs-human
fixed_at: 2026-09-03
reason:
- Тот же Cloud Secrets gap. B36 Fixer: не invent.
needed_decision_or_secret:
- `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` в Cloud Secrets.
files_changed: none
commit: n/a

## INC-20260901-1945-scout-suggest-next-ignores-titles
status: fixed
run_date: 2026-09-01
role: excalibur-blog-scout
topic_id: B32
article_dir: n/a
severity: medium
category: script

### What went wrong
- `scout_helper --suggest-next` читал только строки `| 20` из `published-articles.md`.
- Текущий ledger без дат → reserved пустой (если нет article dirs) → next `B01`, хотя `shared/published-titles.md` уже до B31/B32.

### How the agent recovered this run
- Director передал Fixer; Scout не стартовал заново.

### Durable fix needed before next run
- `--suggest-next` должен смотреть колонку `topic_id` (`B\d+`) в `shared/published-titles.md`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_scout_helper.py`

### Secrets
- none recorded

### Fixer resolution
status: fixed
fixed_at: 2026-09-01
fix_summary:
- `load_published_title_topic_ids` + `load_reserved_topic_ids` + `next_b_topic_id`.
- `--suggest-next` на этом репо → `B33` (titles до B32).
- Тело B32 / Sol не трогали.
files_changed:
- `scripts/excalibur_blog_scout_helper.py`
- `tests/test_scout_helper_query_slug_cover.py`
- `skills/scout-excalibur-blog/SKILL.md`
- `.cursor/skills/scout-excalibur-blog/SKILL.md`
- `agents/excalibur-blog-scout.md`
- `.cursor/agents/excalibur-blog-scout.md`
checks_run:
- `python3 -m unittest tests.test_scout_helper_query_slug_cover` — ok
- `python3 scripts/excalibur_blog_scout_helper.py --suggest-next` → B33
commit: 1a625f9

## INC-20260901-1944-html-linter-allow-h1
status: fixed
run_date: 2026-09-01
role: excalibur-blog-writer
topic_id: B32
article_dir: n/a
severity: low
category: script

### What went wrong
- HTML linter раньше браковал `<h1>` как forbidden tag. В этом прогоне `h1` уже в `ALLOWED_TAGS`.

### How the agent recovered this run
- Confirm + regression test, без правки прозы B32.

### Durable fix needed before next run
- Держать `h1` в whitelist; тест, что `<h1>` не FAIL.

### Suggested files to inspect/change
- `scripts/excalibur_blog_html_linter.py`
- `tests/test_html_linter.py`

### Secrets
- none recorded

### Fixer resolution
status: fixed
fixed_at: 2026-09-01
fix_summary:
- `ALLOWED_TAGS` уже содержит `h1` (этот прогон). Добавлен `tests/test_html_linter.py`.
- Тело B32 не трогали.
files_changed:
- `tests/test_html_linter.py`
checks_run:
- `python3 -m unittest tests.test_html_linter` — 3/3 ok
commit: 1a625f9

## INC-20260901-1943-research-start-wipe-published-titles
status: fixed
run_date: 2026-09-01
role: excalibur-blog-research
topic_id: B32
article_dir: n/a
severity: high
category: script

### What went wrong
- `write_titles` читал только строки `| 20` из `published-articles.md`.
- Ledger без дат → `build_titles=[]` → `shared/published-titles.md` перезаписывался пустой таблицей.

### How the agent recovered this run
- titles на диске ещё держали B12–B32; Fixer сделал durable preserve/merge.

### Durable fix needed before next run
- Не затирать существующие строки titles, если ledger без дат. Merge, не wipe.

### Suggested files to inspect/change
- `scripts/excalibur_blog_published_titles.py`
- `scripts/excalibur_blog_research_start.py`

### Secrets
- none recorded

### Fixer resolution
status: fixed
fixed_at: 2026-09-01
fix_summary:
- `load_existing_title_rows` + `merge_title_rows`: пустой/без дат ledger не стирает titles.
- Dateless `| Bxx |` строки ledger тоже читаются; статусы `live` / `quality_review` в allowed.
- Smoke: existing=39, built=7, merged=39 (B12–B32 + LIVE сохранены).
files_changed:
- `scripts/excalibur_blog_published_titles.py`
- `tests/test_writer_editorial_contracts.py`
checks_run:
- `test_write_titles_keeps_existing_when_ledger_has_no_dates` ok
- `test_write_titles_does_not_wipe_to_empty_header` ok
commit: 1a625f9

## INC-20260901-1939-publish-false-409-example-b32
status: needs-human
run_date: 2026-09-01
role: excalibur-blog-publish
topic_id: B32
article_dir: memory/blog/articles/B32-on-pishet-tolko-nochyu-dnem-molchit
severity: high
category: env

### What went wrong
- After GATE PASS upload with `SITE_PUBLISH_TOKEN`: 201 `article_id=42`.
- Approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» while H2 «Как изменить сценарий без драмы и выяснения отношений» (чеклист шагов) and a night-chat scene are already in the body.
- SITE token GET quality → 403. skip_quality_review / force ignored.
- Live GET 404 both `/blog/{slug}/` and `/{slug}/`. Same checker as B27 INC-0650 / B29 INC-2035 / B30 INC-0700 / B31 INC-1405.
- Script `article_has_practice_h2` looked only for «практик»/«чеклист» in H2 and set `director_next=return_sol_practice` + `practice_h2_present=false`. That would wrongly send Sol.

### How the agent recovered this run
- Did not rewrite Sol. Did not add «Возьмём:» / «Сцена» / «например» / «кейс» / ярлык «конкретный пример».
- Did not invent a live permalink. `live_ok=false`.
- Overrode `director_next=false_example_409_no_body_edit` and `practice_h2_present=true` in `site-publish-result.json`.
- Slot 21:21 not closed. B21/B22 not touched. Dzen Studio / Hall not used.

### Durable fix needed before next run
- Site quality checker (вне репо) must stop blocking approve on «конкретный пример» when practice H2 + scene exist; or SITE token needs quality-pass.
- Script detector must treat H2 «Как изменить сценарий…» (and similar practice titles without the words «практика»/«чеклист») as practice already present.
- Do not treat this 409 as a Writer/Sol rewrite.

### Suggested files to inspect/change
- `scripts/excalibur_blog_site_publish.py` (`article_has_practice_h2`)
- `shared/excalibur-site-publish-contract.md`
- site admin quality checker (вне репо)

### Secrets
- none recorded

### Fixer resolution
status: needs-human
fixed_at: 2026-09-01
reason:
- Durable approve fix is the site quality checker (вне репо). Same false gate as B27/B29/B30/B31.
- Repo detector (этот Fixer): `article_has_practice_h2` считает «Как изменить сценарий…» / «проверк» / «шаг» практикой. Не «починили сайт».
- В репо нет гейта «конкретный пример». Не лечить телом, не «Возьмём:».
needed_decision_or_secret:
- Site admin: перестать блокировать approve по «конкретный пример», когда practice H2 + сцена уже есть; или выдать SITE token quality-pass.
- Не помечать «починили сайт». Тело B32 / Sol не трогать.
repo_fix:
- `article_has_practice_h2` + `PRACTICE_H2_MARKERS` (практик, чеклист, сценарий, проверк, шаг)
- контракт: H2 «Как изменить сценарий…» = практика уже в теле
- тесты: markers + quality 409 scenario H2 → `false_example_409_no_body_edit`
files_changed:
- `scripts/excalibur_blog_site_publish.py`
- `shared/excalibur-site-publish-contract.md`
- `tests/test_site_publish.py`
checks_run:
- `test_practice_h2_markers_include_scenario_check_step` ok
- `test_first_upload_quality_409_scenario_h2_no_body_edit` ok
- upload 201 / approve 409 / live 404 / quality GET 403 / article GET score 88 (этот прогон, сайт)
commit: 1a625f9 (repo detector); site 409 still needs-human

## INC-20260901-1431-metrika-credentials-b31
status: needs-human
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
status: needs-human
fixed_at: 2026-09-03
reason:
- Тот же Cloud Secrets gap. B36 Fixer: не invent.
needed_decision_or_secret:
- `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` в Cloud Secrets.
files_changed: none
commit: n/a

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
commit: 21afd83

## INC-20260902-1428-cover-kie-result-download
status: needs-human
run_date: 2026-09-02
role: excalibur-blog-cover
topic_id: B34
article_dir: memory/blog/articles/B34-ego-chislo-mesyaca-ne-delaet-shag
severity: medium
category: script

### What went wrong
- Kie createTask #1 succeeded (`task_id` in `cover/kie-image-task.json`, `state=success`).
- `excalibur_blog_quad_apply.py` hung >10 min on `download_url_bytes` with no progress log; PID killed. Not a Kie recreate.
- Full GET / HTTP/2 of the Kie result CDN stalled at ~1.25 MiB of ~2.4 MiB (truncated PNG).
- 256 KiB Range reads timed out after offset 1.25 MiB; 16–8 KiB ranges later stalled; 2 KiB ranges completed.

### How the agent recovered this run
- Same billed Kie URL. No second createTask.
- Resume Range download (2–4 KiB chunks, timeout per range) → full `cover/canvas-quad.png` 2048×1152.
- Then `excalibur_blog_cover_quad_split.py --inject-html` PASS: 3 `figure.inline-quad`, 0 `figure.cover-hero`.

### Durable fix needed before next run
- `asset_download.download_url_bytes` / `quad_apply`: print progress; shrink Range size on timeout; resume partial file; fail fast instead of silent hang.
- Do not treat result-CDN stall as Kie recreate / quality-redo.

### Suggested files to inspect/change
- `scripts/asset_download.py`
- `scripts/excalibur_blog_quad_apply.py`

### Secrets
- none recorded

### Fixer resolution
status: needs-human
fixed_at: 2026-09-03
reason:
- Repo mitigation (Range-resume / progress) уже в дереве (commit 6f812de). CDN hang не воспроизведён на B35/B36 — это не «починили».
- B36 Cover: 1 Kie i2i `Виктория.png`, `create_attempts=1`, `state=success`, глаза green-hazel, 3 inline, cover-hero в теле нет. Quality-redo не делали (белый блейзер на обложке — не lock, не второй billed).
needed_decision_or_secret:
- Если hang вернётся: тот же billed URL + Range-resume, не второй createTask.
files_changed: none (этот прогон)
checks_run:
- B36 `kie-image-task.json`: create_attempts=1 success; не quality-redo
commit: n/a (mitigation already 6f812de)

## INC-20260902-2121-director-gemini-task-catalog-missing
status: needs-human
run_date: 2026-09-02
role: excalibur-blog-director
topic_id: B35
article_dir: memory/blog/articles/B35-on-predlagaet-druzhbu-posle-rasstavaniya
severity: medium
category: env

### What went wrong
- Gemini 3.7 Flash (`gemini-3.7-flash-high`) нет в каталоге Task этого runtime.
- Текстовые шаги B35 и B36 шли `inherit` automation. Это gap каталога, не сбой статьи.

### How the agent recovered this run
- Director не подставлял другой model id. Policy `text_model` не меняли.

### Durable fix needed before next run
- Человек: добавить Gemini 3.7 Flash в Task-каталог runtime **или** явно сменить pin.
- До решения: если slug нет в каталоге — inherit automation. Не угадывать `gpt-*` / `gemini-2.*` / flash-lite.

### Suggested files to inspect/change
- `shared/pipeline-model-policy.json` (pin не менять без человека)
- `shared/subagent-chain.md`
- `agents/excalibur-blog-director.md`
- Cloud / Task catalog (вне репо)

### Secrets
- none recorded

### Fixer resolution
status: needs-human
fixed_at: 2026-09-02
reason:
- Каталог Task — env. Репо только фиксирует fallback inherit и запрет угадывать модель.
- B36: тот же catalog miss; текст снова inherit. Новый INC не плодили.
- Канон директора уже содержит фразу catalog miss → inherit. B36 Fixer добавил `_comment` в policy.
needed_decision_or_secret:
- Добавить `gemini-3.7-flash-high` в каталог Task этого runtime или явно сменить `text_model`.
repo_fix:
- `catalog_missing_fallback=inherit`, `catalog_missing_do_not_guess_model=true`
- `_comment`: catalog miss → inherit
- Director / chain / docs: inherit, не другой slug
files_changed:
- `shared/pipeline-model-policy.json`
- `shared/subagent-chain.md`
- `docs/cursor/models.md`
- `agents/excalibur-blog-director.md`
- `skills/director-excalibur-blog/SKILL.md`
- `.cursor/agents/excalibur-blog-director.md`
- `.cursor/skills/director-excalibur-blog/SKILL.md`
- `tests/test_subagent_chain_and_models.py`
- `memory/pipeline-fix-queue.md`
checks_run:
- `python3 -m json.tool shared/pipeline-model-policy.json`
- `python3 -m unittest tests.test_subagent_chain_and_models tests.test_writer_sol_pipeline`
- rg: catalog_missing_fallback=inherit; text_model still gemini-3.7-flash-high
commit: 3ae045f

## INC-20260902-2121-html-linter-div-strong-unwrap-b35
status: fixed
run_date: 2026-09-02
role: excalibur-blog-sol
topic_id: B35
article_dir: memory/blog/articles/B35-on-predlagaet-druzhbu-posle-rasstavaniya
severity: low
category: qa

### What went wrong
- html_linter сначала FAIL: forbidden `<div>` / `<strong>` (CTA-обёртка), как B34.
- Sol unwrap. Тело после unwrap без этих тегов.

### How the agent recovered this run
- Sol unwrap, не расширение whitelist. Writer/Sol skill не раздували.

### Durable fix needed before next run
- Не добавлять `div` / `strong` в `ALLOWED_TAGS` ради CTA.
- FAIL → верни Sol unwrap. CTA остаётся `p` / `b` / `a`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_html_linter.py`
- `tests/test_html_linter.py`
- `agents/excalibur-blog-director.md`
- `skills/director-excalibur-blog/SKILL.md`

### Secrets
- none recorded

### Fixer resolution
status: fixed
fixed_at: 2026-09-02
fix_summary:
- Whitelist не расширяли. Комментарий в linter + тест, что `div`/`strong` остаются forbidden.
- Director: FAIL на CTA-div → Sol unwrap, как B34/B35.
- Тело B35 `article.html` этот Fixer не трогал.
files_changed:
- `scripts/excalibur_blog_html_linter.py`
- `tests/test_html_linter.py`
- `agents/excalibur-blog-director.md`
- `skills/director-excalibur-blog/SKILL.md`
- `.cursor/agents/excalibur-blog-director.md`
- `.cursor/skills/director-excalibur-blog/SKILL.md`
- `memory/pipeline-fix-queue.md`
checks_run:
- `python3 -m unittest tests.test_html_linter` — 3/3 ok
- `python3 scripts/excalibur_blog_html_linter.py` B35 article.html → PASS (unwrap already in tree; Fixer did not edit body)
- rg: div/strong not in ALLOWED_TAGS; Director unwrap note
commit: 3ae045f

