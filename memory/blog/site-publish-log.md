# Site publish log

## 2026-09-01 B32 on-pishet-tolko-nochyu-dnem-molchit

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 42
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 409 quality_score=88 warning «Нет конкретного примера или разбора ситуации» при H2 практике уже в теле («Как изменить сценарий без драмы и выяснения отношений»)
- publish: not called
- quality GET: 403 hall_token
- verdict: needs_sol
- director_next: false_example_409_no_body_edit
- practice_h2_present: true
- script_practice_h2_detect: false (детектор ищет только «практик»/«чеклист»; H2 сценария не посчитал)
- live_get: 404 `{{SITE_BASE}}/blog/on-pishet-tolko-nochyu-dnem-molchit/`
- root `{{SITE_BASE}}/on-pishet-tolko-nochyu-dnem-molchit/`: 404
- permalink live не выдумывался
- sol_rewritten_by_publish: no
- dzen_studio: not_used
- slot 21:21: not closed
- B21/B22: not touched
- ledger published-titles: quality_review; published-articles: quality_review (not live)

## 2026-09-01 B31 on-otkladyvaet-otnosheniya-na-osen

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 41
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 409 quality_score=88 warning «Нет конкретного примера или разбора ситуации» при H2 практике уже в теле
- publish: 409 «только одобренную»
- quality-pass / PATCH status: 403 hall_token
- verdict: needs_sol
- director_next: false_example_409_no_body_edit
- practice_h2_present: true
- live_get: 404 `{{SITE_BASE}}/blog/on-otkladyvaet-otnosheniya-na-osen/`
- root `{{SITE_BASE}}/on-otkladyvaet-otnosheniya-na-osen/`: 404
- sol_rewritten_by_publish: no
- dzen_studio: not_used
- ledger published-*: quality_review (not live)

## 2026-09-01 B30 on-ne-derzhit-slovo-v-otnosheniyah

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 40
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 409 quality «Сначала статья должна пройти проверку качества»
- publish: not called
- verdict: needs_sol
- director_next: false_example_409_no_body_edit
- practice_h2_present: true
- live_get: 404 `{{SITE_BASE}}/blog/on-ne-derzhit-slovo-v-otnosheniyah/`
- root `{{SITE_BASE}}/on-ne-derzhit-slovo-v-otnosheniyah/`: 404
- sol_rewritten_by_publish: no
- dzen_studio: not_used
- ledger published-*: not updated (not live)

## 2026-08-31 B29 on-stavit-pauzu-vmesto-sblizheniya

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 39
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 409 quality «Сначала статья должна пройти проверку качества»
- publish: not called
- verdict: needs_sol
- director_next: false_example_409_no_body_edit
- practice_h2_present: true
- live_get: 404 `{{SITE_BASE}}/blog/on-stavit-pauzu-vmesto-sblizheniya/`
- sol_rewritten_by_publish: no
- dzen_studio: not_used
- slot 21:21: not closed
- ledger published-*: not updated (not live)

## 2026-08-31 B28 on-obyavilsya-spustya-mesyacy-molchaniya

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used)
- article_id: 38
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: 200
- publish: 500 sitemap EACCES → live_ok
- live_get: 200 `{{SITE_BASE}}/blog/on-obyavilsya-spustya-mesyacy-molchaniya/`
- root `{{SITE_BASE}}/on-obyavilsya-spustya-mesyacy-molchaniya/`: 404 (live канон /blog/)
- live has scene «Привет, как дела?» + «Разберём этот конкретный пример…» + practice H2; no «Возьмём:»; no cover-hero; 3 inline figures
- related `blog-card__` covers ≠ вторая обложка
- sol_rewritten_by_publish: no
- dzen_studio: not_used

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
