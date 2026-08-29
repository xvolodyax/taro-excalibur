# SETUP — онбординг тенанта

Агент: **`excalibur-blog-setup`** (чат, не Task).  
Skills: `setup-excalibur-blog`, `setup-voice-excalibur-blog`, `setup-visual-excalibur-blog`.

## Фазы

| Phase | Что спрашиваем | Куда пишем |
|-------|----------------|------------|
| 0 cloud | Environment, Secrets, **Memories OFF**, MCP | `memory/setup/cloud-checklist.md` |
| 1 site | Бренд, ниша, язык, цели | `memory/brief/site-brief.md`, `tenant-config` |
| 2 author | Имя, bio, sameAs | `shared/authors-registry.json` |
| 3 voice | Стиль + примеры (ссылки/файлы/канал) | inbox → Task Voice → SOUL + examples + `article-style.md` |
| 4 visual | Обложки, референсы | inbox → Task Visual → cover configs + assets |
| 5 cta | Ссылки / продукт / «без ссылок» | `tenant-config.cta_*`, `rf-blocked-entities.cta_ok` |
| 6 scout | signal_urls, Wordstat | `tenant-config.scout_signal_urls`, `yandex_cloud_folder_id`, site-brief |
| 7 stamp | Финал | `memory/setup/status.json`, `tenant-config.setup_complete=true` |

## Правила

- Один блок вопросов за раз; дождаться ответа человека.
- Секреты **не** писать в git-файлы.
- Пока `complete=false` — Director не публикует.
- Повторный Setup Voice/Visual допускается (обновление слога/визуала).

## Inbox / log

- Ответы человека (без секретов): `memory/setup/answers.md`
- Тексты/ссылки слога: `memory/setup/voice-inbox/`
- Картинки/референсы: `memory/setup/visual-inbox/` (+ копируются в `memory/cover/assets/`)
