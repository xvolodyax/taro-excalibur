# Референсы лиц — ТАРО СЕЙЧАС

Cover работает в режиме `host_reference`. На обложках **только Виктория**.
Алёну сюда не класть: в `authors-registry` она лицо бренда, не реф для i2i.

Файлов лица **в git сейчас нет**. Пока их нет, Kie i2i для обложки с лицом не запускать.

Не класть ключи и не хостить реф на localhost / 127.0.0.1.

## Куда положить файлы

Канон (то же, что `memory/cover/blog-hero.json` → `input_urls`):

```text
images/refs/victoria-face.jpg                 # крупный портрет (исходник: victoria_ref.jpg)
images/refs/victoria-sheet.png                # коллаж ~12 кадров, серый фон
images/refs/victoria-character-sheet-2k.png   # лист 8 кадров CLOSE-UP / 3/4 / PROFILE / BACK
```

После загрузки **обязательно** скопировать в форк:

```text
memory/cover/assets/victoria-face.jpg
memory/cover/assets/victoria-sheet.png
memory/cover/assets/victoria-character-sheet-2k.png
```

Допустимы `.jpg` / `.jpeg` / `.png` / `.webp`. Публичный URL после заливки на сайт — только `{{SITE_BASE}}/wp-content/uploads/excalibur/<name>` в `reference_url_hosted`. Не catbox.

## Что даёт реф

- лицо Виктории
- глаза: зелёные + слегка светло-карие у зрачка (не карие, не серые, не голубые)
- волосы: блонд, тёмные корни, пробор посередине

Реф **не** костюм и **не** эмоция. На каждой обложке менять одежду и выражение. Не копировать белый пиджак, камисоль, голубые джинсы, золотую подвеску-дерево, карты в руках.

Связанный репо `xvolodyax/taro-content` на 2026-08-21 картинок в git не содержит (только README). Если jpg лежат локально — положи по путям выше.
