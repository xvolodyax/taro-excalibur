# Excalibur-2-Cloud — Cloud Automation (Daily)

**Только после** `memory/setup/status.json` → `complete: true`.

Одно окно: эта automation = **Директор**. Не поднимай второй Cloud Agent
на Writer/Sol/Cover (`/in-cloud`, `environment: cloud` запрещены).
Цепочка: `shared/subagent-chain.md`. Модели: `shared/pipeline-model-policy.json`.
Cursor: `docs/cursor/README.md`.

Модель, выбранная в UI automation, идёт на Директора, Research, Schema,
Publish. Текст и промпт картинки пишет **Gemini 3.7 Flash**. Пиксели — Kie.

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
Текст и промпт (scout/title/writer/sol/description/cover-text/cover/setup-visual): Task model gemini-3.7-flash-high.
Research/schema/indexer/publish/fixer: model inherit. Пиксели Cover — Kie, не Gemini.
Если setup_complete != true — остановись и запусти Setup (см. CLOUD-FIRST-RUN.md).
Игнорируй Automation Memory. Memories в Tools = OFF.

doctor + today.
Если dzen_rf_pack: прочитай shared/dzen-content-rules.md + rf-blocked-entities.json.
needs_scout → Scout Gemini (signal_urls из tenant + Wordstat API; не RF-DENY heroes).
research_start --topic-id … --title "…".
Research (inherit) → Title (Gemini) → Writer (Gemini) → Sol (Gemini) → Description (Gemini).
shell после Description:
  python3 scripts/excalibur_blog_pipeline_canon.py --article-dir … --stamp
  + opening_meta / description_gate / html_linter.
Cover-text (Gemini) || Schema (inherit) → Cover (Gemini prompt, Kie pixels); Indexer; Publish; merge; content-learner.
```

Секреты только из Cloud Secrets.
