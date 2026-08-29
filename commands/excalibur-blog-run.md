---
description: Excalibur-2-Cloud — живой прогон статьи через оркестратор и субагентов.
---

# Excalibur-2-Cloud — запуск пайплайна

Сначала: `memory/setup/status.json` → `complete: true`. Иначе — Setup.

«Запусти Excalibur для темы **B01**»

Это **одно окно Директора**. Не `/in-cloud`. Специалисты — foreground Task.
Текст и промпт картинки: Gemini 3.7 Flash. Research/publish: модель automation. Пиксели: Kie.

## Параметры

- `topic_id`: B01 | all | P0-only
- `publish`: yes | no (default yes)

## Пайплайн

```text
Scout? → Research → Title → Writer → Sol → Description → Cover||Schema
→ Indexer → Publish
```

Writer / Sol / Title / Description / Cover-text / Scout-title / Cover-prompt / Setup-visual — Gemini 3.7 Flash.
Research / Schema / Publish — модель automation. Пиксели Cover — Kie. Не читать тела старых статей.
Publish BLOCK без setup / без pipeline_canon stamp.

Оркестратор: `skills/director-excalibur-blog/SKILL.md`.
