# Cover host canon — лицо Вики

HARD. Единственный файл рефа лица:

`cover-refs/Виктория.png`  
`memory/cover/assets/Виктория.png` (тот же байтовый канон для Cover)

Имя строго кириллицей, с заглавной **В**. Не `виктория.png`.

## Запрещено (удалить из репо и не заливать в Kie)

- `viktoriaref.png`
- `victoria-sheet.png` / `victoria-sheet-front.png`
- `victoria.png`
- `victoria_ref.jpg` / `victoria_ref.jpeg`
- любой другой face-sheet или чужое лицо

## Кто читает

- `memory/cover/blog-hero.json` → `reference_image`
- `scripts/excalibur_blog_cover_identity_gate.py`
- `scripts/excalibur_blog_cover_quad_prompt.py`
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `scripts/excalibur_blog_hero_reference_url.py`

First-try cover (INC-20260831-0636 + правило 2026-09-09): **ONE** i2i
`gpt-image-2-5-flare-image-to-image` at **2K** from **Виктория.png**,
`Host LARGE left half`, **Victoria age 33**, face fills left.
B14 Cyrillic cover-text **ON** the cover cell + brand line; **no red frame**.
Type / calendar / mug — **RIGHT only**. Type+props cannot replace the host.
Inline: **no Victoria face**. Cover **не** invent второй createTask
из‑за host miss (один owner redo — только по явному запросу).
**Запрещены** четыре отдельные 1K-генерации.

Живые статьи не переписывать и не перерисовывать. Новые обложки — только с этого файла.
