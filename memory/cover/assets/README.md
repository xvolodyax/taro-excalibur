# Cover assets — ТАРО СЕЙЧАС

Сюда Setup Visual / Cover кладут реф **только Виктории** для i2i.

## Сейчас: need upload

Лиц в git нет. `blog-hero.json` → `status: NEED_MORE_REFS`, `assets_status: need_upload`.
`reference_url_hosted` пустой. Не выдумывать URL на чужой CDN.

Не запускать Cover i2i, пока не лежат:

```text
memory/cover/assets/victoria-face.jpg
memory/cover/assets/victoria-sheet.png
memory/cover/assets/victoria-character-sheet-2k.png
```

Алёну в эту папку не класть.

`input_urls` в `blog-hero.json` = эти два файла. Kie берёт локальный файл через `prefer_local_reference` + File Upload (ключ только в Cursor Secrets). Публичный URL после заливки — `{{SITE_BASE}}/wp-content/...`. Не catbox, не localhost.

Реф = лицо и глаза. Одежду и эмоцию на каждой статье менять.
Глаза: зелёные + слегка светло-карие у зрачка.

В Дзен готовые PNG грузить файлом с диска, не с localhost.
