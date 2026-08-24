# Cloud checklist — заполняет Setup (блок 0)

Ответы yes/no. **Секреты сюда не писать.**

| Пункт | Статус | Комментарий |
|-------|--------|-------------|
| Репозиторий подключён к Cursor Cloud Environment | yes | Форк `xvolodyax/taro-excalibur`. Этот first-run прогон видит репо. |
| Automation Tools → **Memories = OFF** | yes | Канон тенанта: Memories держать OFF. Docs Cursor: Memories ON by default — выключатель в Automation → Tools обязателен. |
| Secrets: PUBLIC_SITE_URL | no | Публичный бренд: `https://www.таросейчас.рф/`. Live host в git-артефактах статей — только `{{SITE_BASE}}`. Значение секрета в чат/репу не писать. |
| Secrets: FTP_HOST / FTP_USER / FTP_PASS / FTP_ROOT | n/a | WordPress publish **выключен**. В файлы репы не ставить `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes`. |
| MCP Wordstat (если нужен Scout) | no | Нужен. `folderId` каталога Yandex Cloud задан в tenant-config (это не ключ). API-ключ Wordstat — только Cursor Secrets, не git. |
| MCP WordPress blob / image API (если нужны) | n/a | WP blob не используем. Картинки: Kie.ai GPT Image 2. |
| Image API key (Kie / provider) | no | Провайдер: Kie.ai GPT Image 2. Ключ `KIE_API_KEY` — только Cursor Secrets. Не печатать. |
| Yandex Metrika tokens | n/a | Опционально для Content-learner. Сейчас не задаём. |
| First-run automation = Setup prompt | yes | Этот прогон = Setup. Scout / Research / Publish не запускать. |
| Daily automation = CLOUD-AUTOMATION.md (после setup) | yes | После stamp. Публикация в Дзен: **Холл в браузере** (файл с диска). Не WordPress, не localhost / 127.0.0.1. |

## Разница First-run vs Daily

- **First-run (этот прогон):** только Setup. Файлы тенанта. Voice + Visual. Без статей.
- **Daily:** Director → Scout → статья → Cover. Готовые PNG в Дзен грузит человек (Холл) из файлов на диске. Пайплайн WP не включать, пока тенант сам не попросит.
