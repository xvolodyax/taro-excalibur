# Excalibur-2-Cloud — Cloud Automation (Daily)

**Только после** `memory/setup/status.json` → `complete: true`.

Одно окно: эта automation = **Директор**. Не поднимай второй Cloud Agent
на Writer/Sol/Cover (`/in-cloud`, `environment: cloud` запрещены).
Цепочка: `shared/subagent-chain.md`. Модели: `shared/pipeline-model-policy.json`.
Cursor: `docs/cursor/README.md`.

Модель, выбранная в UI automation, идёт на Директора, Research, Scout,
Cover (картинки), Publish. Текст статьи всё равно пишет **Gemini 3.7 Flash**.

## Канон

```text
Scout? → research_start → Research → Title → Writer → Sol
→ Description → Cover-text||Schema → Cover → Indexer → Publish
→ Fixer → merge → Content-learner
```

Writer = смысл (`drafts/writer.html`). Sol = финальный слог тенанта.
Description = тизер карточки ≠ title ≠ opening.

## Automation prompt

```text
Прочитай AGENTS.md + shared/subagent-chain.md + shared/pipeline-model-policy.json
+ shared/pipeline-canon.json + shared/tenant-config.json.
Ты Директор в ЭТОМ окне. Не /in-cloud, не environment:cloud, не isolated worktree.
Специалисты только foreground Task; они не запускают свой пайплайн.
Текст (title/writer/sol/description/cover-text): только Gemini 3.8 Flash High (в Cloud Agents НЕТ id gemini-3.8-flash-high; правильный вызов: Task model gemini-3.8-flash, model_params.reasoning_effort=high).
Запрет fallback на inherit/default для текста. Дефолтный Cloud Agent / Director / Setup НИКОГДА не пишет текст сам при сбое — FAIL only.
Research/scout/schema/cover/indexer/publish/fixer: model inherit. Не трогать Kie/картинки.
Если setup_complete != true — остановись и запусти Setup (см. CLOUD-FIRST-RUN.md).
Игнорируй Automation Memory. Memories в Tools = OFF.

doctor + today.
Если dzen_rf_pack: прочитай shared/dzen-content-rules.md + rf-blocked-entities.json.
needs_scout → Scout (signal_urls из tenant + Wordstat; не RF-DENY heroes).
research_start --topic-id … --title "…".
Research (inherit) → Title (Gemini 3.8 Flash High) → Writer (Gemini 3.8 Flash High) → Sol (Gemini 3.8 Flash High) → Description (Gemini 3.8 Flash High). При недоступности текстовой роли — FAIL only.
shell после Description:
  python3 scripts/excalibur_blog_pipeline_canon.py --article-dir … --stamp
  + opening_meta / description_gate / html_linter.
Cover-text (Gemini 3.8 Flash High) || Schema (inherit) → Cover (inherit); Indexer; Publish; merge; content-learner.
```

Секреты только из Cloud Secrets.
