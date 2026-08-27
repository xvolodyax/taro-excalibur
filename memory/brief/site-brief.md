# Site brief — ТАРО СЕЙЧАС

Метаданные сайта и контент-стратегия для Cover / Scout / Writer / Sol / Publish.
Не источник prose для Writer (Writer = master prompt + research + titles-only).

## Сайт

- **site_name:** ТАРО СЕЙЧАС
- **site_url:** `https://www.xn--80aakc2ajeicm8b4d.xn--p1ai/` (IDN: https://www.таросейчас.рф/) — публичный, не секрет
- **blog:** `https://www.таросейчас.рф/blog/`
- **canonical article URL в артефактах:** `{{SITE_BASE}}/<slug>/` (без `/blog/`)
- **language:** ru
- **niche:** таро / отношения. Ядро — женщины 20–50. Покупают не «таро», а доступ к голове человека, которого нельзя спросить. Около 78% запросов — отношения.

## Продукт и CTA

`cta_required: true`. Не путать **бот** и **приложение**.

| Куда | Что можно обещать | Ссылка |
|------|-------------------|--------|
| Бот (Макс; на сайте ещё Telegram) | 3 бесплатных расклада: триплет / крест | [бот Макс](https://max.ru/id531102974575_bot) |
| Приложение ВК | «Суть – Тень – Вектор», аудиоразбор | [приложение ВК](https://vk.com/app54565776) |
| Приложение Макс | то же, что ВК | [приложение Макс](https://max.ru/id531102974575_bot?startapp=ref_9BAD4149) |
| Сайт дополнительно | Telegram-бот и Telegram-приложение | [Telegram бот](https://t.me/TodayTaro_bot?start=id8293683394), [Telegram приложение](https://t.me/TodayTaro_bot?startapp=ref_361BDE45) |

Обязательные `cta_links` (есть в каждой статье, в том числе для Дзена):

1. https://max.ru/id531102974575_bot
2. https://vk.com/app54565776
3. https://max.ru/id531102974575_bot?startapp=ref_9BAD4149

Сайт-only (`cta_links_site_only`, **не** в Дзен и **не** в `cta_links` гейта):

- https://t.me/TodayTaro_bot?start=id8293683394
- https://t.me/TodayTaro_bot?startapp=ref_361BDE45

Правила текста:

- два блока, не копипаст: после сцены «сразу к делу» (выжимка + 2–3 вопроса к картам + две двери) и свой продающий финал;
- сырые URL в теле не светить — только гиперссылки в слова;
- не писать «личный аудиоразбор»;
- Дзен: без Telegram.

Публикацию на сайт и в Дзен делает **Hall**, не этот пайплайн. RSS в Дзен не подключать. `EXCALIBUR_BLOG_ALLOW_PUBLISH` выкл.

## Редакция

- **формат:** живая сцена про отношения / карту / число → практика → две двери (бот / приложение)
- **канон:** `shared/pipeline-canon.json`
- **стиль:** `shared/article-style.md` + `shared/SOUL.md` + `shared/dzen-content-rules.md`
- **темы:** Scout → handoff `topic_id` + короткий title; `memory/topics/` запрещена
- **слоты (для Hall / расписания, не автопубликация пайплайна):**
  - 09:00 — острый запрос → бот
  - 16:00 — нумерология → приложение ВК
  - 20:00 — карта дня → бот

## Scout

- signal_urls: https://dzen.ru/todaytaro_bot ; https://www.таросейчас.рф/blog/
- Wordstat: Yandex Cloud Search API v2, folderId `b1g0a71ifv910gjalmhp` (ключ только в Secrets).
- Внешнего агента Вордстат не звать: Scout ищет сам.
- До Scout: прочитать `shared/dzen-content-rules.md` + `shared/rf-blocked-entities.json`.

## Главный герой визуала

- **cover_mode:** `host_reference`
- **host:** Виктория (`author_id=victoria`). Алёну на обложки не ставить.
- **reference:** `memory/cover/assets/victoria.png` (канон имени; в checkout бинарник может отсутствовать — Cover i2i не запускать без файла)
- **lock:** `memory/cover/blog-hero.json` — платиновый блонд, прямой пробор; глаза зелёные + hazel у зрачка; тёмные брови, чёрная стрелка; mauve помада; тёплый загар. Одежда и эмоция каждый раз новые (белый блейзер рефа — не lock).
- **style:** `memory/cover/cover-design-code.json` + `memory/cover/quad-style-victoria-studio.json`
- **палитра:** фон `#FFFFFF`, ink `#141821`, акцент сдержанное золото/nude `#C4A574` / `#D4B5A0`. Не `#FF1493`, не gothic.
- **подпись кодом над картинкой** (не рисовать нейросетью): `Виктория - таролог команды «ТАРО СЕЙЧАС»`
- хук 2–6 слов на кадре, не заголовок статьи. `meme_caption_ru` всегда пуст.
- светлая high-key студия, business-chic. Не тёмный стол со свечами, не gothic, не pink-cat коллаж.
- Kie GPT Image 2, i2i, 2K. Холст 2×2, резка по белым швам. Inline без людей и лиц, 3–6 кириллических labels.
- лицо не Вики или кривой шов → пересобрать холст, не чинить лицо снаружи.

## Запреты

- таргет 13–17
- СВО / медицина
- обещать прочитать мысли; пугать одиночеством
- VPN / обход блокировок (`dzen_rf_pack`)
- выдуманные цены
- эмодзи в тексте статей
- мат (Дзен)
- секреты и ключи в git
- Telegram-ссылки в материале для Дзена
- RSS-автопостинг в Дзен
