# WeChat API Notes

## Endpoints

- Access token: `GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=...&secret=...`
- Inline image: `POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=...`
- Cover image material: `POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=...&type=image`
- Draft create: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=...`

## Common Errors

- `40164`: caller IP is not in the official account IP whitelist.
- `40001` / `42001`: invalid or expired token; refresh credentials and retry.
- `45004`: digest or content metadata may be too long.
- `41005`: media file missing from multipart request.
- `40007` / `40009`: invalid media id or invalid image type.

## Constraints

- Draft title must be 32 characters or fewer.
- Digest must be 128 characters or fewer.
- Inline content images should use URLs returned by `media/uploadimg`.
- Cover images must use a `media_id` from permanent material upload.
- Do not include local file paths in final article HTML.
