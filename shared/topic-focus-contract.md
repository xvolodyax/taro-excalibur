# Topic Focus Contract (HARD)

**Обновлено:** 2026-08-21  
**Владелец:** Scout + `scripts/excalibur_blog_topic_focus.py` + `research_start`  
**Тенант:** ТАРО СЕЙЧАС

Этот контракт — **жёсткий gate**, не «советы». Новая тема обязана попасть
в ядро канала (женщины 20–50, около 78% тем про отношения), а не в
скелет Cursor/AI и не в RF/Дзен DENY.

**До Scout обязательно:** `shared/dzen-content-rules.md` +
`shared/rf-blocked-entities.json`.

---

## Ядро (ALLOW — новая тема обязана попасть сюда)

Новая тема **обязана** содержать минимум один маркер ядра в title
(проверяется вместе со slug):

- таро / расклад / карты
- пауза / конец (крючок-образец «Пауза или конец?»)
- отношения
- что он чувствует / молчит / молчание
- вернётся ли
- написать первой
- смотрит истории
- расставание / измена / любовь / парень
- аудиоразбор / бот в Макс (разные продукты: расклад в боте, «Суть – Тень – Вектор» в приложении; не сырой URL)

Лучший крючок-образец: **«Пауза или конец?»**.
Живые углы Scout: пауза; что чувствует; вернётся; написать первой;
смотрит истории (`tenant-config.scout_live_angles`).

## Не жевать как новую тему

Уже были на Дзене `todaytaro_bot` (см. `shared/published-titles.md`):

- «он не пишет»
- «дата рождения»

Это не RF DENY, но Scout **не берёт** их как новую карточку.

## Жёсткий запрет (DENY — перекрывает ALLOW)

| Кластер | Примеры запрета |
|--------|------------------|
| Скорость сайта | PageSpeed, Core Web Vitals, LCP/INP/CLS |
| Счётчики/кабинеты | GA4, Метрика/Вебвизор, Директ, Вебмастер, GSC |
| **RF / Дзен DENY heroes** | Meta, Facebook, Instagram, Threads, LinkedIn, Twitter/X, Discord, VPN/обход |
| СВО / война | «СВО» как герой темы |
| Медицина | самолечение, диагнозы |
| Читать мысли | обещание «прочитать мысли» |
| Telegram | каналы, боты, t.me в теме |
| Таргет 13–17 | подростки как аудитория |

**meta-теги SEO** — не Meta Platforms; DENY не срабатывает на `meta-тег*`.

Cursor / MCP / Make / n8n / LLM — **не ядро** этого тенанта. Не брать
как тему даже если хайп свежий.

## Кто проверяет

1. **Директор до Scout:** прочитал `dzen-content-rules.md` + rf-blocked.
2. Scout **до** handoff:
   ```bash
   python3 scripts/excalibur_blog_topic_focus.py --text "<title>"
   python3 scripts/excalibur_blog_scout_helper.py --check-focus "<title>"
   ```
3. `excalibur_blog_scout_helper.py --check-query` автоматически гоняет focus gate.
4. `excalibur_blog_research_start.py --title` — BLOCK до SERP, если off-focus.
5. `excalibur_blog_today.py` — всегда `needs_scout` (пул topics удалён).

## Внешний сигнал (Scout)

Новая тема обязана опираться на **свежий** сигнал этой недели
(`signal_urls` в handoff): канал Дзена `todaytaro_bot`, сайт тенанта,
Wordstat (несколько фраз), живой SERP по углам отношений.

Запрещено выбирать тему только как «следующий номер серии» из
`published-titles.md` без внешнего спроса.

- Fixer **не** удаляет этот контракт / скрипт / Дзен-канон и **не**
  возвращает ядро к Cursor/AI-скелету.
- Doctor проверяет наличие `shared/topic-focus-contract.md`,
  `shared/dzen-content-rules.md`, `shared/rf-blocked-entities.json` и
  `scripts/excalibur_blog_topic_focus.py`.
