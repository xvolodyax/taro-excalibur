# Site brief — Excalibur-2-Cloud

<!-- SETUP_REQUIRED: fills excalibur-blog-setup (блоки Site / CTA / Scout / Visual summary) -->

Метаданные сайта и контент-стратегия для Cover / Scout / Publish.
Не источник prose для Writer (Writer = master prompt + research + titles-only).

## Сайт

- **site_name:** _(pending setup)_
- **site_url:** `{{SITE_BASE}}` (live URL только в Cloud Secrets / PUBLIC_SITE_URL)
- **language:** ru
- **niche:** _(pending setup)_

## Продукт и CTA

См. `shared/tenant-config.json` → `cta_links`, `cta_required`.

## Редакция

- **формат:** how-to / чеклист / comparison / troubleshooting / новость с применением
- **канон:** `shared/pipeline-canon.json`
- **стиль:** `shared/article-style.md` + `shared/SOUL.md` + (если включено) `shared/dzen-content-rules.md`
- **темы:** Scout → handoff `topic_id` + короткий title; `memory/topics/` запрещена

## Главный герой визуала

- **cover_mode:** см. tenant-config (`host_reference` | `illustrative` | `unset`)
- **reference / lock:** `memory/cover/blog-hero.json` + **только** `memory/cover/assets/Виктория.png`
- **запрещены:** `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`, `victoria_ref.*`
- **style:** `memory/cover/cover-design-code.json` + style preset из Setup Visual

## Запреты

- VPN / обход блокировок (если `dzen_rf_pack`)
- Выдуманные цены
- Эмодзи в тексте статей (дефолт; Setup может ослабить)
- Секреты и live hostname в git-артефактах (только `{{SITE_BASE}}`)
