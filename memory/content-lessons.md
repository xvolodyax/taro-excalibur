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
- none — practice/checklist 409 на B26 первый раз; B24/B25 были про форму opening, не про этот чекер. Rollback не нужен.

### Resolution
status: recorded
