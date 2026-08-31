# Content lessons — ТАРО СЕЙЧАС

Канон: `shared/content-learning-contract.md`.
Исторические scorecard / judge / ensemble — read-only, не шаблон.
Writer prompt и Sol skill сюда не раздувать автоматически.

## LESSON-20260830-1936-B26-evening-practice-h2
status: proposed
topic_id: B26
category: structure
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK.
- process: `site-publish-result.json` + `memory/pipeline-fix-queue.md#INC-20260830-1932-publish-site-quality-409-b26`
  finding: первый upload `article_id=36` v1 → approve 409, quality 76, warning «Нет практического блока (практика / шаги / чеклист)». Позже live: approve 200, sitemap 500 EACCES + live GET 200 = `live_ok`. В финале есть H2 «Практика: чеклист шагов, если он сказал «не готов»».
- process: `cover/quad-mcp-batch.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference`); `cover_png_figures_removed=0` / `cover_hero_removed=0` — cover не в теле; Hall не использовался, SITE token сам.
- process: `research-notes.md` + `title-brief.json`
  finding: вечерний острый запрос «он сказал, что не готов»; не «карта дня»; жирная Wordstat «отношения без обязательств» в H1 не клеить; слот ≠ 21:21.
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). Цифры не выдумывать.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (практика/чеклист; первый upload; later live)

### Keep
- Вечерний острый запрос (фраза уже сказана, он остаётся) — не формат «карта дня».
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file).
- `cover.png` только файл обложки, не вторая картинка в теле.
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.

### Change
- Заранее H2 практика/чеклист из фактов этой статьи (Writer смысл → Sol слог), иначе сайт 409 на первом approve.
- Не ждать возврата Sol после quality 76. Publish тело не переписывает.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена».
- Часы и день B23 («суббота, 20:40») в чужой слот.
- Клеить жирную Wordstat («отношения без обязательств» и шум «играл со мной») в H1.
- Закрывать слот 21:21 (опрос / карта дня) этой статьёй.

### Proposed apply
- Review-only: Director/Sol до первого upload держат H2 практика/чеклист из research/Writer этой статьи.
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически (один кейс + evidence SKIP).
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`), иначе следующий Content-learner снова BLOCKER.

### Durable applied
- 2026-08-30 Fixer INC-1932: Writer/Sol заранее H2 «Практика: чеклист шагов…» из маркеров этой статьи; Publish первый quality 409 → `needs_sol` (не PIPELINE FAIL); практика ≠ «конкретный пример: ЧЧ:ММ»; без «Возьмём:» и без шаблона B23. B25 INC-1423 не закрыт как «починили сайт».

### Resolution
status: recorded

## LESSON-20260831-0709-B27-morning-future-talk
status: proposed
topic_id: B27
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился.
- process: `research-notes.md` + `title-brief.json` + `research-context.json`
  finding: слот утро 2026-08-31 / 09:00 / острый запрос «он не обсуждает будущее»; не карта дня, не нумерология, не вечерний «напишет ли». H1 — наблюдаемый разговор («зовёт на выходные, но избегает разговоров о будущем»), не жирная Wordstat «не видит будущего» / мусор «он не говорит мы».
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + `memory/cover/assets/Виктория.png`); style `victoria-studio`; `cover_png_figures_removed=0` / `cover_hero_removed=0` — cover не в теле. Первый billed gen без хоста (INC-0636); один owner redo → host left. Manifest pink-cat leftover закрыт INC-0640.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=37`; excerpt 403 = не FAIL; publish 500 sitemap EACCES + live GET 200 = `live_ok`; `quality_score=100`, `practice_h2_present=true`, `sol_rewritten=false`.
- process: `memory/pipeline-fix-queue.md#INC-20260831-0650-publish-false-409-example-b27`
  finding: первый approve 409, quality 88, warning «Нет конкретного примера или разбора ситуации» при живой сцене (четверг / суббота / геопозиция отеля / «там посмотрим») и H2 «Практика: чеклист шагов для проверки общего горизонта отношений». Warning «практический блок» не было. Слот вышел после фразы «Разберём этот конкретный пример…» + новый POST (не resume). Это ≠ ярлык «Возьмём:».
- process: LESSON-20260831-0650-B27-scene-in-lead
  finding: Fixer-фрагмент про 409/сцену уже записан; этот блок — полный slot-lesson Content-learner после publish.
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260831-0709-metrika-credentials-b27; B26 INC-1936 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (конкретный пример ≠ «Возьмём:»; первый upload; later live)

### Keep
- Утренний острый запрос «не обсуждает будущее» (контакт и суббота есть, горизонта нет) — не формат «карта дня».
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`.
- `cover.png` только файл обложки, не вторая картинка в теле.
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Живая сцена из research этой статьи в лиде + заранее H2 «Практика: чеклист шагов…».
- Publish тело не правит. Sitemap EACCES + live 200 = `live_ok`.

### Change
- 409 «нет конкретного примера» при уже живой сцене + H2 практике — не лечить ярлыком «Возьмём:» / «например» / «кейс» и не слать Sol на вставку ярлыка (`false_example_409_no_body_edit`).
- Не ждать возврата Sol после quality 88, если практика уже в статье.
- Не помечать B25 INC-1423 / site quality как «починили сайт».

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение 409 example.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Клеить жирную Wordstat («не видит будущего», шум «он не говорит мы») в H1.
- Часы и день B23 («суббота, 20:40») в утренний слот.
- Сливать угол с B26 («сказал, что не готов, но остаётся»).
- Раздувать `shared/writer-master-prompt.md` / Writer skill автоматически (фраза «Разберём этот конкретный пример…» уже в prompt после Fixer 5b88870; новый токен не добавлять).

### Proposed apply
- Review-only: слот утро / острый запрос «не обсуждает будущее» держит сцену+практику из research этой статьи; 409 example ≠ «Возьмём:».
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически (один кейс + evidence SKIP + повтор 409 уже закрыт Fixer INC-0650).
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`), иначе следующий Content-learner снова BLOCKER.

### Durable applied
- none this run. Prior Fixer INC-0650 (commit 5b88870): сцена в лиде + фраза опоры; Publish `false_example_409_no_body_edit`; Writer prompt не трогать повторно. Rollback: вернуть только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

## LESSON-20260831-0650-B27-scene-in-lead
status: recorded
topic_id: B27
category: structure
confidence: medium

### Evidence
- process: INC-20260831-0650 — approve 409 «нет конкретного примера» при живой
  сцене в лиде и H2 практике. Слот вышел после одной фразы
  «Разберём этот конкретный пример…» + новый POST (не resume).
- user: сайт не бракует слог; в репо нет гейта «конкретный пример» /
  «возьмём/например/кейс». Не лечить «Возьмём:». Не помечать «починили сайт».

### Keep
- Живая сцена из research этой статьи в лиде (Writer смысл → Sol слог).
- H2 «Практика: чеклист шагов…» заранее.
- Publish тело не правит.

### Never again
- Ярлык «Возьмём:» / «например» / «кейс» как лечение 409.
- Возврат Sol, если практика уже в статье.
- Закрывать INC как «починили сайт».
