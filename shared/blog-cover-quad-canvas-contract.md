# Blog cover quad canvas contract

> **TENANT-DRIVEN:** palette/hero/style come from Setup Visual (`memory/cover/*`). No personal default brand.

# Excalibur BLOG — Quad Canvas (1 Image API → 4 панели)

Cover-агент работает **после** `article.html` + Writer finalize PASS.

## Главное правило

**Одна** генерация Kie GPT Image 2 Image-to-Image API → один холст `2048×1152` (2×2, каждая панель 16:9) → split в `cover.png` + **ровно три** `inline-01..03.png`. Три inline обязательны: это вторая, третья и четвёртая картинки по явному запросу пользователя.

Prompt должен быть коротким: один общий style-lock + 4 коротких описания квадрантов. Не дублировать длинные style/negative blocks на каждую панель.

Hard gate перед image API:

- `quad-mcp-batch.json` пересобран текущим run, а не взят из старого article artifact
- `validation.prompt_chars <= 3500`
- `reference_url_hosted` — URL тенанта или локальный asset; сторонние временные хосты (catbox и т.п.) запрещены для reference
- `jobs[0].mcp_args.resolution == "2K"`

| Панель | Роль | Герой |
|--------|------|-------|
| **top-left cover** | Один hook 2–6 слов (композиция, не H1 статьи) + один предмет/метафора + воздух | Виктория **всегда в кадре** при `host_reference`: реф только `виктория.png` / `victoria.png`; сверка реф+кадр после gen; одежда и эмоция **каждый раз новые**; без наушников. Не копировать белый пиджак с рефа. Натюрморт без неё запрещён на cover (`shared/cover-host-canon.md`) |
| **3 inline** | Только информация H2: схема / вопрос / сравнение / шаги / факт | людей и лиц нет |

## Workflow

```bash
# 1. Публичный URL эталона (обязательно для i2i)
python scripts/excalibur_blog_hero_reference_url.py

# 2. Manifest: cover_hook + visual_type для inline
python scripts/excalibur_blog_quad_manifest.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --merge

# 3. Промпт + image batch (1 job)
python scripts/excalibur_blog_cover_quad_prompt.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --write-batch

# 4. Kie async image API (PRIMARY Cloud path when KIE_API_KEY is set):
#    Требует env KIE_API_KEY из Cloud Secrets. Не писать ключ в файлы/логи.
#    Скрипт создаёт task через createTask, polling'ом recordInfo ждёт success,
#    затем пишет cover/quad-mcp-result.json с URL.
#    Если KIE_API_KEY задан — НЕ вызывать sync MCP gpt-image-2 первым.
python scripts/excalibur_blog_kie_gpt_image2_api.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>

# 5. Скачать canvas + split
python scripts/excalibur_blog_quad_apply.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --inject-html
```

Legacy MCP fallback: **только если `KIE_API_KEY` отсутствует**. Тогда один вызов
Cursor MCP `gpt-image-2` (или async create/status) с `jobs[0].mcp_args`.
В Cursor Cloud sync MCP 2K i2i часто падает с `-32001 Request timed out`;
без URL/task_id/status tool это `COVER MCP ASYNC BLOCKER`, повторять sync create
вслепую нельзя. Промпты Директора не должны требовать «ONE MCP gpt-image-2»
как primary step.

## Раскладка 2×2

```text
+------------------+------------------+
|  cover (hero)    |  inline_1 (UI)   |
|  top_left        |  top_right       |
+------------------+------------------+
|  inline_2        |  inline_3        |
|  bottom_left     |  bottom_right    |
+------------------+------------------+
```

Split-скрипт в режиме `auto` пробует белые gutters у центра, но **отклоняет** сдвиг, если полоса далеко от x=1024/y=576 или после реза нужен сильный center-crop до 16:9. Fallback — механический 50/50. Форс: `--split-mode mechanical|gutter`. Gutters только на линиях x=1024 / y=576, контент строго внутри квадранта.

## Visual locks

- Palette / hero / style — **только** из Setup Visual (`memory/cover/*`). Нет чужого дефолтного коллажа.
- Background: cover и все inline-панели на чистом белом `#FFFFFF`; запрещены beige/cream/off-white, gray, gradient и grunge full-panel backgrounds.
- Cover при `host_reference`: Виктория всегда в кадре по `shared/cover-host-canon.md` + `blog-hero.json` + один hook (**2–6 слов**, кириллица, не H1 статьи). Реф только `виктория.png` / `victoria.png`. Длинные прямые светлые волосы, зелёные глаза слегка светло-карие, то же лицо. Не брюнетка, не двойник, не Алёна, не шов по лицу. После gen открыть реф и кадр рядом; mismatch — пересобрать весь холст. Натюрморт без неё — только инлайн. Одежда и эмоция **каждый раз новые** — не копировать белый пиджак и выражение с рефа. Подпись кодом: `Виктория - таролог команды «ТАРО СЕЙЧАС»`. Обложку рисует только агент; Холл не перерисовывает. Запрещены all-accent headline и штамп «EXCALIBUR BLOG» (INC-20260723-1223).
- Identity-fail (нет лица / чужое лицо / шов / натюрморт на cover) = HARD reject, новый холст. Это не beauty-redo. Beauty/sticky/style redo по-прежнему запрещён (INC-20260724-2120).
- Не делать фирменным языком: одно белое худи на все кадры, мемные стикеры, скотч / torn paper, кот-герой, слово «лох», тёмный стол, свечи, готика.
- `meme_caption_ru` = `""`.
- Cover `scene_hint` ≈**80–140** chars:
  `<hero lock from blog-hero>; tiny topic metaphor; #FFF`
- Inline: 3–6 labels; без людей и без лиц; смысл / схема / вопрос.
- `reference_url_hosted` — URL тенанта или локальный asset после загрузки рефа. Чужой CDN и localhost запрещены. Пока рефа нет — Cover i2i не запускать.

## Файлы

| Файл | Кто |
|------|-----|
| `memory/cover/blog-hero.json` | `reference_url_hosted` |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `memory/cover/quad-style-*.json` (tenant preset) | **default** style preset |
| `memory/cover/assets/style-refs/` | mood refs тенанта (не чужой plate) |
| `cover/quad-manifest.json` | cover + inline slots |
| `cover/quad-mcp-batch.json` | **1 job**, `input_urls`, `api_args` |
| `cover/kie-image-task.json` | task_id/status прямого Kie API |
| `cover/quad-mcp-result.json` | URL результата (имя legacy, читает apply) |
| `cover/canvas-quad.png` | результат image API |
| `cover/cover.png`, `inline-01..03.png` | split script |
| `cover/cover-registry.json` | split script |

## Editorial-informative code

`memory/cover/cover-design-code.json` +
`memory/cover/quad-style-*.json` (tenant preset из Setup Visual):

- чистый белый `#FFFFFF`, ink и accent из design-code тенанта (не чужой неон-розовый коллаж);
- style refs: `memory/cover/assets/style-refs/` — только тенант, не чужой plate;
- cover интересный за счёт лица, композиции и хука, а не gimmick/meme;
- inline полезен только если объясняет конкретный H2: comparison, workflow, checklist, schema/question или fact card;
- inline в той же палитре, что cover, но **без лиц** и без скотч-коллажа как фирменного языка;
- все Cyrillic labels реально нарисованы; **empty gray placeholder boxes /
  unfinished wireframes = blocker**;
- голый минималистичный SaaS-slide = blocker; заголовок целиком одним accent = blocker;
- во всех inline запрещены герой, люди, лица, мемы и шутки;
- `local_reference` — только локальный asset тенанта после загрузки; не выдумывать URL.

См. `memory/cover/inline-visual-types.json`. Выбор по keywords H2 в `excalibur_blog_quad_manifest.py`.

## Blockers

- `❌ COVER HERO BLOCKER` — нет `reference_url_hosted` или image call без `input_urls`
- `❌ KIE API BLOCKER` — нет `KIE_API_KEY`; non-retryable createTask/recordInfo fail; retryable 500 exhausted; image-fetch File Upload exhausted; sensitive 422 после одного agent soften+recreate; или polling без URL. Первый `failCode=422` sensitive ≠ permanent blocker, пока доступен controlled rewrite. При живом `KIE_API_KEY` не уходить в MCP после 422. После 500×2 / `--max-create-retries` exhausted: Director same-batch re-run Kie script на неизменённом `quad-mcp-batch.json` + Cover apply-only (не quality-redo; B102/B104).
- `❌ COVER MCP TIMEOUT BLOCKER` — image tool вернул повторный timeout, а status/result tool подтверждает failed/no result
- `❌ COVER MCP ASYNC BLOCKER` — sync `gpt-image-2` обрывается по client timeout, а MCP server не даёт `task_id` и отдельный status/result tool для получения позднего URL
- **4 отдельных image jobs** на cover+inline — запрещено
- **quality multi-gen** (host/sticky/style redo после PNG без ошибки Kie API) — запрещено (INC-20260724-2120), **кроме явного запроса владельца/блогера** переделать cover/inline (user-directed quality redo = 1 новый billed gen)
- отсутствует любой из `inline-01.png`, `inline-02.png`, `inline-03.png`
- у inline отсутствует существующий `h2_anchor` или `<figure>` не injected после нужного H2
- inline-панель не объясняет конкретный H2 или содержит людей/лица/мемы
- inline-панель не имеет 3–6 читаемых labels, ясного reading order/outcome
- inline-панель unfinished: empty gray boxes, missing labels, sparse SaaS-slide
  vs dense cover finish
- generated UI выдан за реальный screenshot
- cover или inline имеют beige/gray/grunge/gradient full-panel background вместо чистого белого `#FFFFFF`
- cover содержит мем/gimmick/spam, больше одного hook/предмета либо `meme_caption_ru` не пуст
- cover печатает `cover_keys_ru` как «Ключевые темы» / keyword checklist (keys = metadata only)
- comparison по Cursor SDK / local agent помечает Chat/SDK как «интернет не нужен»
