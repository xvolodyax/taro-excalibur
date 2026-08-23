# Pipeline fix queue

## INC-20260823-0630-cover-prefer-local-site-base
status: open
run_date: 2026-08-23
role: excalibur-blog-cover
topic_id: B05
article_dir: memory/blog/articles/B05-chto-on-skryvaet-v-otnosheniyah-i-skazhet-li-pravdu
severity: high
category: script

### What went wrong
- First Kie run failed before createTask: batch `input_urls` keep git-safe `{{SITE_BASE}}`, Cloud env has no `PUBLIC_SITE_URL` / `WP_SITE_URL`, and `batch_mcp_args` required live expand even when `prefer_local_reference` is true.
- Tenant path is local Victoria PNG + File Upload. Catbox is forbidden. No billed task was created.

### How the agent recovered this run
- `expand_input_urls(..., allow_unexpanded=True)` when `prefer_local_reference` is set; File Upload still replaces `input_urls` before createTask.
- Batch file stays git-safe (`{{SITE_BASE}}` / local path). No live host written.

### Durable fix needed before next run
- Keep the skip: prefer_local File Upload must not require a live site URL.
- Document in Kie contract that local-ref tenants can generate without `PUBLIC_SITE_URL`.

### Suggested files to inspect/change
- `scripts/excalibur_blog_kie_gpt_image2_api.py`
- `shared/kie-gpt-image-api-contract.md`
- `tests/test_kie_prefer_local_site_base.py`

### Secrets
- none recorded

### Fixer resolution
- pending
