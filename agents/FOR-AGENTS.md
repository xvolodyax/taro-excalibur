# Excalibur-2-Cloud — субагенты

Карта: `shared/pipeline-task-map.md`  
Цепочка: `shared/subagent-chain.md`  
Модели: `shared/pipeline-model-policy.json`  
Доки Cursor: `docs/cursor/README.md`

Одно окно: Setup или Директор = главный чат. Специалисты = foreground Task.
Не `/in-cloud`, не `environment: cloud`. Специалист не зовёт `Task(excalibur-blog-*)`.

## Директор и Setup (не Task)

| Роль | Файл | Skill | Модель |
|------|------|-------|--------|
| Setup (первый запуск) | `excalibur-blog-setup.md` | `setup-excalibur-blog` | inherit (automation) |
| Директор (пайплайн) | `excalibur-blog-director.md` | `director-excalibur-blog` | inherit (automation) |

## Субагенты (Task)

| # | Task | Роль | Модель |
|---|------|------|--------|
| S1 | setup-voice | SOUL + examples + article-style | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| S2 | setup-visual | cover configs + assets | inherit |
| 🔍 | scout | Тема | inherit |
| ① | research | Facts | inherit |
| ①b | title | H1 | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| ② | writer | Смысл → `drafts/writer.html` | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| ②b | **sol** | **Финал `article.html` (слог SOUL)** | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| ②c | **description** | **Дзен/RSS карточка → `description-brief.json`** | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| ④a | cover-text | RU надписи | **Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`) |
| ④b | schema | JSON-LD | inherit |
| ④c | cover | Image API + figures | inherit |
| ⑤ | indexer | llms | inherit |
| ⑥ | publish | WP | inherit |
| ⑦ | fixer | Incidents | inherit |
| ⑦b | content-learner | Metrika | inherit |

**Правило Владимира 03.09.2026 + anti-burn 05.09.2026:**
Текстовые роли пишет только Gemini 3.8 Flash. В Cloud Agents: `gemini-3.8-flash` + `reasoning_effort=low`. `high` — только явный override Владимира. Slug `gemini-3.8-flash-high` в Cloud Agents может не существовать — не полагайся на него как единственный путь.
Строгий запрет fallback на inherit/default для текста. Дефолтный Cloud Agent / Director / Setup НИКОГДА не пишет текст сам (только явный FAIL). Не трогать Kie/картинки.
Один Writer-проход. Нет enricher / Read-loop. После package PASS / site upload ready → EXIT.

После **Sol** → **Description** → shell `pipeline_canon --stamp` +
opening_meta / description_gate / html_linter.

Пока setup не complete — только Setup (+ setup-voice/visual).
