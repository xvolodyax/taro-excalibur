# Excalibur-2-Cloud — карта задач

Директор и Setup **не** Task. Цепочка в **одном окне**:
`shared/subagent-chain.md`, модели `shared/pipeline-model-policy.json`.

```text
[S] Setup (чат, inherit) — если !setup_complete
  ├─ блоки 0–7
  ├─ Task: setup-voice   (Gemini 3.8 Flash High)
  └─ Task: setup-visual  (inherit)

[Д] Директор (чат, inherit) — только если setup_complete
  ├─ Scout (needs_scout)          inherit
  ├─ shell: today + research_start (+ titles-only)
  ├─ Research (inherit) → Title (Gemini 3.8 Flash High) → Writer (Gemini 3.8 Flash High)
  │    → Sol (Gemini 3.8 Flash High) → Description (Gemini 3.8 Flash High)
  ├─ shell: pipeline_canon --stamp + opening_meta + description_gate + html_linter
  ├─ Cover-text (Gemini 3.8 Flash High) || Schema (inherit) → Cover (inherit)
  ├─ Indexer (llms only) → Publish                 inherit
  └─ Fixer(open) → merge_to_main → Content-learner inherit
```

## Кто трогает текст

**Правило Владимира 03.09.2026:**
Текстовые роли пишет **только Gemini 3.8 Flash High** (`gemini-3.8-flash` + `reasoning_effort=high`; slug `gemini-3.8-flash-high` в Cloud Agents может не существовать — не полагаться на него как единственный путь).
Запрет fallback на inherit/default для текста. Дефолтный Cloud Agent / Director / Setup НИКОГДА не пишет текст сам — только FAIL. Не трогать Kie/картинки.

| Роль | Проза |
|------|-------|
| **Writer** | Смысл → `drafts/writer.html` (Gemini 3.8 Flash High) |
| **Sol** | Слог → финальный `article.html` (+ `drafts/variant-a.html`, Gemini 3.8 Flash High) |
| **Title** | Только H1 в brief (Gemini 3.8 Flash High) |
| **Description** | Только тизер карточки → `description-brief.json` (не body, Gemini 3.8 Flash High) |
| **Cover-text** | Только русские надписи (Gemini 3.8 Flash High) |
| **Setup-voice** | SOUL + article-style + examples (Gemini 3.8 Flash High) |
| `pipeline_canon --stamp` | meta only, **0** переписки |
| Cover | Только `<figure>` (inherit) |

## Правила

1. Title → `title-brief.json`
2. Writer → `drafts/writer.html`
3. Sol → `article.html` (SOUL + soul-examples; факты из Writer)
4. Description → `description-brief.json` (`shared/dzen-description-rules.md`)
5. `python3 scripts/excalibur_blog_pipeline_canon.py --article-dir … --stamp`
6. Cover-text → Cover; Indexer; Publish
