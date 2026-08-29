---
name: publish-excalibur-blog
description: Excalibur BLOG Publish — site API upload/approve/publish after GATE PASS. Hall не заливает.
disable-model-invocation: true
---

# Excalibur BLOG — Publish (субагент ⑥)

**Роль:** `Task(excalibur-blog-publish)`  
**Когда:** сразу после Indexer, после GATE PASS (stamp + opening + description + html_linter + cover).

Контракт: `shared/excalibur-site-publish-contract.md`.

## Канон

После GATE PASS рой **сам** заливает статью. Hall **не** upload / approve / publish.
Ключ есть → publish **не SKIP**. Нет ключа → SKIP «нет ключа», не падать.
Живую **B21** не трогать. В Дзен Студию не ходить — RSS сам.

## Вызов

```bash
python3 scripts/excalibur_blog_site_publish.py --env-check

python3 scripts/excalibur_blog_site_publish.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --dry-run

python3 scripts/excalibur_blog_site_publish.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>
```

Сайт по умолчанию: `https://www.xn--80aaoqxlidb0d.xn--p1ai`  
(override `PUBLIC_SITE_URL` / `--site-base`).

## Env (только Cloud Secret → env)

Первое непустое:

1. `SITE_PUBLISH_TOKEN`
2. `HALL_PUBLISH_TOKEN`
3. `PUBLISH_TOKEN`
4. `TARO_SITE_TOKEN`

Header: `Authorization: Bearer …` или `X-Publish-Token`.
Значение ключа не писать в git / лог / отчёт.

## tgz

`article.html` + `article.meta.json` + `description-brief.json` +
`cover/{cover,inline-01,inline-02,inline-03}.png`

Перед упаковкой вырезать `figure.cover-hero`. `cover.png` только файл обложки.
В теле три врезки. После publish — live URL, нет второй обложки, `t.me` на месте
(если сайт сменил на `/rasklad-taro-online/` — вернуть).

## Нет ключа

```text
gate: PASS
publish: SKIP
reason: нет ключа
exit: 0
```

## Handoff

```text
=== EXCALIBUR BLOG PUBLISH ===
topic_id:
slug:
article_dir:
verdict: PASS|SKIP|FAIL
publish: PUBLISHED|SKIP
reason:
permalink:
blockers:
```

SKIP «нет ключа» — не BLOCKER. FAIL upload/live — BLOCKER без PIPELINE DONE.

## Запрещено

- Писать или переписывать longread (кроме restore `t.me`)
- Hall / админка сайта вместо скрипта
- Дзен Студия
- Трогать живую B21
- Печатать токен
