# Content lessons — ТАРО СЕЙЧАС

Канон: `shared/content-learning-contract.md`.
Исторические scorecard / judge / ensemble — read-only, не шаблон.
Writer prompt и Sol skill сюда не раздувать автоматически.

## LESSON-20260901-0659-B30-morning-broken-word
status: proposed
topic_id: B30
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: слот утро 2026-09-01 / 09:00 / CTA bot (триплет/крест; не vk_app). Scout канон: Дзен → сайт (только заголовки) → неделя → Wordstat. Острый запрос «дал слово (прийти / позвонить) и сорвал». Не карта дня, не нумерология. Не клон B29 (стена при живом чате / пауза вместо сближения), B28 (привет после месяцев без шага), B27 (выходные есть, горизонта нет), B26 («не готов», но остаётся), B20 (карта дня + отмена свидания). H1 — наблюдаемый срыв слова («Он обещает прийти или позвонить, но не держит слово»), не жирные Wordstat «он обещал» (27568) / «он врёт» (21312) / «он не пришёл» (161262) / «таро на отношения» (52289). Угол Scout «он не держит слово» = 1334 — не жир, жирнее в H1 не клеить.
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; pack cover+3 inline. Cover INC-20260901-0648: Kie `failCode=500` ×2 (`create_attempt=1` затем max-1 recreate). Cover не выдумал третий `createTask`, не повышал `--max-create-retries`, batch не менял. Director same-batch re-run → `state=success` (`task_id` c112399b…, `create_attempts=3` = успешный Director-прогон, не Cover-retry). `cover_png_figures_removed=0` / `cover_hero_removed=0`; в теле только `figure.inline-quad` ×3, `figure.cover-hero` нет. Hall / MCP gpt-image-2 не звали.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=40`; excerpt 403 = не FAIL; первый approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» при H2 «Практика: чеклист шагов, как отличить случайный срыв от пустых обещаний» уже в теле. Publish 409 «только одобренную»; live GET 404; `site_status=quality_review`; `live_ok=false`; `sol_rewritten=false`; `director_next=false_example_409_no_body_edit`. Тело не правили. «Возьмём:» / «Сцена» в `article.html` нет.
- process: `memory/pipeline-fix-queue.md#INC-20260901-0700-publish-false-409-example-b30` + INC-20260831-2035 (B29) + INC-20260831-0650 (B27)
  finding: тот же ложный 409 example, что B27/B29. Чекер вне репо, `needs-human`. 409 example ≠ «Возьмём:» / «Сцена» / ярлык «конкретный пример»; Director/Publish тело не правили (`false_example_409_no_body_edit`). SITE token GET quality / force-approve → 403. Не помечено «починили сайт».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260901-0659-metrika-credentials-b30; B26 INC-1936, B27 INC-0709, B28 INC-1526 и B29 INC-2040 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (конкретный пример ≠ «Возьмём:»; первый upload; live 404 / quality_review)
- KIE API BLOCKER (500×2; recovered Director same-batch; INC-0648 still open — не «починили Kie»)

### Keep
- Scout: Дзен → сайт (заголовки) → неделя → Wordstat. Утренний острый запрос «дал слово и сорвал» — не формат «карта дня», даже если чужие утренние арканы так подписаны.
- Жир Wordstat не в H1.
- Заранее H2 «Практика: чеклист шагов…» из фактов этой статьи. 409 example при практике в теле — не лечить ярлыком.
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`. Pack cover+3 inline; `cover.png` только файл обложки, не вторая картинка в теле (`cover-hero` не инжектить).
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- После Kie 500×2: Cover стоп + неизменный `quad-mcp-batch.json`; Director `--director-same-batch`, затем Cover apply-only. Publish / Director тело не правят.

### Change
- 409 «нет конкретного примера» при уже живой сцене + H2 практике — не слать Sol на ярлык (`false_example_409_no_body_edit`). Повтор B27 INC-0650 / B29 INC-2035 / B30 article_id=40.
- Не помечать B25 INC-1423 / B26–B29 409 как «починили сайт»: B30 снова 409 + live 404.
- После Cover 500×2 не поднимать `--max-create-retries` и не звать третий `createTask` из Cover. Канон — Director same-batch.
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение 409 example.
- Третий billed Kie `createTask` из Cover после 500×2 (не повышать retries, не soften prompt, не MCP).
- Возврат Sol на ярлык, если практика уже в статье.
- Клон B29 стены при живом чате / B28 месяцев молчания / B27 субботы без горизонта / B26 «не готов».
- Клеить жирную Wordstat («он обещал», «он врёт», «он не пришёл», «таро на отношения») в H1.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот утро / 09:00 / CTA bot / «дал слово и сорвал» держит Scout Дзен→сайт→неделя→Wordstat + H1-наблюдение + практику из research этой статьи; 409 example ≠ «Возьмём:»; live 404 = quality_review, не PIPELINE FAIL после GATE PASS.
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Site quality checker (вне репо) — INC-2035 already needs-human; не дублировать apply из этого прогона.
- Cover 500×2: INC-0648 — Director `--director-same-batch` + Cover apply-only; не помечать «починили Kie».
- Site quality 409: INC-0700 needs-human (чекер вне репо).

### Durable applied
- 2026-09-01 Fixer INC-0648: скрипт отказывает Cover в третьем create после 500×2; Director `--director-same-batch`; после success skip create (apply-only). B30 на кластере. Не «починили Kie».
- 2026-09-01 Fixer INC-0700: контракт B27/B29/B30 + SITE token quality/force-approve 403; не лечить ярлыком. `article.html` B30 не трогали. Не «починили сайт».

### Resolution
status: recorded

## LESSON-20260831-2040-B29-evening-wall-live-chat
status: proposed
topic_id: B29
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-context.json`
  finding: слот вечер 2026-08-31 / 20:00 / CTA bot; острый запрос «стена при живом чате» (отвечает, иногда сам пишет, встреча может быть — но шаг ближе сам режет). Не карта дня (вечерний слот тенанта так подписан — игнорировать). Не клон B26 («не готов», но остаётся), B27 (выходные есть, осени нет), B28 (привет после месяцев без конкретного шага). H1 — наблюдаемый живой контакт без шага («Он остаётся на связи, но ставит паузу вместо сближения»), не жирные Wordstat «пауза в отношениях» (9033) / «он отдалился» (3943) / «он не пишет первым» (3924).
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; Kie `state=success`, `create_attempts=1`. `cover_png_figures_removed=0` / `cover_hero_removed=0` — cover не в теле. Hall / MCP gpt-image-2 не звали.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=39`; excerpt 403 = не FAIL; первый approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» при H2 «Практика: чеклист шагов, когда диалог есть, а движения навстречу нет» уже в теле. Publish 409 «только одобренную»; live GET 404; `site_status=quality_review`; `live_ok=false`; `sol_rewritten=false`; `slot_2121=not_closed`. Тело не правили.
- process: `memory/pipeline-fix-queue.md#INC-20260831-2035-publish-false-409-example-b29` + LESSON-20260831-2035-B29-false-example-409
  finding: Fixer-фрагмент про 409/пример уже записан; этот блок — полный slot-lesson Content-learner. 409 example ≠ «Возьмём:»; Director/Publish тело не правили (`false_example_409_no_body_edit`). Не помечено «починили сайт».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260831-2040-metrika-credentials-b29; B26 INC-1936, B27 INC-0709 и B28 INC-1526 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (конкретный пример ≠ «Возьмём:»; первый upload; live 404 / quality_review)

### Keep
- Вечерний острый запрос «стена при живом чате» — не формат «карта дня», даже если слот 20:00 так назван у тенанта.
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`.
- `cover.png` только файл обложки, не вторая картинка в теле.
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Заранее H2 «Практика: чеклист шагов…» из фактов этой статьи. 409 example при практике в теле — не лечить ярлыком.
- Publish / Director тело не правят. Слот 21:21 не закрывать этой статьёй.

### Change
- 409 «нет конкретного примера» при уже живой сцене + H2 практике — не слать Sol на ярлык (`false_example_409_no_body_edit`). Повтор B27 INC-0650 / B29 INC-2035.
- Не помечать B25 INC-1423 / B26–B27 409 как «починили сайт»: B29 снова 409 + live 404.
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение 409 example.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Клеить жирную Wordstat («пауза в отношениях», «он отдалился», «он не пишет первым») в H1.
- Сливать угол с B26 («не готов, но остаётся»), B27 (живой календарь субботы без осени), B28 (привет после месяцев без шага).
- Возврат Sol на ярлык, если практика уже в статье.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот вечер / 20:00 / «стена при живом чате» держит H1-наблюдение + практику из research этой статьи; 409 example ≠ «Возьмём:»; live 404 = quality_review, не PIPELINE FAIL после GATE PASS.
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Site quality checker (вне репо) — INC-2035 already needs-human; не дублировать apply из этого прогона.

### Durable applied
- none this run. Prior Fixer INC-2035 (commit 3726cd9): после GATE PASS + H2 практики не слать Sol на ярлык; `article.html` B29 не трогали. Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

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

## LESSON-20260831-2035-B29-false-example-409
status: recorded
topic_id: B29
category: publish
confidence: medium

### Evidence
- process: INC-20260831-2035 — GATE PASS, upload 201 `article_id=39`,
  approve 409, `quality_score=88`, warning «Нет конкретного примера
  или разбора ситуации». H2 практики уже в теле. Повтор B27 INC-0650.
- user / Hall: сайт текст не бракует; в репо нет гейта «конкретный
  пример» / «возьмём / например / кейс». Не лечить «Возьмём:».
  Директор тело не правил. Чекер качества — вне репо.

### Keep
- После GATE PASS + H2 «Практика: чеклист шагов…» — не слать Sol
  на ярлык (`false_example_409_no_body_edit`).
- Publish / Director тело не правят.

### Never again
- Возврат Sol на ярлык «конкретный пример», если практика уже в статье.
- Закрывать INC как «починили сайт».

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

## LESSON-20260831-1526-B28-day-silence-return
status: proposed
topic_id: B28
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-context.json`
  finding: слот день 2026-08-31 / 16:00 / CTA vk_app; острый запрос «написал после месяцев молчания, шага нет». Не карта дня, не утренний B27 («зовёт на выходные»), не вечерний B26 («не готов, но остаётся»), не B22 (рваный контакт без долгой ямы). H1 — наблюдаемое сообщение без плана («Он написал после месяцев молчания, но не предлагает ничего конкретного»), не жирная Wordstat «он объявился» (4446) / «объявился бывший» (3130).
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; `cover_png_figures_removed=0` / `cover_hero_removed=0` — cover не в теле. Первый Kie poll window исчерпан на still-`generating` (INC-1508); тот же `task_id` → late 500 → max-1 recreate → success. Hall / MCP gpt-image-2 не звали.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=38`; excerpt 403 = не FAIL; **первый approve 200** (без 409); publish 500 sitemap EACCES + live GET 200 = `live_ok`; `practice_h2_present=true`; `sol_rewritten=false`. H2 «Практика: чеклист шагов, если он написал после долгой тишины» уже в финале.
- process: `memory/pipeline-fix-queue.md#INC-20260831-1508-cover-kie-poll-timeout-b28`
  finding: Cover timeout уже закрыт Fixer (commit 0f076d7): `--max-wait` 1500 + `--late-poll-extend` на том же taskId; не третий billed create. `article.html` B28 Fixer не трогал.
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260831-1526-metrika-credentials-b28; B26 INC-1936 и B27 INC-0709 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- KIE_POLL_TIMEOUT (первый window; recovered same-task + recreate; Fixer INC-1508 already fixed)

### Keep
- Дневной острый запрос «написал после месяцев тишины, шага нет» — не формат «карта дня».
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`.
- `cover.png` только файл обложки, не вторая картинка в теле.
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Заранее H2 «Практика: чеклист шагов…» из фактов этой статьи. Первый approve 200 при практике в теле — не доказательство, что «сайт починили».
- Publish тело не правит. Sitemap EACCES + live 200 = `live_ok`.
- Cover: после poll-window на still-`generating` — тот же `task_id`, не новый create.

### Change
- Один первый approve 200 не закрывает B25 INC-1423 / B26–B27 409 как «починили сайт».
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение quality.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Клеить жирную Wordstat («он объявился», «объявился бывший») в H1.
- Сливать угол с B22 (рваный контакт), B26 («не готов, но остаётся»), B27 (живой календарь субботы).
- Третий billed Kie create после timeout на still-`generating`.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот день / 16:00 / «написал после молчания» держит H1-наблюдение + практику из research этой статьи; 200 на первом approve ≠ «сайт починили».
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Cover durable уже в Fixer INC-1508 — не дублировать apply из этого прогона.

### Durable applied
- none this run. Prior Fixer INC-1508 (commit 0f076d7): Kie late-poll same taskId + max-wait 1500; recreate max-1. Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded
