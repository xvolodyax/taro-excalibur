# Content lessons — ТАРО СЕЙЧАС

Канон: `shared/content-learning-contract.md`.
Исторические scorecard / judge / ensemble — read-only, не шаблон.
Writer prompt и Sol skill сюда не раздувать автоматически.

## LESSON-20260903-2045-B37-he-texted-need-to-talk-and-vanished
status: proposed
topic_id: B37
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: вечерний слот 03.09.2026 / 20:00 острый контакт / CTA bot (3 бесплатных расклада; приложение для «Суть – Тень – Вектор»). Scout канон: Дзен → сайт (только заголовки) → неделя → Wordstat. Живой сигнал недели: в канале Дзен ТАРО СЕЙЧАС (todaytaro_bot) разобран острый триггер подвешенного вечернего разговора «нам надо поговорить» с уходом в паузу. Отраслевые материалы Psychologies и Psychodemia подтверждают избегающее поведение и сброс тревоги. Тема не пересекается с B17, B18, B23, B29, B36. Не «карта дня». H1 — живая сцена («Он написал «нам надо поговорить» и пропал»), жирная фраза Wordstat изолированно в H1 не вставлялась. Wordstat OK_WITH_PARTIAL.
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip` + `memory/cover/blog-hero.json`
  finding: лицо только `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; глаза `green+hazel` (зелёные с легким карим). Рефы `viktoriaref.png` / latin alias / sheet запрещены и не использовались. Пакет: cover.png 16:9 + 3 врезки inline-01..03. В теле статьи нет `figure.cover-hero`. Kie Image 2 i2i выполнен с 1 попытки (`create_attempt=1`, task_id `64b14841ecd290c89ac836fbb083f10f`, state=success). Split + inject в article.html выполнен штатно через Range download.
- process: `site-publish-result.json`
  finding: публикация выполнена напрямую через site-api (`SITE_PUBLISH_TOKEN`; Hall / Дзен Студия не привлекались). Upload 201 (`article_id=51`), excerpt_clear 403 (не FAIL), approve 200, publish 200, live GET 200 (`live_ok=true`). Пермалинк: `{{SITE_BASE}}/blog/on-napisal-nam-nado-pogovorit-i-propal/`. Слот 21:21 статьей не закрывался. «Возьмём:» в тексте нет, лид после H1 один, тело после Sol не редактировалось.
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` пропущен / credentials blocker (секреты Метрики не заданы в Cloud Secrets).

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER

### Keep
- Scout берёт тему из живого сигнала (Дзен → сайт → неделя → Wordstat).
- H1 формулируется как живое наблюдаемое предложение, жирная фраза Wordstat не ставится ярлыком.
- Без формулировки «карта дня».
- Лицо на обложке строго `Виктория.png`, глаза зелёные с легким карим, стиль `victoria-studio`.
- В теле статьи только три inline-врезки, обложка повторно в текст не ставится (`figure.cover-hero` отсутствует).
- Сайт в текст не лезет, слово «Возьмём:» исключено.
- Публикация ключом `SITE_PUBLISH_TOKEN` (upload 201 → approve 200 → publish 200 → live 200). Hall не вызывается.

### Never again
- Писать «карта дня» в вечернем слоте.
- Использовать `viktoriaref.png` вместо `Виктория.png`.
- Вставлять `figure.cover-hero` в тело статьи.
- Переписывать слог статьи после Sol или добавлять искусственные маркеры «Возьмём:».

## LESSON-20260902-1455-B34-month-number-no-step
status: proposed
topic_id: B34
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: слот день 2026-09-02 / 16:00 нумерология / CTA vk_app (приложение; не bot). Scout канон: Дзен → сайт (только заголовки) → неделя → Wordstat. Сигнал недели 26.08–02.09: сентябрь 2026 как календарная 1 / «первый шаг» (Mail 27.08, Шняги 26.08 + комменты «не ждать чужого первого шага») против Дзен «Код отношений» 02.09 (сентябрь как 9 в году 1). Канал `dzen.ru/todaytaro_bot` жив, но карточка дня — сюжет B33, не B34. Не карта дня. Не клон B12 (личный год / 2026=1), B16 (личное число дня), B19 (число имени), B31 (сгоревший «потом / с осени»), B33 (ежедневный тёплый чат без зова). Ядро: календарная единица / его личный месяц описывает ритм недель, не делает шаг за него. H1 — наблюдаемая сцена («Его число месяца не делает шаг за него»), не жир Wordstat «нумерология сентября» (1093). Research = OK_WITH_PARTIAL (API v2 `topRequests`, 4 фразы); «личное число сентября» 53 = WORDSTAT PARTIAL (totalCount-only) — не стоп.
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip` + `memory/cover/blog-hero.json`
  finding: реф только `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; глаза `green+hazel` / зелёные с карим. `viktoriaref.png` / latin alias / sheet — forbid, не звали. Pack cover+3 inline. Kie `state=success`, `create_attempts=1`, `task_id` 1d44e959…. `cover_png_figures_removed=0` / `cover_hero_removed=0`; в теле только `figure.inline-quad` ×3, `figure.cover-hero` нет. Hall / MCP gpt-image-2 не звали.
- process: `memory/pipeline-fix-queue.md#INC-20260902-1428-cover-kie-result-download`
  finding: Kie create #1 success; `quad_apply` завис на полном GET CDN (~1.25/2.4 MiB). Recovered same billed URL, Range 2–4 KiB → canvas 2048×1152; split+inject PASS. Не второй createTask. INC-1428 still open (script hang) — не «починили Kie».
- process: `site-publish-result.json` + `community-cta-gate.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=45`; excerpt 403 = не FAIL; approve 200; publish 200; live GET 200; `live_ok=true`; `verdict=pass`. CTA vk_app PASS. H2 «Практика: как рассчитать его личный месяц и оценить готовность к шагу» уже в теле. Тело не правили. Один live 200 после B33 directory EACCES + live 404 не закрывает «починили сайт».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260902-1455-metrika-credentials-b34; B33 INC-0650, B32 INC-1945, B31 INC-1431, B30 INC-0659, B29 INC-2040, B28 INC-1526, B27 INC-0709 и B26 INC-1936 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- KIE_RESULT_DOWNLOAD_HANG (same-URL recover; INC-1428 still open — не recreate)

### Keep
- Scout сам берёт живой сигнал (Дзен «сегодня» + неделя Mail/Шняги «сентябрь 2026 = 1»). Дзен → сайт (заголовки) → неделя → Wordstat. Не формат «карта дня», даже если чужие арканы так подписаны. Слот 16:00 нумерология / CTA vk_app.
- Не клон B12 (год), B16 (день), B33 (ежедневный чат без зова). Канал todaytaro_bot 02.09 держит B33 — это чужая сцена, не сюжет B34.
- WORDSTAT PARTIAL / totalCount-only — не стоп. Research перепроверка OK_WITH_PARTIAL. Жир Wordstat («нумерология сентября») не в H1. H1 — наблюдаемая сцена.
- Заранее практика из фактов этой статьи (H2 «Практика: как рассчитать его личный месяц…»).
- Cover i2i только от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`, глаза зелёные с карим (`green+hazel`). `viktoriaref.png` / victoria-sheet / latin alias — forbid. Pack cover+3 inline; `cover.png` только файл обложки, не вторая картинка в теле (`cover-hero` не инжектить).
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать. Publish / Director тело не правят.
- После Kie success + CDN stall: тот же billed URL / Range resume, не второй createTask.

### Change
- Один live 200 / article_id=45 не закрывает B33 INC-0645 (directory EACCES + live 404) и B25–B32 409 как «починили сайт».
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.
- Cover result-CDN hang: INC-1428 already open; progress + shrink Range + fail-fast — скрипт, не тело.

### Never again
- Клон B12 личного года / B16 личного дня / B33 ежедневного чата без зова / B31 «потом с осени» / B19 числа имени.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Клеить жирную Wordstat («нумерология сентября») в H1.
- Стоп пайплайна из-за WORDSTAT PARTIAL / totalCount-only, если живой сигнал и перепроверка есть.
- Реф `viktoriaref.png` / victoria-sheet / `victoria.png` / строчная `виктория.png` вместо `Виктория.png`.
- Инжект `figure.cover-hero` / `cover.png` второй картинкой в тело.
- Второй billed Kie create после success + CDN stall.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот день / 16:00 нумерология / CTA vk_app / сигнал «сентябрь 2026 = календарная 1, личный месяц шаг не делает» держит Scout Дзен→сайт→неделя→Wordstat + H1-наблюдение + практику из research этой статьи; WORDSTAT PARTIAL ≠ стоп; live 200 / id 45 ≠ «сайт починили».
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Cover CDN hang: INC-1428 already open; не дублировать apply из этого прогона.

### Durable applied
- none this run. Prior Cover recover INC-1428 (same billed URL, Range resume) — Fixer pending; `article.html` B34 не трогали. Не «починили Kie». Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

## LESSON-20260902-0650-B33-morning-writes-daily-no-invite
status: proposed
topic_id: B33
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: слот утро 2026-09-02 / 09:00 / CTA bot (триплет/крест; не vk_app). Scout сам: канал `dzen.ru/todaytaro_bot` 02.09 живой (шапка «Ты пишешь, он молчит?!»; лента «1 день назад» — соседняя B28-боль), недельный SERP держит тёплую ежедневную переписку без зова. Не карта дня, не нумерология. Не клон B32 (пишет только ночью / днём молчит), B31 (сгоревший «потом / с осени»), B30 (сорвал слово), B29 (стена при живом чате), B28 (привет после месяцев — чат умирал), B27 (зовёт на выходные, горизонта нет — зов есть). Ядро: сообщения тёплые и регулярные; даты встречи нет. H1 — наблюдаемая сцена («Он пишет каждый день, но не зовёт»), не жир Wordstat «не зовет на свидание» (926) / «мужчина не зовет на свидание» (367). Узкие «он пишет но не зовет» 163 и «пишет каждый день но не зовет» 63 = WORDSTAT PARTIAL (totalCount-only) — не стоп. Research перепроверка = OK_WITH_PARTIAL (API v2 `topRequests`, 4 фразы).
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; глаза `green+hazel` / зелёные с карим (`memory/cover/blog-hero.json`). Pack cover+3 inline. Kie `state=success`, `create_attempts=1`, `task_id` 5098bc76…. `cover_png_figures_removed=0` / `cover_hero_removed=0`; в теле только `figure.inline-quad` ×3, `figure.cover-hero` нет. Hall / MCP gpt-image-2 не звали.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=43`; excerpt 403 = не FAIL; **первый approve 200**, `quality_score=100`, warnings `[]`. H2 «Практика одного шага: как проверить реальные намерения» уже в теле. Publish 500: «Не удалось создать каталог публикации: `/var/www/TaroSeoSite/blog/on-pishet-kazhdyj-den-no-ne-zovet` (EACCES)». Live GET 404; `site_status=approved`; `live_ok=false`; `sol_rewritten=false`; `false_example_409=false`; `director_next=needs_human_publish_dir_eacces`. Тело не правили. «Возьмём:» / «Сцена» в `article.html` нет. Это не sitemap EACCES (контракт B23: sitemap + live 200 = live_ok) и не 409 example (B27–B32).
- process: `memory/pipeline-fix-queue.md#INC-20260902-0645-publish-dir-eacces-b33`
  finding: Fixer already `status: fixed` (commit cbab9ae): directory EACCES + live 404 = `needs_human`, не sitemap skip; resume не слать approve, если API уже `approved`. Права www на каталог блога — вне репо. Не «починили сайт». Не урок «лечить EACCES текстом».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260902-0650-metrika-credentials-b33; B32 INC-1945, B31 INC-1431, B30 INC-0659, B29 INC-2040, B28 INC-1526, B27 INC-0709 и B26 INC-1936 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_PUBLISH_DIR_EACCES (первый approve 200 / quality 100; publish 500 каталог; live 404 / approved — не 409 example)

### Keep
- Scout сам берёт живой сигнал (канал + недельный SERP «пишет каждый день, но не зовёт»). Дзен → сайт (заголовки) → неделя → Wordstat. Не формат «карта дня», даже если утренний слот тенанта так подписан.
- WORDSTAT PARTIAL / totalCount-only — не стоп. Research перепроверка OK_WITH_PARTIAL. Жир Wordstat не в H1.
- Заранее практика из фактов этой статьи (H2 «Практика одного шага…»). Первый approve 200 + quality 100 — не доказательство, что «сайт починили» после B27–B32 409.
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`, глаза зелёные с карим (`green+hazel`). Pack cover+3 inline; `cover.png` только файл обложки, не вторая картинка в теле (`cover-hero` не инжектить).
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Publish / Director тело не правят. Directory EACCES + live 404 = `needs_human`, не PIPELINE FAIL после GATE PASS и не ярлык в тексте.

### Change
- Publish 500 directory EACCES ≠ sitemap EACCES (B23/B27/B28: sitemap + live 200 = live_ok). B33: каталог slug не создан, live 404 → `needs_human_publish_dir_eacces`. INC-0645 already fixed в скрипте; права www — вне репо.
- Один первый approve 200 / quality 100 не закрывает B25 INC-1423 / B26–B32 409 как «починили сайт».
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение publish 500 / EACCES / quality.
- Возврат Sol / правка тела, чтобы «починить» права каталога на сервере.
- Путать directory EACCES + live 404 с sitemap EACCES + live 200.
- Стоп пайплайна из-за WORDSTAT PARTIAL / totalCount-only, если живой сигнал и перепроверка есть.
- Клон B32 ночного ритма / B31 осени / B30 срыва слова / B29 стены при живом чате / B28 месяцев молчания (чат умирал) / B27 субботы без горизонта (зов есть).
- Клеить жирную Wordstat («не зовет на свидание», «мужчина не зовет на свидание») в H1.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот утро / живой сигнал «пишет каждый день, но не зовёт» держит Scout Дзен→сайт→неделя→Wordstat + H1-наблюдение + практику из research этой статьи; WORDSTAT PARTIAL ≠ стоп; directory EACCES + live 404 = needs_human, не PIPELINE FAIL после GATE PASS; 200 на первом approve ≠ «сайт починили».
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Directory EACCES: INC-0645 already fixed в скрипте; права www на `/var/www/TaroSeoSite/blog/<slug>` — needs-human вне репо; не дублировать apply из этого прогона.

### Durable applied
- none this run. Prior Fixer INC-0645 (commit cbab9ae): directory EACCES → `needs_human`, не sitemap skip; `article.html` B33 не трогали. Не «починили сайт». Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

## LESSON-20260901-1945-B32-evening-night-only-chat
status: proposed
topic_id: B32
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: слот вечер 2026-09-01 / CTA бот (3 расклада) + vk_app. Scout сам взял живой сигнал «пишет только ночью / днём молчит»: канал `dzen.ru/todaytaro_bot` 01.09 крутит «Ты пишешь, он молчит?!»; лента — вечерний внезапный контакт (~9 ч) и недельные посты про молчание / поздний экран. Не карта дня, не 21:21, не 16:00-нумерология. Не клон B31 (сгоревший «потом / с осени»), B30 (сорвал слово), B29 (стена при живом чате), B28 (привет после месяцев), B22 (ночной «Спишь?» после точки). H1 — наблюдаемая сцена («Он пишет только ночью, а днём молчит»), не жир Wordstat «парень пишет ночью» (1123; топ — «спокойной/доброй ночи») / «он пишет мне ночью» (1171). Ближе к боли: «он пишет ночью пишет днем» = 449. Wordstat перепроверка Research = OK (API v2 `topRequests`); часть фраз totalCount-only («он пишет только ночью» 162, «он пишет поздно ночью» 48) = WORDSTAT PARTIAL — не стоп.
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; глаза `green+hazel` / зелёные с карим. Pack cover+3 inline. Kie `state=success`, `create_attempts=1`, `task_id` 74c2b5be…. `cover_png_figures_removed=0` / `cover_hero_removed=0`; в теле только `figure.inline-quad` ×3, `figure.cover-hero` нет. Hall / MCP gpt-image-2 не звали.
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=42`; excerpt 403 = не FAIL; первый approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» при сцене ночного чата и H2 «Как изменить сценарий без драмы и выяснения отношений» уже в теле. Publish не звали; live GET 404; `site_status=quality_review`; `live_ok=false`; `sol_rewritten=false`; `director_next=false_example_409_no_body_edit`; `slot_21_21=not_closed`. Тело не правили. «Возьмём:» / «Сцена» в `article.html` нет. Скрипт `article_has_practice_h2` смотрел только «практик»/«чеклист» → `script_practice_h2_detect=false`; Publish переопределил `practice_h2_present=true`.
- process: `memory/pipeline-fix-queue.md#INC-20260901-1939-publish-false-409-example-b32` + INC-20260901-1405 (B31) + INC-20260901-0700 (B30) + INC-20260831-2035 (B29) + INC-20260831-0650 (B27)
  finding: тот же ложный 409 example. Чекер вне репо, `needs-human`. 409 example ≠ «Возьмём:» / «Сцена» / ярлык «конкретный пример»; Director/Publish тело не правили. SITE token GET quality → 403. Не помечено «починили сайт». Не урок «добавить Возьмём».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260901-1945-metrika-credentials-b32; B31 INC-1431, B30 INC-0659, B29 INC-2040, B28 INC-1526, B27 INC-0709 и B26 INC-1936 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (конкретный пример ≠ «Возьмём:»; первый upload; live 404 / quality_review)

### Keep
- Scout сам берёт живой сигнал («пишет только ночью / днём молчит» из канала + недели + SERP). Дзен → сайт (заголовки) → неделя → Wordstat. Не формат «карта дня», даже если вечерний слот тенанта так подписан.
- WORDSTAT PARTIAL / totalCount-only — не стоп. Research перепроверка OK. Жир Wordstat не в H1.
- Заранее практика из фактов этой статьи (H2 сценария / шагов). 409 example при сцене + практике в теле — не лечить ярлыком.
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`, глаза зелёные с карим (`green+hazel`). Pack cover+3 inline; `cover.png` только файл обложки, не вторая картинка в теле (`cover-hero` не инжектить).
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Publish / Director тело не правят. Слот 21:21 не закрывать этой статьёй.

### Change
- 409 «нет конкретного примера» при уже живой сцене + H2 практике — не слать Sol на ярлык (`false_example_409_no_body_edit`). Повтор B27 INC-0650 / B29 INC-2035 / B30 INC-0700 / B31 INC-1405 / B32 article_id=42.
- Не помечать B25 INC-1423 / B26–B31 409 как «починили сайт»: B32 снова 409 + live 404.
- Детектор `article_has_practice_h2` не видит H2 без слов «практик»/«чеклист» («Как изменить сценарий…»). Это скрипт, не тело; INC-1939 already needs-human.
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение 409 example. Не урок «добавить Возьмём».
- Возврат Sol на ярлык, если практика уже в статье.
- Стоп пайплайна из-за WORDSTAT PARTIAL / totalCount-only, если живой сигнал и перепроверка есть.
- Клон B31 осени / B30 срыва слова / B29 стены при живом чате / B28 месяцев молчания / B22 ночного «Спишь?» после расставания.
- Клеить жирную Wordstat («парень пишет ночью», «он пишет мне ночью», «спокойной ночи») в H1.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот вечер / живой сигнал «пишет только ночью» держит Scout Дзен→сайт→неделя→Wordstat + H1-наблюдение + практику из research этой статьи; WORDSTAT PARTIAL ≠ стоп; 409 example ≠ «Возьмём:»; live 404 = quality_review, не PIPELINE FAIL после GATE PASS.
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Site quality checker (вне репо) + детектор H2 практики — INC-1939 already needs-human; не дублировать apply из этого прогона.

### Durable applied
- none this run. Prior Fixer INC-1405 / INC-0700 / INC-2035 / INC-0650: контракт false-example 409 + не лечить ярлыком. `article.html` B32 не трогали. Не «починили сайт». Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

## LESSON-20260901-1431-B31-day-autumn-deadline
status: proposed
topic_id: B31
category: other
confidence: low

### Evidence
- artifact: none (skipped under human-first-v2)
  finding: `content-evidence-report.json` отсутствует; evidence_gate=SKIP, не BLOCK. Report не invent'ился. Gate-артефакт: `content-evidence-gate.json` status=SKIP.
- process: `research-notes.md` + `title-brief.json` + `research-agent-report.json`
  finding: слот день 2026-09-01 / 16:00 / CTA vk_app (приложение «Суть – Тень – Вектор»; не bot). Scout канон: Дзен → сайт (только заголовки) → неделя → Wordstat. Острый запрос — календарный дедлайн «потом / с осени / после лета»: лето кончилось, 1 сентября уже вторник, фраза не сменилась на день или шаг. Не карта дня, не нумерология. Не клон B30 (сорвал приход / звонок), B29 (стена при живом чате), B28 (привет после месяцев без шага), B27 (выходные есть, горизонта нет — привычный паттерн свиданий, не сгоревший сезонный срок), B26 («не готов», но остаётся). H1 — наблюдаемый сгоревший сезон («Лето кончилось, а он всё ещё говорит тебе «потом»»), не жир Wordstat «с осени» (243652) / «после лета» (2521002) / «давай осенью» (14530) / «потом осень» (3755) / «кормит завтраками» (4043) / «первый шаг» (ребёнок 379 у «он не делает шаг» 1348). Exact working_title «он откладывает отношения на осень» — EMPTY. Узкий хвост «он откладывает на осень» = 21 — не жир.
- process: `cover/quad-mcp-batch.json` + `cover/cover-registry.json` + `cover/kie-image-task.json` + `cover/quad-split-report.json` + `site-publish-result.json#strip`
  finding: реф `Виктория.png` (`prefer_local_reference` + local file); style `victoria-studio`; pack cover+3 inline. Kie `state=success`, `create_attempts=2`, `task_id` 0aa0a409…. `cover_png_figures_removed=0` / `cover_hero_removed=0`; в теле только `figure.inline-quad` ×3, `figure.cover-hero` нет. Hall / MCP gpt-image-2 не звали. Cover INC-20260901-1350 (tenant style_file / local-ref / gold) recovered this run → Fixer `status: fixed` (commit 21afd83); не «починили Kie».
- process: `site-publish-result.json`
  finding: SITE token сам (`token_env=SITE_PUBLISH_TOKEN`, Hall / Дзен Студия `not_used`). Upload 201 `article_id=41`; excerpt 403 = не FAIL; первый approve 409, `quality_score=88`, warning «Нет конкретного примера или разбора ситуации» при H2 «Практика: чеклист шагов, как отличить точный срок от повторного тумана» уже в теле. Publish 409 «только одобренную»; live GET 404; `site_status=quality_review`; `live_ok=false`; `sol_rewritten=false`; `director_next=false_example_409_no_body_edit`. Тело не правили. «Возьмём:» / «Сцена» в `article.html` нет.
- process: `memory/pipeline-fix-queue.md#INC-20260901-1405-publish-false-409-example-b31` + INC-20260901-0700 (B30) + INC-20260831-2035 (B29) + INC-20260831-0650 (B27)
  finding: тот же ложный 409 example, что B27/B29/B30. Чекер вне репо, `needs-human`. 409 example ≠ «Возьмём:» / «Сцена» / ярлык «конкретный пример»; Director/Publish тело не правили (`false_example_409_no_body_edit`). SITE token GET quality / force-approve → 403. Не помечено «починили сайт».
- metrika_signal: none
  finding: `excalibur_blog_metrika_fetch.py --days 30 --ingest` → METRIKA CREDENTIALS BLOCKER (нет `YANDEX_METRIKA_OAUTH_TOKEN` / `YANDEX_METRIKA_COUNTER_ID`). `memory/analytics/metrika-latest.json` не создан. Цифры не выдумывать. См. INC-20260901-1431-metrika-credentials-b31; B30 INC-0659, B29 INC-2040, B28 INC-1526, B27 INC-0709 и B26 INC-1936 всё ещё open.

### Named blockers
- EVIDENCE_SKIPPED
- METRIKA FEEDBACK BLOCKER
- SITE_QUALITY_409 (конкретный пример ≠ «Возьмём:»; первый upload; live 404 / quality_review)

### Keep
- Scout: Дзен → сайт (заголовки) → неделя → Wordstat. Дневной острый запрос «потом / с осени» как сгоревший календарный дедлайн — не формат «карта дня», даже если чужие недельные арканы так подписаны.
- Календарный дедлайн «потом / с осени» ≠ B27 (выходные есть, горизонта нет). B27 — привычный паттерн свиданий без разговора о будущем; B31 — сезон, который он сам назвал сроком, уже наступил.
- Жир Wordstat не в H1.
- Заранее H2 «Практика: чеклист шагов…» из фактов этой статьи. 409 example при практике в теле — не лечить ярлыком.
- Cover i2i от рефа `Виктория.png` (`prefer_local_reference` + local file), style `victoria-studio`. Pack cover+3 inline; `cover.png` только файл обложки, не вторая картинка в теле (`cover-hero` не инжектить).
- SITE token сам: upload → approve → publish; Hall / Дзен Студия не звать.
- Publish / Director тело не правят.

### Change
- 409 «нет конкретного примера» при уже живой сцене + H2 практике — не слать Sol на ярлык (`false_example_409_no_body_edit`). Повтор B27 INC-0650 / B29 INC-2035 / B30 INC-0700 / B31 article_id=41.
- Не помечать B25 INC-1423 / B26–B30 409 как «починили сайт»: B31 снова 409 + live 404.
- Metrika secrets по-прежнему отсутствуют — следующий Content-learner снова BLOCKER, пока секреты не в Cloud Secrets.

### Never again
- «Возьмём:» / «Возьмем:» / «Сцена» как лечение 409 example.
- Возврат Sol на ярлык, если практика уже в статье.
- Клон B30 срыва слова / B29 стены при живом чате / B28 месяцев молчания / B27 субботы без горизонта / B26 «не готов».
- Сливать B31 с B27: «потом / с осени» — сгоревший сезонный срок, не «зовёт на выходные, но не говорит про будущее».
- Клеить жирную Wordstat («с осени», «после лета», «давай осенью», «потом осень», «кормит завтраками», «первый шаг») в H1.
- Закрывать слот картой дня / числом дня / 21:21 этой статьёй.
- Раздувать `shared/writer-master-prompt.md` / Writer / Sol skill автоматически (один кейс + evidence SKIP + no-Metrika).

### Proposed apply
- Review-only: слот день / 16:00 / CTA vk_app / календарный дедлайн «потом / с осени» держит Scout Дзен→сайт→неделя→Wordstat + H1-наблюдение + практику из research этой статьи; 409 example ≠ «Возьмём:»; live 404 = quality_review, не PIPELINE FAIL после GATE PASS.
- Не добавлять правила в `shared/writer-master-prompt.md` и Writer/Sol skill автоматически.
- Cloud Secrets: `YANDEX_METRIKA_OAUTH_TOKEN` + `YANDEX_METRIKA_COUNTER_ID` (scope `metrika:read`).
- Site quality checker (вне репо) — INC-1405 already needs-human; не дублировать apply из этого прогона.
- Cover tenant style/local-ref: INC-1350 already fixed (commit 21afd83); не помечать «починили Kie».

### Durable applied
- none this run. Prior Fixer INC-1350 (commit 21afd83): tenant `style_preset` + local `Виктория.png` + gold/editorial; `article.html` B31 не трогали. Prior Fixer INC-1405: контракт B27/B29/B30/B31 + SITE token quality/force-approve 403; не лечить ярлыком. Не «починили сайт». Rollback: только по явному решению человека, не из этого SKIP+no-Metrika прогона.

### Resolution
status: recorded

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
