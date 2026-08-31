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
| **top-left cover** | Один hook + один предмет/метафора + воздух | reference host обязателен: естественная уверенная эмоция, белое плотное худи, без наушников |
| **3 inline** | Только информация H2: comparison table, workflow, checklist, UI explanation, fact card | людей и лиц нет |

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

Типографика, герой, палитра — **только** из tenant `memory/cover/cover-design-code.json` +
`blog-hero.json` + `quad-style-*.json`. Нет дефолта «bold condensed Cyrillic»,
`#FF1493`, белого худи или кота без лица.

- Background: cover и все inline-панели на чистом белом `#FFFFFF`, если tenant
  не задал иное; запрещены gray, gradient и grunge full-panel backgrounds.
- **Герой:** из `blog-hero.json` `cover_mode`. `host_reference` = лицо рефа
  (для ТАРО СЕЙЧАС — Виктория). Не подставлять кота и не убирать лицо.
  Цвет волос копируется с рефа (`hair_color_lock.prompt`). Платина / ice-blonde /
  осветление = `COVER IDENTITY BLOCKER`, пересобрать холст.
  Gate: `python3 scripts/excalibur_blog_cover_identity_gate.py --article-dir …`
- **Хук:** editorial display из `typography.hook_prompt` (журнальный кириллический:
  high-contrast modern serif / didone **или** refined geometric grotesque,
  нормальный трекинг). Буквы часть кадра, не стикер. Одно ударное слово —
  та же гарнитура, цвет `accent_primary` (золото медальона, не розовый).
- **Вторичные подписи** (sticky, inline labels): лёгкий humanist sans из
  `typography.secondary_prompt`. Не системный UI-шрифт.
- **Запрещено в промптах и design-code:** Arial, Roboto, Inter, Impact, Times,
  «обычный жирный», default bold condensed, squish-bold meme, all-caps плашка
  как наклейка. Кривые буквы / разный кегль в одном слове = blocker, пересобрать
  холст.
- Подпись credit (`cover_credit_html`) — кодом поверх, не моделью.
- `meme_caption_ru` = `""`. Запрещён штамп «EXCALIBUR BLOG» (INC-20260723-1223).
- Cover `scene_hint` ≈**80–140** chars:
  `Host LARGE left half, same woman as Виктория.png, face fills left; tiny <topic object> RIGHT only; #FFF`
- Inline: 3–6 labels; без людей и лиц.

## Файлы

| Файл | Кто |
|------|-----|
| `memory/cover/blog-hero.json` | `reference_url_hosted` |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `memory/cover/quad-style-*.json` (tenant preset) | **default** style preset |
| `memory/cover/assets/style-refs/` | Pinterest mood refs + 16:9 moodboard |
| `cover/quad-manifest.json` | cover + inline slots |
| `cover/quad-mcp-batch.json` | **1 job**, `input_urls`, `api_args` |
| `cover/kie-image-task.json` | task_id/status прямого Kie API |
| `cover/quad-mcp-result.json` | URL результата (имя legacy, читает apply) |
| `cover/canvas-quad.png` | результат image API |
| `cover/cover.png`, `inline-01..03.png` | split script |
| `cover/cover-registry.json` | split script |

## Editorial-informative code

`memory/cover/cover-design-code-cat-digital-collage.json` +
`memory/cover/quad-style-*.json` (tenant preset)
(legacy editorial without cats:
legacy example name — use tenant preset):

- clean white base `#FFFFFF`, ink `#141821`, accent и typeface — из tenant
  design-code (ТАРО: золото медальона, пыльные летние тона, editorial display);
- style moodboard: `memory/cover/assets/style-refs/` если tenant положил;
- cover интересный за счёт композиции, масштаба и метафоры, а не gimmick/meme;
- inline полезен только если объясняет конкретный H2: comparison table, workflow, checklist, UI explanation или fact card;
- **inline = тот же finished язык, что cover** (свет / золото / humanist sans).
  Не «недоделанный» каркас рядом с жирной обложкой;
- все Cyrillic labels реально нарисованы; **empty gray placeholder boxes /
  unfinished wireframes = blocker**;
- схема может быть чистой по структуре, но обязана оставаться в фирменном
  языке тенанта. Голый минималистичный SaaS-slide = blocker;
  all-caps плашка-наклейка = blocker; bold condensed как дефолт = blocker;
- во всех inline запрещены герой, люди, лица, мемы и шутки;
- `local_reference` / style plate = finished sample (mood quality bar),
  не geometric color blocks.

См. `memory/cover/inline-visual-types.json`. Выбор по keywords H2 в `excalibur_blog_quad_manifest.py`.

## Blockers

- `❌ COVER HERO BLOCKER` — нет `reference_url_hosted` или image call без `input_urls`
- `❌ COVER IDENTITY BLOCKER` — нет hair lock phrase в промпте, или волосы платина / ice-blonde / сильно светлее рефа. Пересобрать холст, не чинить волосы снаружи. Gate: `excalibur_blog_cover_identity_gate.py`
- `❌ KIE API BLOCKER` — нет `KIE_API_KEY`; non-retryable createTask/recordInfo fail; retryable 500 exhausted; image-fetch File Upload exhausted; sensitive 422 после одного agent soften+recreate; или polling без URL **после** late-poll + `--resume` (job already terminal fail, not still-generating). Первый `failCode=422` sensitive ≠ permanent blocker, пока доступен controlled rewrite. При живом `KIE_API_KEY` не уходить в MCP после 422. После 500×2 / `--max-create-retries` exhausted: Director same-batch re-run Kie script на неизменённом `quad-mcp-batch.json` + Cover apply-only (не quality-redo; B102/B104).
- `❌ KIE POLL WINDOW EXHAUSTED` (exit 2) — job всё ещё `waiting`/`generating` после `--max-wait` + late-poll extend. **Не** новый create и **не** 500×2 path. Cover: `--resume` / `--task-id` тот же job. Late 500 → script max-1 recreate. Recreate poll: `--max-create-retries 0` (INC-20260831-1508 / B28).
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
