#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(scriptDir, '..');
const defaultConfigPath = path.join(process.env.HOME ?? '', '.config/wechat-official-draft/config.yaml');

function usage() {
  return `Usage:
  push_draft.mjs init --appid <appid> --secret <secret> [--config <path>]
  push_draft.mjs --file article.md --title "Title" --cover cover.png [options]

Options:
  --digest <text>        WeChat digest, max 128 characters
  --author <text>        Author, max 16 characters
  --cover <path>         Cover image path; required unless --dry-run
  --out <path>           Response JSON path
  --preview-out <path>   Local rendered HTML preview path
  --config <path>        Config YAML path; default ~/.config/wechat-official-draft/config.yaml
  --dry-run              Render local HTML preview without WeChat API calls
`;
}

function parseInitArgs(argv) {
  const args = { config: defaultConfigPath };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      const value = argv[++i];
      if (value == null) throw new Error(`missing value for ${arg}`);
      return value;
    };
    if (arg === '--appid') args.appid = next();
    else if (arg === '--secret') args.secret = next();
    else if (arg === '--config') args.config = next();
    else if (arg === '--help' || arg === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`unknown init argument: ${arg}`);
    }
  }
  if (!args.appid) throw new Error('init requires --appid');
  if (!args.secret) throw new Error('init requires --secret');
  return args;
}

function parseArgs(argv) {
  const args = {
    author: '',
    digest: '',
    out: '',
    previewOut: '',
    config: defaultConfigPath,
    dryRun: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      const value = argv[++i];
      if (value == null) throw new Error(`missing value for ${arg}`);
      return value;
    };
    if (arg === '--file') args.file = next();
    else if (arg === '--title') args.title = next();
    else if (arg === '--digest') args.digest = next();
    else if (arg === '--author') args.author = next();
    else if (arg === '--cover') args.cover = next();
    else if (arg === '--out') args.out = next();
    else if (arg === '--preview-out') args.previewOut = next();
    else if (arg === '--config') args.config = next();
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--help' || arg === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  if (!args.file) throw new Error('--file is required');
  if (!args.title) throw new Error('--title is required');
  if (!args.dryRun && !args.cover) throw new Error('--cover is required for draft creation');
  if ([...args.title].length > 32) throw new Error('--title must be 32 characters or fewer');
  if ([...args.digest].length > 128) throw new Error('--digest must be 128 characters or fewer');
  if ([...args.author].length > 16) throw new Error('--author must be 16 characters or fewer');
  return args;
}

function initConfig(args) {
  const configPath = path.resolve(args.config);
  fs.mkdirSync(path.dirname(configPath), { recursive: true, mode: 0o700 });
  const content = `wechat:\n  appid: ${args.appid}\n  secret: ${args.secret}\n`;
  fs.writeFileSync(configPath, content, { mode: 0o600 });
  fs.chmodSync(configPath, 0o600);
  console.log(JSON.stringify({ success: true, config: configPath }, null, 2));
}

function yamlValue(text, key) {
  return text.match(new RegExp(`^\\s*${key}:\\s*(.+?)\\s*$`, 'm'))?.[1]?.trim();
}

function readWechatConfig(file) {
  const envAppid = process.env.WECHAT_APPID?.trim();
  const envSecret = process.env.WECHAT_SECRET?.trim();
  if (envAppid && envSecret) return { appid: envAppid, secret: envSecret };
  const text = fs.readFileSync(file, 'utf8');
  const appid = yamlValue(text, 'appid');
  const secret = yamlValue(text, 'secret');
  if (!appid || !secret) {
    throw new Error(`missing WeChat credentials. Set WECHAT_APPID/WECHAT_SECRET or configure ${file}`);
  }
  return { appid, secret };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function inlineMd(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, '<code style="background:#f6f8fa;color:#334155;padding:2px 5px;border-radius:4px;font-size:14px;">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong style="color:#0f766e;font-weight:700;">$1</strong>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" style="color:#0f766e;text-decoration:none;">$1</a>');
}

async function getJson(url, options = {}) {
  const res = await fetch(url, options);
  const json = await res.json();
  if (!res.ok || json.errcode) {
    const err = new Error(json.errmsg || `HTTP ${res.status}`);
    err.response = json;
    throw err;
  }
  return json;
}

async function uploadMultipart(url, filePath, fieldName = 'media') {
  const bytes = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const type = ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : ext === '.webp' ? 'image/webp' : 'image/png';
  const blob = new Blob([bytes], { type });
  const form = new FormData();
  form.append(fieldName, blob, path.basename(filePath));
  const res = await fetch(url, { method: 'POST', body: form });
  const json = await res.json();
  if (!res.ok || json.errcode) {
    const err = new Error(json.errmsg || `HTTP ${res.status}`);
    err.response = json;
    throw err;
  }
  return json;
}

function collectImages(markdown, articlePath) {
  return [...markdown.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)].map((match) => ({
    alt: match[1],
    source: match[2],
    resolved: path.isAbsolute(match[2]) ? match[2] : path.resolve(path.dirname(articlePath), match[2]),
  }));
}

function renderHtml(markdown, imageUrlBySource = new Map()) {
  const lines = markdown.split(/\r?\n/);
  const out = [];
  let inCode = false;
  let code = [];
  let list = [];

  function flushList() {
    if (list.length === 0) return;
    out.push(`<ul style="margin:12px 0 18px 20px;padding:0;color:#334155;font-size:16px;line-height:1.85;">${list.map((item) => `<li style="margin:4px 0;">${inlineMd(item)}</li>`).join('')}</ul>`);
    list = [];
  }

  function flushCode() {
    out.push(`<pre style="white-space:pre-wrap;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px 16px;color:#334155;font-size:13px;line-height:1.65;overflow:auto;">${escapeHtml(code.join('\n'))}</pre>`);
    code = [];
    inCode = false;
  }

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (line.startsWith('```')) {
      if (inCode) flushCode();
      else {
        flushList();
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      code.push(raw);
      continue;
    }
    if (line.trim() === '') {
      flushList();
      continue;
    }
    const image = line.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if (image) {
      flushList();
      const url = imageUrlBySource.get(image[2]) ?? image[2];
      out.push(`<p style="margin:24px 0;text-align:center;"><img src="${escapeHtml(url)}" alt="${escapeHtml(image[1])}" style="max-width:100%;border-radius:8px;display:block;margin:0 auto;" /></p>`);
      continue;
    }
    const h1 = line.match(/^#\s+(.+)$/);
    if (h1) {
      flushList();
      out.push(`<h1 style="margin:0 0 24px;font-size:24px;line-height:1.35;color:#0f172a;font-weight:800;">${inlineMd(h1[1])}</h1>`);
      continue;
    }
    const h2 = line.match(/^##\s+(.+)$/);
    if (h2) {
      flushList();
      out.push(`<h2 style="margin:32px 0 14px;font-size:20px;line-height:1.45;color:#0f766e;font-weight:800;border-left:4px solid #0f766e;padding-left:10px;">${inlineMd(h2[1])}</h2>`);
      continue;
    }
    const h3 = line.match(/^###\s+(.+)$/);
    if (h3) {
      flushList();
      out.push(`<h3 style="margin:22px 0 10px;font-size:17px;line-height:1.5;color:#334155;font-weight:700;">${inlineMd(h3[1])}</h3>`);
      continue;
    }
    const quote = line.match(/^>\s*(.+)$/);
    if (quote) {
      flushList();
      out.push(`<blockquote style="margin:18px 0;padding:14px 16px;background:#f0fdfa;border-left:4px solid #14b8a6;color:#334155;border-radius:6px;font-size:16px;line-height:1.8;">${inlineMd(quote[1])}</blockquote>`);
      continue;
    }
    const li = line.match(/^(?:-|\d+\.)\s+(.+)$/);
    if (li) {
      list.push(li[1]);
      continue;
    }
    flushList();
    out.push(`<p style="margin:13px 0;color:#334155;font-size:16px;line-height:1.9;">${inlineMd(line)}</p>`);
  }
  flushList();
  if (inCode) flushCode();

  return `<section style="max-width:720px;margin:0 auto;padding:24px 12px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,'Noto Sans SC',sans-serif;background:#ffffff;">${out.join('\n')}</section>`;
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv[0] === 'init') {
    initConfig(parseInitArgs(argv.slice(1)));
    return;
  }
  const args = parseArgs(argv);
  const articlePath = path.resolve(args.file);
  const markdown = fs.readFileSync(articlePath, 'utf8');
  const images = collectImages(markdown, articlePath);
  const defaultOutDir = path.resolve(process.cwd(), '.tmp/wechat-official-draft');
  fs.mkdirSync(defaultOutDir, { recursive: true });
  const previewOut = path.resolve(args.previewOut || path.join(defaultOutDir, `${path.basename(articlePath, path.extname(articlePath))}.preview.html`));
  const responseOut = path.resolve(args.out || path.join(defaultOutDir, `${path.basename(articlePath, path.extname(articlePath))}.draft-response.json`));

  if (args.dryRun) {
    const html = renderHtml(markdown);
    fs.writeFileSync(previewOut, html);
    console.log(JSON.stringify({ success: true, dry_run: true, preview: previewOut, images: images.length }, null, 2));
    return;
  }

  const { appid, secret } = readWechatConfig(path.resolve(args.config));
  const tokenJson = await getJson(`https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${encodeURIComponent(appid)}&secret=${encodeURIComponent(secret)}`);
  const token = tokenJson.access_token;
  if (!token) throw new Error('WeChat access token missing in response');

  const imageUrlBySource = new Map();
  for (const image of images) {
    if (!fs.existsSync(image.resolved)) throw new Error(`image not found: ${image.resolved}`);
    const upload = await uploadMultipart(`https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=${encodeURIComponent(token)}`, image.resolved);
    imageUrlBySource.set(image.source, upload.url);
  }

  const coverPath = path.resolve(args.cover);
  if (!fs.existsSync(coverPath)) throw new Error(`cover not found: ${coverPath}`);
  const cover = await uploadMultipart(`https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${encodeURIComponent(token)}&type=image`, coverPath);
  if (!cover.media_id) throw new Error('cover media_id missing in response');

  const content = renderHtml(markdown, imageUrlBySource);
  fs.writeFileSync(previewOut, content);
  const payload = {
    articles: [
      {
        title: args.title,
        author: args.author,
        digest: args.digest,
        content,
        content_source_url: '',
        thumb_media_id: cover.media_id,
        need_open_comment: 0,
        only_fans_can_comment: 0,
      },
    ],
  };
  const draft = await getJson(`https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${encodeURIComponent(token)}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });
  fs.writeFileSync(responseOut, JSON.stringify({ draft, title: args.title, preview: previewOut }, null, 2));
  console.log(JSON.stringify({ success: true, draft, saved: responseOut, preview: previewOut }, null, 2));
}

const IP_WHITELIST_URL = 'https://developers.weixin.qq.com/platform?tab1=basicInfo&tab2=dev';

main().catch((error) => {
  const output = { success: false, error: error.message, details: error.response ?? null };
  if (error.response?.errcode === 40164 || /not in whitelist/.test(error.message)) {
    const ip = error.message.match(/invalid ip ([\d.]+)/)?.[1];
    output.hint = `Current IP${ip ? ` ${ip}` : ''} is not in the WeChat IP whitelist. Add it at: ${IP_WHITELIST_URL}`;
  }
  console.error(JSON.stringify(output, null, 2));
  process.exit(1);
});
