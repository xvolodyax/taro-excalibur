# Site publish log

## 2026-09-04 B39 on-otpravil-reakciyu-na-istoriyu-i-molchit

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used; Dzen Studio not used)
- article_id: 56
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: **200**
- publish: **200**
- live GET **200** `{{SITE_BASE}}/blog/on-otpravil-reakciyu-na-istoriyu-i-molchit/`
- title/H1: Он отправил реакцию на историю и молчит
- pack: cover.png 16:9 + inline-01/02/03; `figure.cover-hero` нет; обложка один раз как `seo-article__cover`
- «Возьмём:» в теле нет (в related blog-card чужих постов — не трогали)
- лид после H1 один (`p.seo-article__lead` = первый абзац)
- тело не правили после Sol; Дзен Студия не звали
- B21/B22: not touched
- verdict: pass

## 2026-09-04 B38 on-udalil-perepisku-v-otnosheniyah

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used; Dzen Studio not used)
- article_id: 52
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: **200**
- publish: **200**
- live GET **200** `{{SITE_BASE}}/blog/on-udalil-perepisku-v-otnosheniyah/`
- title/H1: Он удалил переписку у обоих и оборвал отношения
- pack: cover.png 16:9 + inline-01/02/03; `figure.cover-hero` нет; обложка один раз как `seo-article__cover`
- «Возьмём:» в теле нет (в related blog-card чужих постов — не трогали)
- лид после H1 один (`p.seo-article__lead` = первый абзац)
- тело не правили после Sol; Дзен Студия не звали
- B21/B22: not touched
- verdict: pass

## 2026-09-03 B35 lichnoe-chislo-ne-zakryvaet-staryj-chat

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used; Dzen Studio not used)
- article_id: 50
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: **200**
- publish: **200**
- live GET **200** `{{SITE_BASE}}/blog/lichnoe-chislo-ne-zakryvaet-staryj-chat/`
- title/H1: Личное число не закрывает старый чат
- pack: cover.png 16:9 + inline-01/02/03; `figure.cover-hero` нет; обложка один раз как `seo-article__cover`
- «Возьмём:» в теле нет (в related blog-card чужих постов — не трогали)
- лид после H1 один (`p.seo-article__lead` = первый абзац)
- тело не правили после Sol; Дзен Студия не звали
- B21/B22: not touched
- verdict: pass

## 2026-09-02 B34 ego-chislo-mesyaca-ne-delaet-shag

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used; Dzen Studio not used)
- article_id: 45
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- approve: **200**
- publish: **200**
- live GET **200** `{{SITE_BASE}}/blog/ego-chislo-mesyaca-ne-delaet-shag/`
- title/H1: Его число месяца не делает шаг за него
- H2 практики в теле; «Возьмём:» в теле нет (в related blog-card чужих постов — не трогали)
- тело не правили; Дзен Студия не звали; ключ не меняли
- B21/B22: not touched
- verdict: pass

## 2026-09-02 B33 live after VPS #16

- POST `/api/admin/content/articles/43/publish` → **200**
- API status `published`, published_at 2026-09-02T12:16:35.508Z, quality 100
- live GET **200** `{{SITE_BASE}}/blog/on-pishet-kazhdyj-den-no-ne-zovet/`
- title/H1: Он пишет каждый день, но не зовёт
- тело не трогали; Дзен Студия не звали; ключ не меняли

## 2026-09-02 B33 resume after VPS #15

- resume `--resume-article-id 43`; approve skipped (`already_approved`, score 100)
- publish 500 EPERM (не EACCES): «Не удалось создать каталог публикации: /var/www/TaroSeoSite/blog/on-pishet-kazhdyj-den-no-ne-zovet (EPERM)»
- live GET 404 `{{SITE_BASE}}/blog/on-pishet-kazhdyj-den-no-ne-zovet/`
- тело не трогали; Дзен Студия не звали; ключ не меняли

## 2026-09-02 B33 on-pishet-kazhdyj-den-no-ne-zovet

- method: site-api (`SITE_PUBLISH_TOKEN`; Hall not used; Dzen Studio not used)
- article_id: 43
- upload: 201
- excerpt_clear: 403 hall_token_no_patch (не FAIL)
- first approve: **200**, `quality_score=100`, warnings `[]` — ложный 409 «нет конкретного примера» в этом прогоне не сработал
- publish: 500 EACCES «Не удалось создать каталог публикации: /var/www/TaroSeoSite/blog/on-pishet-kazhdyj-den-no-ne-zovet»
- resume `--resume-article-id 43`: approve 409 «проверка качества» при API `status=approved` (не example-gate); publish снова 500 тот же EACCES
- live GET: 404 `{{SITE_BASE}}/blog/on-pishet-kazhdyj-den-no-ne-zovet/` и корень `{{SITE_BASE}}/on-pishet-kazhdyj-den-no-ne-zovet/`
- site_status: approved; published_at: null; live_ok: false
- sol_rewritten: no; тело не правили; «Возьмём:» не добавляли
- director_next: needs_human_publish_dir_eacces
- B21/B22: not touched

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
