# Site publish log

## 2026-08-31 B27 on-ne-obsuzhdaet-buduschee-vashih-otnoshenij

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- first upload: 201 article_id 37 version 1 → approve 409 quality_score 88 warning «Нет конкретного примера…»; needs_sol; тело не правили
- second POST upload (no `--resume-article-id`): 201 same id 37 version 2 (новое тело: «Разберём этот конкретный пример…» в лиде)
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 200
- publish: 500 sitemap EACCES → live_ok
- quality_score: 100
- quality_warnings: none
- live_get: 200 `{{SITE_BASE}}/blog/on-ne-obsuzhdaet-buduschee-vashih-otnoshenij/`
- root `{{SITE_BASE}}/on-ne-obsuzhdaet-buduschee-vashih-otnoshenij/`: 404 (live канон /blog/)
- live has example sentence + practice H2; no «Возьмём:»; no cover-hero
- sol_rewritten_by_publish: no
- dzen_studio: not_used

## 2026-08-30 B26 on-skazal-chto-ne-gotov-k-otnosheniyam

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 36
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 200
- publish: 500 sitemap EACCES → live_ok
- live_get: 200
- permalink: {{SITE_BASE}}/blog/on-skazal-chto-ne-gotov-k-otnosheniyam/
- sol_rewritten: practice checklist H2 after first 409; no «Возьмём:»; no B23 clock template
- dzen_studio: not_used
- slot 21:21: not closed

## 2026-08-30 B25 ty-vidish-izmenu-v-ego-pauze

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 34
- version: 4
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 200
- publish: 500 sitemap EACCES → live_ok
- quality_score: 100
- live_get: 200
- permalink: {{SITE_BASE}}/blog/ty-vidish-izmenu-v-ego-pauze/
- sol_rewritten: no
