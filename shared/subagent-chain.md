# Excalibur-2-Cloud — цепочка в одном окне

Канон запуска субагентов после документации Cursor от **2026-08-20**:
[docs/cursor/README.md](../docs/cursor/README.md).
Модели: [pipeline-model-policy.json](pipeline-model-policy.json).

## Одно окно

Daily / First-run **Automation** поднимает **один** Cloud Agent
(Директор или Setup). Это единственный «главный» чат.

Специалисты — **foreground Task** в том же прогоне:

- свой контекст (так устроены subagents Cursor);
- тот же checkout, та же ветка;
- результат возвращается родителю;
- родитель зовёт **следующий** шаг.

Это оркестратор Cursor: planner → specialist → specialist,
а не дерево отдельных Cloud Agent / Agents Window чатов.

## Запрещено (ломает цепочку)

| Действие | Почему нельзя |
|----------|----------------|
| `Task(..., environment="cloud")` | Новый VM + ветка + окно (`/in-cloud`) |
| `/in-cloud`, `/babysit` на шаге пайплайна | Cloud subagent вне цепочки |
| `is_background: true` / `run_in_background: true` | Шаг не блокирует родителя, цепочка рассыпается |
| Isolated worktree / `best-of-n-runner` | Чужой checkout |
| `Task(excalibur-blog-director)` / `Task(excalibur-blog-setup)` | Оркестратор не субагент |
| Специалист вызывает `Task(excalibur-blog-*)` | Вложенный пайплайн (Cursor 2.5 это технически умеет на 1 уровень) |
| Автозапуск skill специалиста в чужой роли | Writer skill на Research → статья без канона |
| Fallback на inherit/default для текстовых ролей | Текст пишет только Gemini 3.8 Flash; fallback запрещён |
| Дефолтный Cloud Agent / Director / Setup пишет текст сам | При недоступности Writer/Title/Sol/Description/Cover-Text — только FAIL |

Единственное вложенное Task: **Setup** → `setup-voice` и `setup-visual`.

Единственная параллель: **Cover-text ∥ Schema** (два foreground Task
в одном сообщении Директора), затем Cover.

## Кто какой моделью (Правило Владимира 03.09.2026)

- **Текст** (заголовки Title / H1, черновик смысла Writer, финальная статья Sol, карточка Дзена description, надписи обложки cover-text, SOUL/article-style setup-voice):
  только **Gemini 3.8 Flash**.
  В Cloud Agents **НЕТ** id `gemini-3.8-flash-high`.
  Дефолт текста: `model: "gemini-3.8-flash"`, `model_params: {"reasoning_effort": "low"}`.
  `reasoning_effort=high` — только явный override Владимира.
  **В эфир с default/inherit Cloud Agent не уходит НИКАКОЙ текст.**
  **Нет Gemini = FAIL.** Дефолтный Cloud Agent / Director / Setup **НИКОГДА** не пишет H1/Title и тело сам.
  Запрещён fallback на inherit/default для текста. При сбое или недоступности модели/субагента — **FAIL ONLY** (только FAIL).
- **Research, Scout, картинки, schema, publish, fixer, indexer, visual setup,
  Директор, Setup:** `model: inherit` — модель **этой** automation /
  выбранная пользователем. Не трогать Kie/картинки.

Если Task **опускает** `model`, runtime часто берёт модель родителя
и может перебить YAML. Поэтому текстовые шаги Директор передаёт явно:
`model: "gemini-3.8-flash"`, `model_params: {"reasoning_effort": "low"}`.
Не-текст: `inherit` или поле не передавать.

## Как Директор вызывает Task

```text
Текстовый шаг:
  subagent_type: excalibur-blog-{title|writer|sol|description|cover-text}
  model: gemini-3.8-flash
  model_params:
    reasoning_effort: low
  run_in_background: false
  (environment не передавать — default local)
  (В Cloud Agents НЕТ id gemini-3.8-flash-high!)
  При недоступности / сбое: FAIL ONLY. Не переключаться на inherit/default, не писать текст самому!

Не-текст:
  subagent_type: excalibur-blog-{scout|research|schema|cover|indexer|publish|fixer|content-learner}
  model: inherit   # или опустить
  run_in_background: false
```

Полный prompt субагенту: входные пути, topic_id, article_dir, что уже
готово, что **не** делать. Субагент не видит историю родителя.

## Skills

Специалист-skills: `disable-model-invocation: true`.
Их читает **свой** агент по пути из `agents/*.md`, а не Auto всего чата.

Директор и Setup остаются auto-skills оркестратора.

## Anti-burn (HARD)

- Writer: **один** проход тела. Нет enricher, нет второго автора, нет Read-loop.
- Не перечитывать gate-скрипты вхолостую после первого PASS.
- После package PASS / site upload ready → **EXIT**. Не ждать следующий цикл.
