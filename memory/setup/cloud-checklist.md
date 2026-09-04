# Cloud checklist — заполняет Setup (блок 0)

Ответы yes/no. **Секреты сюда не писать.**

| Пункт | Статус | Комментарий |
|-------|--------|-------------|
| Репозиторий подключён к Cursor Cloud Environment | pending | |
| Automation Tools → **Memories = OFF** | pending | Official docs: Memories ON by default |
| Secrets: PUBLIC_SITE_URL | pending | |
| Secrets: FTP_HOST / FTP_USER / FTP_PASS / FTP_ROOT | pending | SFTP under FTP_* names |
| MCP Wordstat (если нужен Scout) | yes | folder в tenant-config; ключ в Cloud Secret; MCP-сервер ещё не подключён |
| MCP WordPress blob / image API (если нужны) | pending | optional |
| Image API key (Kie / provider) | pending | optional until Cover |
| Yandex Metrika tokens | pending | optional Content-learner |
| First-run automation = Setup prompt | pending | см. CLOUD-FIRST-RUN.md |
| Daily automation = CLOUD-AUTOMATION.md (после setup) | pending | |
