# Site brief — Excalibur-2-Cloud

Метаданные сайта и контент-стратегия для Cover / Scout / Publish.
Не источник prose для Writer (Writer = master prompt + research + titles-only).

## Сайт

- **site_name:** ТАРО СЕЙЧАС
- **site_url:** `{{SITE_BASE}}` (live URL только в Cloud Secrets / PUBLIC_SITE_URL)
- **language:** ru
- **niche:** Таро, психологический анализ отношений, глубокие расклады «Суть – Тень – Вектор», разбор мотивов партнеров и внутренних блоков.

## Продукт и CTA

См. `shared/tenant-config.json` → `cta_links`, `cta_required`.
Три ссылки воронки:
1. Telegram-бот: `https://t.me/TodayTaro_bot?start=id8293683394`
2. Макс-бот: `https://max.ru/id531102974575_bot`
3. ВК-аудио: `https://vk.com/app54565776`

## Редакция

- **формат:** how-to / чеклист / глубокий психологический разбор ситуации через Арканы Таро
- **канон:** `shared/pipeline-canon.json`
- **стиль:** `shared/article-style.md` + `shared/SOUL.md` + (если включено) `shared/dzen-content-rules.md`
- **темы:** Scout → handoff `topic_id` + короткий title; `memory/topics/` запрещена

## Главный герой визуала

- **cover_mode:** `host_reference`
- **reference / lock:** ведущая Виктория (`memory/cover/blog-hero.json` + `memory/cover/assets/Виктория.png`). Овальное лицо, зелёные глаза с карим оттенком (hazel), прямой тёплый блонд до плеч с натуральными корнями, структурированный белый двубортный блейзер, золотая подвеска-медальон. Сеттинг: современный минималистичный интерьер, стол с классическим раскладом Таро, студийный свет.
- **style:** `memory/cover/cover-design-code.json` + `memory/cover/quad-style-taro.json` (благородная палитра: белый #FFFFFF, графит #141821, тёплое золото #D4AF37, глубокий индиго #1A237E; психологический аналитический стиль без дешёвой магии, клипартов и мемов).

## Запреты

- VPN / обход блокировок (если `dzen_rf_pack`)
- Выдуманные цены
- Эмодзи в тексте статей (дефолт)
- Фраза «карта дня»
- Секреты и live hostname в git-артефактах (только `{{SITE_BASE}}`)
