# Cloud checklist — заполняет Setup (блок 0)

Ответы yes/no. **Секреты сюда не писать.**

| Пункт | Статус | Комментарий |
|-------|--------|-------------|
| Репозиторий подключён к Cursor Cloud Environment | yes | Этот прогон = First-run Cloud Agent |
| Automation Tools → **Memories = OFF** | desired | Владелец: Memories OFF **желательны**. Docs: ON by default. Игнорировать Automation Memory |
| Secrets: PUBLIC_SITE_URL | yes | Публичный URL, не секрет. Значение не дублируем как «секрет» |
| Secrets: FTP_HOST / FTP_USER / FTP_PASS / FTP_ROOT | n/a | Публикацию на сайт/Дзен делает Hall, не этот пайплайн |
| MCP Wordstat (если нужен Scout) | yes | Ключ уже снаружи. Scout зовёт Wordstat сам, внешнего агента нет |
| MCP WordPress blob / image API (если нужны) | n/a | Hall публикует. Image = Kie, не WP blob |
| Image API key (Kie / provider) | yes | Kie уже в секретах снаружи. В git не класть |
| Yandex Metrika tokens | n/a | Не запрошены; Content-learner опционален |
| First-run automation = Setup prompt | done | Setup закрыт 2026-08-29. Анкету не задавать. |
| Daily automation = CLOUD-AUTOMATION.md (после setup) | yes | `setup_complete: true`. Вечерний слот пишет Director + site publish. |

Новых Secrets у человека не просили.
