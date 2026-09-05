# Модели для субагентов (обновлено 2026-09-03)

Источники:

- https://cursor.com/docs/subagents.md#model-configuration
- https://cursor.com/docs/models-and-pricing
- https://cursor.com/docs/models/gemini-3-8-flash

## Pin vs inherit

| YAML / Task `model` | Поведение |
|---------------------|-----------|
| `inherit` | Модель родителя = модель automation / чата |
| конкретный ID | Всегда эта модель (если план/админ не блокирует) |

Если Task **опускает** `model`, в Cloud Agent runtime субагент часто
берёт модель **родителя**, даже если YAML другой. Поэтому Директор
**явно** передаёт модель Gemini на текстовые шаги.

## Gemini 3.8 Flash (Правило Владимира 03.09.2026)

Текстовые роли пишет **только Gemini 3.8 Flash**:

- В Cloud Agents **НЕТ** id `gemini-3.8-flash-high`.
- Дефолт текста: `model: "gemini-3.8-flash"`, `model_params: {"reasoning_effort": "low"}`.
- `reasoning_effort=high` — только явный override Владимира.

Это модель строго для всех текстовых ролей:

- Title (H1 / title)
- Writer (смысл, заголовки H2, черновик)
- Sol (финальная проза)
- Description (тизер карточки)
- Cover-text (русские надписи)
- Setup Voice (SOUL, article-style, examples)

Gemini 3 Pro Image / image preview — **не** текстовые роли.
Картинки Cover идут через Kie/MCP на inherit-агенте `excalibur-blog-cover` (не трогай Kie/картинки).

## Что остаётся на модели automation

Scout, Research, Schema, Cover (генерация изображений), Indexer, Publish, Fixer,
Content-learner, Setup, Setup Visual, сам Директор.

Владелец ставит Grok / Composer / Opus в automation — research и публикация
идут на неё. Текст статьи всё равно Gemini 3.8 Flash.

## Fallback: СТРОГО ЗАПРЕЩЁН ДЛЯ ТЕКСТА (FAIL ONLY)

- **Запрет fallback на inherit/default для текста.** Никакого переключения на inherit или дефолтную модель родителя.
- **Дефолтный Cloud Agent / Director / Setup НИКОГДА не пишет тело статьи, H1, Sol, description, cover-text сам**, если Writer/Title/Sol/Description/Cover-Text недоступны или при сбое.
- **FAIL ONLY:** При любой ошибке вызова Gemini 3.8 Flash или недоступности текстового субагента — останавливаться с явным FAIL. Никакого текста своими силами.
