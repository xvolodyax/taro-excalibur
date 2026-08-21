# Референсы лиц — ТАРО СЕЙЧАС

Cover работает в режиме `host_reference`. Файлов лица **в git сейчас нет**.
Пока их нет, Kie i2i для обложки с лицом не запускать.

Не класть ключи и не хостить реф на localhost / 127.0.0.1.

## Куда положить файлы

```text
images/refs/victoria-face.jpg      # лицо Виктории, крупный портрет
images/refs/victoria-waist.jpg     # Виктория поясной кадр
images/refs/alena-face.jpg         # лицо Алёны, крупный портрет
images/refs/alena-waist.jpg        # Алёна поясной кадр
```

Допустимы `.jpg` / `.jpeg` / `.png` / `.webp`. После загрузки скопировать те же файлы в:

```text
memory/cover/assets/victoria-face.jpg
memory/cover/assets/victoria-waist.jpg
memory/cover/assets/alena-face.jpg
memory/cover/assets/alena-waist.jpg
```

Виктория — обложка по умолчанию. Алёна — только если статья про неё.

Реф нужен как **личность лица**, не как костюм и не как эмоция: одежду и выражение на каждой статье менять.

Связанный репо `xvolodyax/taro-content` на 2026-08-21 картинок в git не содержит (только README). Если jpg там в gitignore локально — забери вручную и положи по путям выше, затем повтори Setup Visual.
