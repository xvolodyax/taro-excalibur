# Setup answers log

Заполнено Setup 2026-08-27 из ответов владельца. **Секретов и ключей нет.**

## Cloud

- Environment: этот прогон = First-run Setup в Cloud Agent. Новых Secrets у человека не просили.
- Memories: **OFF желательны** (в Automation → Tools). Docs Cursor: Memories ON by default. Игнорировать Automation Memory.
- Публикацию на сайт и в Дзен делает **Hall**, не этот пайплайн.
- `EXCALIBUR_BLOG_ALLOW_PUBLISH` оставить выкл (`no` / unset).
- Kie (`KIE_API_KEY`) и Wordstat уже лежат в секретах снаружи; в git не класть.
- `PUBLIC_SITE_URL` публичный (не секрет): `https://www.xn--80aakc2ajeicm8b4d.xn--p1ai/` (IDN таросейчас.рф).
- FTP/SFTP для этого пайплайна не нужны: Hall публикует руками.
- First-run = Setup (этот прогон). Daily automation — только после `setup_complete`.

## Site

- brand_name: ТАРО СЕЙЧАС
- language: ru
- niche: таро / отношения; ядро — женщины 20–50. Покупают не «таро», а доступ к голове человека, которого нельзя спросить. ~78% запросов — отношения.
- цели: глубокие живые статьи без воды → бот (расклад) или приложение (аудиоразбор).
- не таргет 13–17; не СВО / медицина; не обещать прочитать мысли; не пугать одиночеством.
- сайт: `https://www.таросейчас.рф/blog/`
- Дзен-канал: `todaytaro_bot` (`https://dzen.ru/todaytaro_bot`). RSS в Дзен **не** подключать. Hall кладёт статьи в Дзен руками.
- dzen_rf_pack: true
- слоты: 9:00 острый запрос → бот; 16:00 нумерология → приложение ВК; 20:00 карта дня → бот.

## Author

- author_id: `victoria`
- имя / подпись: Виктория — таролог команды «ТАРО СЕЙЧАС»
- Алёну на обложки статей **не** ставить.

## Voice

- Живой «ты», женский род. Простые слова. Глубина за счёт одной конкретной сцены, не поэзии.
- Старт: живая сцена, не название механики и не «в этой статье разберём».
- Одна сцена, один чат, одна ловушка. Абзац, который ничего не двигает, вылетает. Без тройного пересказа одной паузы.
- Без штампов «давай честно / знакомо / представь». Если фразу надо объяснять — выкинуть.
- Не гладить голос под SEO. Writer = смысл. Sol = слог. После Sol прозу не переписывать.
- Эталоны (каркас ок, слог ещё сделать живее — задача Setup Voice):
  - https://www.таросейчас.рф/blog/chto-govorit-karta-dnya-esli-on-zovet-segodnya-vecherom/
  - https://www.таросейчас.рф/blog/lichnoe-chislo-goda-etim-letom/
  - https://dzen.ru/a/ao3MoT45IyRaeMYz
  - https://dzen.ru/a/ao2f51866jPqRf2L
- good-outputs: живая сцена + короткий бит.
- bad-outputs: вода, SEO-хвост, «в этой статье», тройной пересказ паузы.

## Visual

- cover_mode: `host_reference` (Виктория).
- реф: owner CANON LOCK 2026-08-28 — только `victoria-sheet.png` (character sheet / Instagram carousel). Другие face-ref удалены. Глаза зелёные с лёгким hazel. Cover i2i ждёт `memory/cover/assets/victoria-sheet.png`.
- глаза: зелёные + слегка светло-карие.
- волосы только с рефа: светлый блонд + honey/пепел, корни темнее. Не платина, не ice-blonde, не осветлять. Платина / сильно светлее рефа = пересобрать холст.
- обложка: лицо по рефу; эмоция и одежда каждый раз новые. Хук 2–6 слов на кадре, не заголовок статьи.
- типографика 27.08: editorial display (didone / refined grotesque), не Arial/Roboto/Inter/Impact/Times/bold condensed; highlight той же гарнитурой золотом медальона; sticky/inline — humanist sans; кривые буквы = пересобрать холст.
- холст 2K 2×2, резка по белым швам. В тексте inline — без лица.
- подпись на обложке **кодом**: `Виктория - таролог команды «ТАРО СЕЙЧАС»`.
- не тёмный стол со свечами. Kie GPT Image 2.
- если лицо не Вики / волосы платина или сильно светлее рефа / шов — пересобрать холст, не чинить лицо и волосы снаружи.
- Алёну на обложки не ставить.

## CTA

- cta_required: true
- не путать бот и приложение.
- «Суть – Тень – Вектор» / аудиоразбор — только в приложении.
- 3 бесплатных расклада (триплет/крест) — только в боте.
- не писать «личный аудиоразбор».
- два блока ссылок: после крючка «сразу к делу» (выжимка + 2–3 вопроса к картам + две двери) и свой продающий финал. Не копипаст.
- Дзен: без Telegram.
- везде (Дзен + сайт): бот Макс, приложение ВК, приложение Макс.
- сайт дополнительно: Telegram бот, Telegram приложение.
- сырые URL в теле не светить, только гиперссылки в слова.

Ссылки (не секреты):

- бот Макс: https://max.ru/id531102974575_bot
- приложение ВК: https://vk.com/app54565776
- приложение Макс: https://max.ru/id531102974575_bot?startapp=ref_9BAD4149
- сайт / Telegram бот: https://t.me/TodayTaro_bot?start=id8293683394
- сайт / Telegram приложение: https://t.me/TodayTaro_bot?startapp=ref_361BDE45

## Scout

- Wordstat: Yandex Cloud Search API v2, folderId `b1g0a71ifv910gjalmhp`. Ключ: Cloud Secret `YANDEX_CLOUD_SEARCH_API_KEY` или gitignored `memory/wordstat.env.local` (шаблон `memory/wordstat.env.local.example`). Не в git и не в чат.
- signal_urls:
  - https://dzen.ru/todaytaro_bot
  - https://www.таросейчас.рф/blog/
- Агента Вордстат снаружи не звать: Scout ищет сам.
