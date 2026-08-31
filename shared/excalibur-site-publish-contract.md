# Excalibur — заливка на сайт (рой, не Hall)

После **GATE PASS** рой **сам** заливает статью на сайт.
Hall **не** вызывает upload / approve / publish.

## Сайт

Канон: `https://www.xn--80aaoqxlidb0d.xn--p1ai`  
(override: `PUBLIC_SITE_URL` / `--site-base`, без записи live-host в git-артефакты).

## Вызов

```bash
python3 scripts/excalibur_blog_site_publish.py --env-check

python3 scripts/excalibur_blog_site_publish.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --dry-run

python3 scripts/excalibur_blog_site_publish.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>
```

Директор после Indexer: `Task(excalibur-blog-publish)` → этот скрипт.
**Если ключ есть — publish не SKIP.** Нет ключа — GATE PASS + publish SKIP
«нет ключа», пайплайн **не** падает.

## Секрет

Токен **только** из env / Cursor Cloud Secret. Имена по очереди:

1. `SITE_PUBLISH_TOKEN`
2. `HALL_PUBLISH_TOKEN`
3. `PUBLISH_TOKEN`
4. `TARO_SITE_TOKEN`

В git, лог, stdout, handoff и `*-result.json` значение ключа **не** писать.
Не читать токен из `memory/site.env.local` и не просить его в чат.

## HTTP

Header: `Authorization: Bearer <token>` **или** `X-Publish-Token: <token>`
(скрипт шлёт оба).

1. `POST /api/admin/content/excalibur/upload` — multipart field `tgz`
   (файл `article.tgz`).
2. `POST /api/admin/content/articles/{id}/approve`
3. `POST /api/admin/content/articles/{id}/publish`

## Состав tgz

```text
article.html
article.meta.json
description-brief.json
cover/cover.png
cover/inline-01.png
cover/inline-02.png
cover/inline-03.png
```

`article.html` для сайта:

- **нет** `figure.cover-hero` (если есть — вырезать **перед** tgz, диск
  `article.html` не обязательно менять);
- `cover.png` только файл обложки, не вторая картинка в теле;
- в теле ровно три врезки (`inline-01`…`03` / `data-slot="inline_1"`…).
- **HARD (29.08):** тема всегда печатает `excerpt` как `p.seo-article__lead`
  под H1. В tgz `article.meta.json` поле `excerpt` **пустое** (не копия
  первого `<p>`). После upload скрипт PATCH `excerpt=""`. Лид живёт только
  в теле. `description` / RSS — карточка Дзена, не dek под H1.

## Ограничения сайта (B23 / B24 / B26) — не лечить телом статьи

Сайт **игнорирует** `skip_quality_review` / `auto_approve` в meta.
Это не повод править opening. Чекер качества живёт **вне этого репо**.
У него **два разных** warning, их нельзя склеивать:

- «Нет практического блока (практика / шаги / чеклист)» — нужен H2
  «Практика: чеклист шагов…» из маркеров **этой** статьи. Пишут Writer/Sol
  **до** первого upload (вечерний слот). Не «Возьмём:».
- «Нет конкретного примера или разбора ситуации» ≠ часы
  «конкретный пример: ЧЧ:ММ» и ≠ шаблон B23 (H2 «Разбор ситуации»
  + по минутам).
  Хватает сцены из research и фразы вроде «Разберём этот конкретный
  пример…» из фактов статьи. Не копировать opening B23/B25.

Publish после **GATE PASS** **не** переписывает opening Sol ради score.

- **Hall / SITE token не PATCH excerpt.** И `SITE_PUBLISH_TOKEN`, и
  `HALL_PUBLISH_TOKEN` на `PATCH excerpt=""` получают **403**. Это
  **не** FAIL: тема печатает первый `<p>` как `p.seo-article__lead`.
  Скрипт пишет `excerpt_clear_skipped=hall_token_no_patch` и идёт
  дальше. Не откатывать live из‑за двойного лида, который нельзя снять.
- **sitemap EACCES + live 200 = `live_ok`.** `POST …/publish` может
  ответить **500** «Не удалось обновить sitemap.xml (EACCES)», при этом
  статья уже на сайте (`GET` permalink **200**). Не FAIL, не retry
  телом статьи. Скрипт: `publish_sitemap_skipped=eacces`.
- **Related `blog-card` cover ≠ вторая обложка.** Карточки «ещё
  почитать» (`figure.blog-card__media` / любой `blog-card__*`) берут
  чужой `/{other-slug}/cover.png` внутри `<article>`. Live-gate это
  **не** считает второй обложкой этого поста. Настоящая вторая обложка —
  extra `cover.png` figure **без** `seo-article__cover` и **без**
  `blog-card__`.
- **Quality 409 нельзя лечить ярлыком.** Approve **409** «Сначала
  статья должна пройти проверку качества» **не** чинится словами
  «Возьмём:» / «Возьмем:» / «Сцена». Эти ярлыки запрещены
  (`shared/article-style.md`, `shared/SOUL.md`). Не копировать шаблон
  B23 (H2 «Разбор ситуации» + разбор по минутам) в новую статью.
- **Первый quality 409 ≠ PIPELINE FAIL.** Скрипт пишет
  `verdict=needs_sol`, exit 2. `director_next`:
  - нет H2 практика/чеклист → `return_sol_practice` (Sol пишет практику
    из фактов этой статьи, затем новый POST, не `--resume-article-id`);
  - практика уже в теле (B27) → `false_example_409_no_body_edit`.
    **Не** слать Sol на вставку «Возьмём:» / «например» / «кейс».
    В репо **нет** гейта «конкретный пример». Сайт слог не бракует.
    Не помечать «починили сайт». Publish **не** правит тело.
  Writer/Sol заранее кладут живую сцену в лид (без «Возьмём:»).
- **Утренний слот ≠ вечерние часы B23.** Не ставить в opening чужие
  часы/день: «суббота, 20:40» из B23 не принадлежит утреннему прогону.
  Ситуация — только из research / Writer / Sol **этой** статьи.
- **Resume 409 на already-live.** Повторный approve/publish уже
  живой статьи снова даёт 409 (quality / «уже опубликована»), даже
  когда `status=published`. При `--resume-article-id` скрипт не FAIL:
  идёт к live GET.

## После publish

- Проверить live URL (`/blog/{slug}/`).
- В теле нет второй обложки (`cover-hero` / extra `cover.png` figure
  без `seo-article__cover` и без `blog-card__`).
- `t.me` **не** переписывать на `/rasklad-taro-online/`.
  Если сайт переписал — вернуть исходные `t.me` (PATCH статьи) и перепроверить.

## Запреты

- Дзен Студия: **не ходить**. RSS сам (`/blog/rss.xml`).
- Живые **B21** и **B22** не трогать (upload / approve / publish / PATCH — отказ).
- Не заменять Hall-ручной approve в админке: это делает скрипт.

## Нет ключа

```text
gate: PASS
publish: SKIP
reason: нет ключа
exit: 0
```

## Артефакт

`site-publish-result.json` (verdict `pass` | `skip` | `fail`, permalink как
`{{SITE_BASE}}/blog/{slug}/`, без секрета).
