---
name: wechat-official-draft
description: Create stable WeChat Official Account drafts from Markdown articles using a simple inline-HTML layout and the official WeChat draft APIs. Use when asked to format, preview, upload images, create a WeChat draft, push to a WeChat Official Account draft box, or publish Markdown/blog/article content without relying on md2wechat conversion paths.
---

# WeChat Official Draft

## Overview

Use this skill to turn Markdown articles into WeChat Official Account drafts with a simple, stable layout. The default formatter favors compatibility over visual complexity: inline styles, readable headings, clean paragraphs, blockquotes, code blocks, local image upload, and a cover image.

The bundled script uses official WeChat APIs directly:

- `cgi-bin/token`
- `cgi-bin/media/uploadimg` for inline article images
- `cgi-bin/material/add_material` for the cover
- `cgi-bin/draft/add` for draft creation

## Credentials

Default config source:

```text
~/.config/wechat-official-draft/config.yaml
```

Read only:

```yaml
wechat:
  appid: ...
  secret: ...
```

Do not print or echo `secret`. It is acceptable to mention that credentials are present or missing.

Alternative credentials can be passed through environment variables:

```bash
WECHAT_APPID=...
WECHAT_SECRET=...
```

Initialize config:

```bash
node "$HOME/.codex/skills/wechat-official-draft/scripts/push_draft.mjs" \
  init \
  --appid "your_wechat_appid" \
  --secret "your_wechat_appsecret"
```

The init command creates `~/.config/wechat-official-draft/config.yaml` with file mode `600`.

## Quick Start

Create a draft:

```bash
node "$HOME/.codex/skills/wechat-official-draft/scripts/push_draft.mjs" \
  --file article.md \
  --title "文章标题" \
  --digest "128 字以内摘要" \
  --cover cover.png
```

Generate local preview HTML without calling WeChat:

```bash
node "$HOME/.codex/skills/wechat-official-draft/scripts/push_draft.mjs" \
  --file article.md \
  --title "文章标题" \
  --cover cover.png \
  --dry-run
```

## Workflow

1. Inspect the Markdown article.
2. Ensure the WeChat metadata is valid:
   - `title` must be 32 characters or fewer.
   - `digest` must be 128 characters or fewer.
   - A cover image is required for draft creation.
3. Use `--dry-run` first when the user asks to preview formatting.
4. Create the draft only when the user asks to push, upload, publish, or create a WeChat draft.
5. Report the draft `media_id`, saved JSON response path, and preview path if created.

## Layout Principles

Keep the formatter simple and extensible:

- Use inline styles only.
- Prefer a single constrained content column.
- Keep paragraphs readable with 16px text and generous line-height.
- Render Markdown headings, paragraphs, lists, blockquotes, fenced code, inline code, bold text, and images.
- Upload local Markdown images to WeChat and replace them with returned URLs.
- Do not use external CSS, JavaScript, local file paths in the final content, or unsupported WeChat editor features.

Future template extensions should be added behind script options or small reference files, not by changing the core publish workflow.

## Failure Handling

- If token retrieval fails with an IP whitelist error (`errcode` 40164), tell the user the blocked IP from the error message and ask them to add it at <https://developers.weixin.qq.com/platform?tab1=basicInfo&tab2=dev> (WeChat Official Account backend → 设置与开发 → IP 白名单). The script also prints this link in its `hint` field.
- If image upload fails, check local file existence and image size/type first.
- If draft creation fails with title/digest/content errors, shorten metadata or simplify HTML.
- If credentials are missing, ask the user to configure `WECHAT_APPID` / `WECHAT_SECRET` or the config file above.

## Resources

- Use `scripts/push_draft.mjs` for preview and draft creation.
- Read `references/wechat-api-notes.md` only when debugging WeChat API errors or extending the script.
