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

## После publish

- Проверить live URL (`/blog/{slug}/`).
- В теле нет второй обложки (`cover-hero` / `cover.png` внутри body figure).
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
