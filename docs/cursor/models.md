# Модели для субагентов (выжимка, 2026-08-20)

Источники:

- https://cursor.com/docs/subagents.md#model-configuration
- https://cursor.com/docs/models-and-pricing
- https://cursor.com/docs/models/gemini-3-7-flash

## Pin vs inherit

| YAML / Task `model` | Поведение |
|---------------------|-----------|
| `inherit` | Модель родителя = модель automation / чата |
| конкретный ID | Всегда эта модель (если план/админ не блокирует) |

Если Task **опускает** `model`, в Cloud Agent runtime субагент часто
берёт модель **родителя**, даже если YAML другой. Поэтому Директор
**явно** передаёт `gemini-3.7-flash-high` на текстовые шаги.

## Latest Gemini (каталог 2026-08-20)

В публичном каталоге Cursor не hidden: **Gemini 3.7 Flash**
(`gemini-3.7-flash`). Task slug с effort high:
`gemini-3.7-flash-high`.

Это модель для:

- Scout (короткий title в handoff; Wordstat — отдельный API)
- Title (H1 / title)
- Writer (смысл, заголовки H2, черновик)
- Sol (финальная проза)
- Description (тизер карточки)
- Cover-text (русские надписи)
- Cover (scene_hint, hook, alt, промпт холста/inline)
- Setup Voice (SOUL, article-style, examples)
- Setup Visual (prompt_fragment и prompt blocks)

Gemini 3 Pro Image / image preview — **не** текстовые роли.
Пиксели Cover идут через Kie/MCP (`gpt-image`), не через Gemini.

## Что остаётся на модели automation

Research, Schema, Indexer, Publish, Fixer, Content-learner,
Setup (чат), сам Директор.

Владелец ставит Grok / Composer / Opus в automation — research и публикация
идут на неё. Текст и промпт картинки всё равно Gemini.

## Fallback

Админ команды / план / legacy Max Mode могут подменить модель.
Если текст внезапно не Gemini — смотри план и
https://cursor.com/docs/subagents.md#why-is-my-subagent-using-a-different-model
