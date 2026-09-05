# Excalibur-2-Cloud — карта задач

Директор и Setup **не** Task. Цепочка в **одном окне**:
`shared/subagent-chain.md`, модели `shared/pipeline-model-policy.json`.

```text
[S] Setup (чат, inherit) — если !setup_complete
  ├─ блоки 0–7
  ├─ Task: setup-voice   (Gemini 3.8 Flash)
  └─ Task: setup-visual  (inherit)

[Д] Директор (чат, inherit) — только если setup_complete
  ├─ Scout (needs_scout)          inherit
  ├─ shell: today + research_start (+ titles-only)
  ├─ Research (inherit) → Title (Gemini 3.8 Flash) → Writer (Gemini 3.8 Flash)
  │    → Sol (Gemini 3.8 Flash) → Description (Gemini 3.8 Flash)
  ├─ shell: pipeline_canon --stamp + opening_meta + description_gate + html_linter
  ├─ Cover-text (Gemini 3.8 Flash) || Schema (inherit) → Cover (inherit)
  ├─ Indexer (llms only) → Publish                 inherit
  └─ Fixer(open) → merge_to_main → Content-learner inherit
```

## Кто трогает текст

**Правило Владимира 03.09.2026:**
Текстовые роли пишет **только Gemini 3.8 Flash** (`gemini-3.8-flash` + `reasoning_effort=low`; slug `gemini-3.8-flash-high` в Cloud Agents может не существовать — не полагаться на него как единственный путь).
`reasoning_effort=high` — только явный override Владимира.
Запрет fallback на inherit/default для текста. Дефолтный Cloud Agent / Director / Setup НИКОГДА не пишет текст сам — только FAIL. Не трогать Kie/картинки.
Anti-burn: один Writer-проход; нет enricher / Read-loop; после package PASS / site upload ready → EXIT.

| Роль | Проза |
|------|-------|
| **Writer** | Смысл → `drafts/writer.html` (Gemini 3.8 Flash) |
| **Sol** | Слог → финальный `article.html` (+ `drafts/variant-a.html`, Gemini 3.8 Flash) |
| **Title** | Только H1 в brief (Gemini 3.8 Flash) |
| **Description** | Только тизер карточки → `description-brief.json` (не body, Gemini 3.8 Flash) |
| **Cover-text** | Только русские надписи (Gemini 3.8 Flash) |
| **Setup-voice** | SOUL + article-style + examples (Gemini 3.8 Flash) |
| `pipeline_canon --stamp` | meta only, **0** переписки |
| Cover | Только `<figure>` (inherit) |

## Правила

1. Title → `title-brief.json`
2. Writer → `drafts/writer.html`
3. Sol → `article.html` (SOUL + soul-examples; факты из Writer)
4. Description → `description-brief.json` (`shared/dzen-description-rules.md`)
5. `python3 scripts/excalibur_blog_pipeline_canon.py --article-dir … --stamp`
6. Cover-text → Cover; Indexer; Publish
