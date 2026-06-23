# 一手信源内参监控 MVP 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 小时级监控公开一手信源（claude.com/blog 等），新文章自动生成中文摘要、写 OKF 文件、开 PR 通知 review。

**Architecture:** 单 Python 脚本由 launchd 每小时触发。去重以 `data/firsthand/<id>/*.md` 实际文件为唯一真相（扫 frontmatter `resource`）。`firsthand-state.json` 仅做防重复短期记忆 + 健康统计。适配器按 `type` 分派，MVP 仅 Level 1（html-links / rss）。摘要走 `claude -p` 结构化输出。

**Tech Stack:** Python 3（标准库 + requests + feedparser + PyYAML）、`claude` CLI、`gh` CLI、launchd。

**关键约束（来自 spec 与现有 workflow）：**
- 内参 PR 分支前缀 `firsthand/`，**绝不用** `claude/*`、`daily-*`（会触发 auto-merge-daily workflow）。
- commit message **绝不用** `daily:` 前缀（会被 auto-merge 误自动合并，来不及 review）。state 提交用 `chore: firsthand state ...`。
- launchd 环境极简，脚本顶部必须 `export PATH`（复用 `scripts/watch-and-publish.sh:19` 的值）。
- 本机推 main 无 403（403 仅云端）。

---

## File Structure

| 文件 | 职责 |
|------|------|
| `firsthand-sources.yaml` | 信源配置（人工/skill 维护） |
| `scripts/monitor_firsthand.py` | 主脚本：抓取→去重→摘要→OKF→PR→健康统计 |
| `scripts/firsthand/__init__.py` | 包标记 |
| `scripts/firsthand/adapters.py` | Level 1 适配器（html-links / rss），统一返回 `[{url,title}]` |
| `scripts/firsthand/store.py` | OKF 文件读写 + 去重（扫 resource）+ state.json 读写 |
| `scripts/firsthand/summarize.py` | 调 `claude -p` 生成 `{summary, tags}` |
| `tests/firsthand/` | pytest 测试 |
| `data/firsthand-state.json` | 运行时生成（健康统计 + open_pr_urls） |
| `data/firsthand/<id>/*.md` | OKF 文章（去重真相） |
| `scripts/install-monitor-launchd.sh` | 安装 launchd |
| `~/Library/LaunchAgents/com.jialu.monitor-firsthand.plist` | 定时配置 |

测试用 `pytest`。先确认环境：

```bash
python3 -m pytest --version || pip3 install pytest
python3 -c "import requests, feedparser, yaml"  # 缺则 pip3 install requests feedparser PyYAML
```

---

## Task 0: Smoke test — 验证核心外部依赖

先验证两个 MVP 命脉：`claude -p` 能否返回结构化 JSON，html-links 抓取能否拿到 claude.com/blog 文章。失败则整个方案要调整，必须先做。

**Files:** 无（一次性验证）

- [ ] **Step 1: 验证 claude -p 结构化输出**

Run:
```bash
claude -p '只返回 JSON，不要任何其他文字。格式：{"summary":"一句话中文摘要","tags":["标签1","标签2"]}。内容：Claude Code 新增 artifacts 预览能力。'
```
Expected: 输出可被 `json.loads` 解析的对象，含 `summary` 与 `tags`。若混入解释文字，记下——summarize.py 需做 JSON 提取（截取第一个 `{` 到最后一个 `}`）。

- [ ] **Step 2: 验证 html-links 抓取**

Run:
```bash
python3 -c "
import requests, re
html = requests.get('https://claude.com/blog', timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
links = sorted(set(re.findall(r'href=\"(/blog/[^\"?#]+)\"', html)))
print('found', len(links))
for l in links[:5]: print(l)
"
```
Expected: `found 20+`，打印若干 `/blog/xxx` 路径。确认 `requests` 这条路对 claude.com 可用（无需浏览器）。

- [ ] **Step 3: 记录结果**

把两步的实际输出记在心里/笔记，作为 Task 3、Task 5 的实现依据。无需 commit。

---

## Task 1: 信源配置文件 + 加载

**Files:**
- Create: `firsthand-sources.yaml`
- Create: `scripts/firsthand/__init__.py`
- Create: `scripts/firsthand/config.py`
- Test: `tests/firsthand/test_config.py`

- [ ] **Step 1: 写 failing test**

`tests/firsthand/test_config.py`:
```python
from pathlib import Path
from scripts.firsthand.config import load_sources

def test_load_sources_parses_html_links(tmp_path):
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n"
        "  - id: claude-blog\n"
        "    name: Claude Blog\n"
        "    url: https://claude.com/blog\n"
        "    type: html-links\n"
        "    link_prefix: /blog/\n"
        "    base_url: https://claude.com\n",
        encoding="utf-8",
    )
    sources = load_sources(yaml_file)
    assert len(sources) == 1
    s = sources[0]
    assert s["id"] == "claude-blog"
    assert s["type"] == "html-links"
    assert s["base_url"] == "https://claude.com"

def test_load_sources_missing_file_returns_empty(tmp_path):
    assert load_sources(tmp_path / "nope.yaml") == []
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_config.py -v`
Expected: FAIL（ModuleNotFoundError: scripts.firsthand.config）

- [ ] **Step 3: 实现**

`scripts/firsthand/__init__.py`: 空文件。

`scripts/firsthand/config.py`:
```python
from pathlib import Path
import yaml

def load_sources(yaml_path: Path) -> list[dict]:
    """读 firsthand-sources.yaml，返回 source dict 列表；文件不存在返回 []。"""
    p = Path(yaml_path)
    if not p.exists():
        return []
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data.get("sources", []) or []
```

也需要 `tests/firsthand/__init__.py`（空）让 pytest 找到包；并在仓库根放 `conftest.py`（若无）确保 `scripts` 可导入：
```python
# conftest.py（仓库根，若已存在则跳过）
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_config.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: 写真实配置文件**

`firsthand-sources.yaml`:
```yaml
sources:
  - id: claude-blog
    name: Claude Blog
    url: https://claude.com/blog
    type: html-links
    link_prefix: /blog/
    base_url: https://claude.com
```

- [ ] **Step 6: Commit**

```bash
git add firsthand-sources.yaml scripts/firsthand/__init__.py scripts/firsthand/config.py tests/firsthand/ conftest.py
git commit -m "feat(firsthand): 信源配置加载"
```

---

## Task 2: URL 规范化工具

去重靠 URL 精确匹配，必须先统一格式（去 query、去 trailing slash、补全相对路径）。

**Files:**
- Create: `scripts/firsthand/urls.py`
- Test: `tests/firsthand/test_urls.py`

- [ ] **Step 1: 写 failing test**

`tests/firsthand/test_urls.py`:
```python
from scripts.firsthand.urls import canonical_url, make_absolute

def test_canonical_strips_query_and_trailing_slash():
    assert canonical_url("https://claude.com/blog/foo/?utm=x") == "https://claude.com/blog/foo"

def test_canonical_keeps_clean_url():
    assert canonical_url("https://claude.com/blog/foo") == "https://claude.com/blog/foo"

def test_make_absolute_joins_base():
    assert make_absolute("/blog/foo", "https://claude.com") == "https://claude.com/blog/foo"

def test_make_absolute_passes_through_absolute():
    assert make_absolute("https://x.com/a", "https://claude.com") == "https://x.com/a"
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_urls.py -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 实现**

`scripts/firsthand/urls.py`:
```python
from urllib.parse import urljoin, urlsplit, urlunsplit

def canonical_url(url: str) -> str:
    """去 query/fragment，去末尾斜杠，作为去重主键。"""
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))

def make_absolute(href: str, base_url: str) -> str:
    """相对路径补全为绝对 URL；已是绝对则原样返回。"""
    return urljoin(base_url.rstrip("/") + "/", href)
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_urls.py -v`
Expected: PASS（4 passed）

- [ ] **Step 5: Commit**

```bash
git add scripts/firsthand/urls.py tests/firsthand/test_urls.py
git commit -m "feat(firsthand): URL 规范化工具"
```

---

## Task 3: Level 1 适配器（html-links / rss）

**Files:**
- Create: `scripts/firsthand/adapters.py`
- Test: `tests/firsthand/test_adapters.py`

- [ ] **Step 1: 写 failing test**（用本地 HTML 字符串，不打网络）

`tests/firsthand/test_adapters.py`:
```python
from scripts.firsthand.adapters import extract_html_links, fetch_source

SAMPLE_HTML = '''
<html><body>
<a href="/blog/post-a">Post A</a>
<a href="/blog/post-b/?utm=x">Post B</a>
<a href="/about">About</a>
<a href="/blog/post-a">Dup</a>
</body></html>
'''

def test_extract_html_links_filters_prefix_and_dedups():
    source = {"link_prefix": "/blog/", "base_url": "https://claude.com"}
    items = extract_html_links(SAMPLE_HTML, source)
    urls = {i["url"] for i in items}
    assert urls == {
        "https://claude.com/blog/post-a",
        "https://claude.com/blog/post-b",
    }

def test_fetch_source_unknown_type_raises():
    try:
        fetch_source({"id": "x", "type": "nope"}, fetcher=lambda u: "")
        assert False, "should raise"
    except ValueError:
        pass
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_adapters.py -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 实现**

`scripts/firsthand/adapters.py`:
```python
import re
import requests
import feedparser
from .urls import canonical_url, make_absolute

_HREF_RE = re.compile(r'href="([^"]+)"')
_UA = {"User-Agent": "Mozilla/5.0 (firsthand-monitor)"}

def _http_get(url: str) -> str:
    resp = requests.get(url, timeout=20, headers=_UA)
    resp.raise_for_status()
    return resp.text

def extract_html_links(html: str, source: dict) -> list[dict]:
    prefix = source["link_prefix"]
    base = source["base_url"]
    seen, out = set(), []
    for href in _HREF_RE.findall(html):
        if not href.startswith(prefix):
            continue
        url = canonical_url(make_absolute(href, base))
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "title": None})
    return out

def _fetch_html_links(source: dict, fetcher) -> list[dict]:
    return extract_html_links(fetcher(source["url"]), source)

def _fetch_rss(source: dict, fetcher) -> list[dict]:
    feed = feedparser.parse(fetcher(source["url"]))
    out = []
    for e in feed.entries:
        link = getattr(e, "link", None)
        if not link:
            continue
        out.append({"url": canonical_url(link), "title": getattr(e, "title", None)})
    return out

_ADAPTERS = {"html-links": _fetch_html_links, "rss": _fetch_rss}

def fetch_source(source: dict, fetcher=_http_get) -> list[dict]:
    """按 type 分派到适配器。fetcher 可注入便于测试。返回 [{url,title}]。"""
    adapter = _ADAPTERS.get(source["type"])
    if adapter is None:
        raise ValueError(f"未知 source type: {source['type']}")
    return adapter(source, fetcher)
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_adapters.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: 真实抓取冒烟**

Run:
```bash
python3 -c "
from scripts.firsthand.adapters import fetch_source
s = {'id':'claude-blog','type':'html-links','url':'https://claude.com/blog','link_prefix':'/blog/','base_url':'https://claude.com'}
items = fetch_source(s)
print('fetched', len(items))
print(items[0])
"
```
Expected: `fetched 20+`，打印一个 `{'url': 'https://claude.com/blog/...', 'title': None}`。

- [ ] **Step 6: Commit**

```bash
git add scripts/firsthand/adapters.py tests/firsthand/test_adapters.py
git commit -m "feat(firsthand): Level 1 适配器 html-links/rss"
```

---

## Task 4: OKF 存储 + 文件级去重 + state.json

**Files:**
- Create: `scripts/firsthand/store.py`
- Test: `tests/firsthand/test_store.py`

- [ ] **Step 1: 写 failing test**

`tests/firsthand/test_store.py`:
```python
from pathlib import Path
from scripts.firsthand.store import (
    ingested_urls, write_okf, slugify, load_state, save_state,
)

def test_write_and_read_okf_roundtrip(tmp_path):
    article = {
        "title": "Artifacts in Claude Code",
        "source": "claude-blog",
        "url": "https://claude.com/blog/artifacts-in-claude-code",
        "summary": "新增 artifacts 预览。",
        "tags": ["claude-code", "artifacts"],
        "timestamp": "2026-06-23T15:30:00+08:00",
    }
    path = write_okf(tmp_path, article)
    assert path.exists()
    assert path.parent.name == "claude-blog"
    text = path.read_text(encoding="utf-8")
    assert "title: Artifacts in Claude Code" in text
    assert "resource: https://claude.com/blog/artifacts-in-claude-code" in text
    assert "新增 artifacts 预览。" in text
    # 去重读取
    assert ingested_urls(tmp_path, "claude-blog") == {
        "https://claude.com/blog/artifacts-in-claude-code"
    }

def test_ingested_urls_empty_for_new_source(tmp_path):
    assert ingested_urls(tmp_path, "brand-new") == set()

def test_slugify():
    assert slugify("https://claude.com/blog/artifacts-in-claude-code") == "artifacts-in-claude-code"

def test_state_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    assert load_state(state_file) == {}
    save_state(state_file, {"claude-blog": {"last_fetch_ok": True}})
    assert load_state(state_file)["claude-blog"]["last_fetch_ok"] is True
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_store.py -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 实现**

`scripts/firsthand/store.py`:
```python
import json
import re
from pathlib import Path

_FM_RESOURCE_RE = re.compile(r"^resource:\s*(\S+)\s*$", re.MULTILINE)

def slugify(url: str) -> str:
    """取 URL 最后一段作为 slug。"""
    return url.rstrip("/").rsplit("/", 1)[-1]

def _source_dir(root: Path, source_id: str) -> Path:
    return Path(root) / source_id

def ingested_urls(root: Path, source_id: str) -> set[str]:
    """扫 data/firsthand/<id>/*.md 的 frontmatter resource，= 已入库 URL 集合（去重真相）。"""
    d = _source_dir(root, source_id)
    if not d.exists():
        return set()
    urls = set()
    for md in d.glob("*.md"):
        m = _FM_RESOURCE_RE.search(md.read_text(encoding="utf-8"))
        if m:
            urls.add(m.group(1))
    return urls

def write_okf(root: Path, article: dict) -> Path:
    """写一篇 OKF markdown，返回路径。文件名 <date>-<slug>.md。"""
    d = _source_dir(root, article["source"])
    d.mkdir(parents=True, exist_ok=True)
    date = article["timestamp"][:10]
    path = d / f"{date}-{slugify(article['url'])}.md"
    tags = ", ".join(article.get("tags") or [])
    body = article.get("summary") or ""
    content = (
        "---\n"
        "type: Article\n"
        f"title: {article['title']}\n"
        f"source: {article['source']}\n"
        f"resource: {article['url']}\n"
        f"tags: [{tags}]\n"
        f"timestamp: {article['timestamp']}\n"
        "---\n\n"
        f"{body}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path

def load_state(state_file: Path) -> dict:
    p = Path(state_file)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

def save_state(state_file: Path, state: dict) -> None:
    Path(state_file).write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_store.py -v`
Expected: PASS（4 passed）

- [ ] **Step 5: Commit**

```bash
git add scripts/firsthand/store.py tests/firsthand/test_store.py
git commit -m "feat(firsthand): OKF 存储 + 文件级去重 + state"
```

---

## Task 5: 摘要生成（claude -p 结构化输出）

**Files:**
- Create: `scripts/firsthand/summarize.py`
- Test: `tests/firsthand/test_summarize.py`

- [ ] **Step 1: 写 failing test**（注入假 runner，不调真 claude）

`tests/firsthand/test_summarize.py`:
```python
from scripts.firsthand.summarize import summarize, _parse_json

def test_parse_json_extracts_from_noise():
    raw = '好的，结果如下：\n{"summary": "摘要", "tags": ["a", "b"]}\n完成。'
    obj = _parse_json(raw)
    assert obj["summary"] == "摘要"
    assert obj["tags"] == ["a", "b"]

def test_summarize_uses_runner():
    fake = lambda prompt: '{"summary": "新增预览能力。", "tags": ["claude-code"]}'
    result = summarize("Artifacts", "全文……", runner=fake)
    assert result["summary"] == "新增预览能力。"
    assert result["tags"] == ["claude-code"]

def test_summarize_fallback_on_bad_output():
    fake = lambda prompt: "完全不是 JSON 的东西"
    result = summarize("Title", "body", runner=fake)
    assert result["summary"] == "(摘要生成失败)"
    assert result["tags"] == []
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_summarize.py -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 实现**

`scripts/firsthand/summarize.py`:
```python
import json
import subprocess

_PROMPT = """只返回 JSON，不要任何解释或代码块标记。
格式：{{"summary": "中文摘要，100字以内", "tags": ["标签1", "标签2"]}}
针对以下文章生成面向中文 AI 从业者的摘要与 2-4 个主题标签。

标题：{title}

正文：
{body}
"""

def _claude_runner(prompt: str) -> str:
    proc = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=120,
    )
    return proc.stdout

def _parse_json(raw: str) -> dict:
    """从可能含噪声的输出里截取第一个 { 到最后一个 }。"""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no json")
    return json.loads(raw[start : end + 1])

def summarize(title: str, body: str, runner=_claude_runner) -> dict:
    """返回 {summary, tags}；任何失败回退到占位摘要。"""
    prompt = _PROMPT.format(title=title, body=body[:6000])
    try:
        obj = _parse_json(runner(prompt))
        return {
            "summary": str(obj.get("summary") or "(摘要生成失败)"),
            "tags": list(obj.get("tags") or []),
        }
    except Exception:
        return {"summary": "(摘要生成失败)", "tags": []}
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_summarize.py -v`
Expected: PASS（3 passed）

- [ ] **Step 5: 真实 claude 冒烟（可选但建议）**

Run:
```bash
python3 -c "
from scripts.firsthand.summarize import summarize
r = summarize('Artifacts in Claude Code', 'Claude Code now supports inline web artifacts preview...')
print(r)
"
```
Expected: 打印 `{'summary': '...中文...', 'tags': [...]}`。若回退到占位，说明 `claude -p` 输出格式需在 Task 0 笔记基础上调 prompt。

- [ ] **Step 6: Commit**

```bash
git add scripts/firsthand/summarize.py tests/firsthand/test_summarize.py
git commit -m "feat(firsthand): claude -p 摘要生成"
```

---

## Task 6: 正文抓取

为每篇新文章抓全文文本喂给摘要器。claude.com 文章是 SSR，标准库去标签即可。

**Files:**
- Modify: `scripts/firsthand/adapters.py`（追加 `fetch_article_text`）
- Test: `tests/firsthand/test_adapters.py`（追加）

- [ ] **Step 1: 追加 failing test**

在 `tests/firsthand/test_adapters.py` 末尾追加：
```python
from scripts.firsthand.adapters import fetch_article_text

def test_fetch_article_text_strips_tags():
    html = "<html><head><style>x{}</style></head><body><h1>Hi</h1><p>Hello world</p><script>bad()</script></body></html>"
    text = fetch_article_text("http://x", fetcher=lambda u: html)
    assert "Hi" in text
    assert "Hello world" in text
    assert "bad()" not in text
    assert "x{}" not in text
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_adapters.py::test_fetch_article_text_strips_tags -v`
Expected: FAIL（ImportError: cannot import name 'fetch_article_text'）

- [ ] **Step 3: 实现**

在 `scripts/firsthand/adapters.py` 追加：
```python
from html.parser import HTMLParser

class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "noscript"}
    def __init__(self):
        super().__init__()
        self._skip_depth = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
    def handle_data(self, data):
        if self._skip_depth == 0:
            t = data.strip()
            if t:
                self.parts.append(t)

def fetch_article_text(url: str, fetcher=_http_get) -> str:
    parser = _TextExtractor()
    parser.feed(fetcher(url))
    return "\n".join(parser.parts)
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_adapters.py -v`
Expected: PASS（3 passed）

- [ ] **Step 5: Commit**

```bash
git add scripts/firsthand/adapters.py tests/firsthand/test_adapters.py
git commit -m "feat(firsthand): 正文文本抓取"
```

---

## Task 7: 核心编排 — diff 逻辑（无副作用，纯函数）

把"抓取结果 + 已入库 + open_pr_urls → 真·新文章"这一步抽成可测纯函数，先不碰 git/PR。

**Files:**
- Create: `scripts/firsthand/pipeline.py`
- Test: `tests/firsthand/test_pipeline.py`

- [ ] **Step 1: 写 failing test**

`tests/firsthand/test_pipeline.py`:
```python
from scripts.firsthand.pipeline import diff_new_articles

def test_diff_excludes_ingested_and_open_pr():
    fetched = [
        {"url": "https://c/blog/a", "title": "A"},
        {"url": "https://c/blog/b", "title": "B"},
        {"url": "https://c/blog/c", "title": "C"},
    ]
    ingested = {"https://c/blog/a"}
    open_pr = {"https://c/blog/b"}
    new = diff_new_articles(fetched, ingested, open_pr)
    assert [a["url"] for a in new] == ["https://c/blog/c"]

def test_diff_first_run_all_new_when_nothing_known():
    fetched = [{"url": "https://c/blog/a", "title": "A"}]
    assert diff_new_articles(fetched, set(), set()) == fetched
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_pipeline.py -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 实现**

`scripts/firsthand/pipeline.py`:
```python
def diff_new_articles(fetched: list[dict], ingested: set, open_pr: set) -> list[dict]:
    """抓取结果中扣除已入库 + 已在未合并 PR 的 URL，得真·新文章。"""
    known = ingested | open_pr
    return [a for a in fetched if a["url"] not in known]
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_pipeline.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: Commit**

```bash
git add scripts/firsthand/pipeline.py tests/firsthand/test_pipeline.py
git commit -m "feat(firsthand): 新文章 diff 纯函数"
```

---

## Task 8: 主脚本 monitor_firsthand.py（编排 + git + PR）

把各模块串起来。git/PR 副作用集中在此，靠 `--dry-run` 跑通主路径再接真 PR。

**Files:**
- Create: `scripts/monitor_firsthand.py`
- Test: `tests/firsthand/test_monitor_dryrun.py`

- [ ] **Step 1: 写 failing test（dry-run，不打网络不动 git）**

`tests/firsthand/test_monitor_dryrun.py`:
```python
from pathlib import Path
from scripts.monitor_firsthand import run_once

def test_run_once_first_run_no_pr(tmp_path, monkeypatch):
    # 配置一个源
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n"
        "  - id: demo\n"
        "    name: Demo\n"
        "    url: https://demo/blog\n"
        "    type: html-links\n"
        "    link_prefix: /blog/\n"
        "    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"

    # 注入：抓取返回两篇，摘要返回固定，PR/commit 记录调用
    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    calls = {"pr": 0}
    result = run_once(
        sources_path=yaml_file,
        okf_root=okf_root,
        state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: calls.__setitem__("pr", calls["pr"] + 1),
        commit_state_fn=lambda: None,
    )
    # 首刊：不开 PR，但 state 记下 open_pr_urls 为已处理
    assert calls["pr"] == 0
    assert result["new_count"] == 0  # 首刊视为已处理，不计入新增

def test_run_once_second_run_opens_pr(tmp_path):
    yaml_file = tmp_path / "sources.yaml"
    yaml_file.write_text(
        "sources:\n  - id: demo\n    name: Demo\n    url: https://demo/blog\n"
        "    type: html-links\n    link_prefix: /blog/\n    base_url: https://demo\n",
        encoding="utf-8",
    )
    okf_root = tmp_path / "firsthand"
    state_file = tmp_path / "state.json"
    # 预置一篇已入库，模拟非首刊
    (okf_root / "demo").mkdir(parents=True)
    (okf_root / "demo" / "2026-06-22-a.md").write_text(
        "---\nresource: https://demo/blog/a\n---\n", encoding="utf-8")

    fetched = [{"url": "https://demo/blog/a", "title": "A"},
               {"url": "https://demo/blog/b", "title": "B"}]
    captured = {}
    run_once(
        sources_path=yaml_file, okf_root=okf_root, state_file=state_file,
        now="2026-06-23T15:30:00+08:00",
        fetch_fn=lambda s: fetched,
        article_text_fn=lambda u: "body",
        summarize_fn=lambda t, b: {"summary": "摘要", "tags": ["x"]},
        open_pr_fn=lambda branch, articles: captured.update(branch=branch, articles=articles),
        commit_state_fn=lambda: None,
    )
    # 只有 b 是新的 → 开 1 个 PR，分支前缀 firsthand/
    assert captured["branch"].startswith("firsthand/")
    assert [a["url"] for a in captured["articles"]] == ["https://demo/blog/b"]
    # 新文件已写入
    assert (okf_root / "demo" / "2026-06-23-b.md").exists()
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/firsthand/test_monitor_dryrun.py -v`
Expected: FAIL（ModuleNotFoundError: scripts.monitor_firsthand）

- [ ] **Step 3: 实现**

`scripts/monitor_firsthand.py`:
```python
#!/usr/bin/env python3
"""一手信源内参监控 —— launchd 每小时入口。"""
import os
# launchd 环境极简，先补 PATH（复用 watch-and-publish.sh 的值）
os.environ["PATH"] = (
    "/Users/jialu/anaconda3/bin:" + os.environ.get("PATH", "")
    + ":/opt/homebrew/bin:" + os.path.expanduser("~/.nvm/versions/node/v24.13.0/bin")
    + ":" + os.path.expanduser("~/.local/bin")
)

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.firsthand.config import load_sources
from scripts.firsthand.adapters import fetch_source, fetch_article_text
from scripts.firsthand.summarize import summarize
from scripts.firsthand.store import ingested_urls, write_okf, load_state, save_state
from scripts.firsthand.pipeline import diff_new_articles

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = REPO / "firsthand-sources.yaml"
DEFAULT_OKF_ROOT = REPO / "data" / "firsthand"
DEFAULT_STATE = REPO / "data" / "firsthand-state.json"


def run_once(sources_path, okf_root, state_file, now,
             fetch_fn=fetch_source,
             article_text_fn=fetch_article_text,
             summarize_fn=summarize,
             open_pr_fn=None,
             commit_state_fn=None):
    """单轮检查。副作用函数（PR/commit）可注入便于测试。返回统计 dict。"""
    okf_root = Path(okf_root)
    sources = load_sources(sources_path)
    state = load_state(state_file)
    all_new = []           # [(source, article)]
    for source in sources:
        sid = source["id"]
        st = state.setdefault(sid, {})
        try:
            fetched = fetch_fn(source)
            st["last_fetch_ok"] = True
            st["last_fetch_error"] = None
        except Exception as e:  # 抓取失败：记录、跳过
            st["last_fetch_ok"] = False
            st["last_fetch_error"] = str(e)
            st["last_checked"] = now
            continue
        st["last_checked"] = now
        ingested = ingested_urls(okf_root, sid)
        open_pr = set(st.get("open_pr_urls", []))
        first_run = not ingested and not open_pr and "total_articles_seen" not in st
        new_articles = diff_new_articles(fetched, ingested, open_pr)
        if first_run:
            # 首刊：全部标记为已处理，不开 PR
            st["open_pr_urls"] = [a["url"] for a in fetched]
            st["total_articles_seen"] = len(fetched)
            continue
        st["total_articles_seen"] = len(ingested) + len(open_pr)
        for art in new_articles:
            all_new.append((source, art))

    new_count = 0
    if all_new:
        pr_articles = []
        for source, art in all_new:
            text = article_text_fn(art["url"])
            s = summarize_fn(art.get("title") or art["url"], text)
            article = {
                "title": art.get("title") or art["url"],
                "source": source["id"],
                "url": art["url"],
                "summary": s["summary"],
                "tags": s["tags"],
                "timestamp": now,
            }
            write_okf(okf_root, article)
            state[source["id"]].setdefault("open_pr_urls", [])
            state[source["id"]]["open_pr_urls"].append(art["url"])
            state[source["id"]]["last_new_article"] = now
            pr_articles.append(article)
        new_count = len(pr_articles)
        branch = f"firsthand/{now[:10]}"
        if open_pr_fn:
            open_pr_fn(branch, pr_articles)

    save_state(state_file, state)
    if commit_state_fn:
        commit_state_fn()
    return {"new_count": new_count}


def _real_open_pr(branch, articles):
    """建分支、提交 OKF 文件、开 PR。"""
    subprocess.run(["git", "checkout", "-B", branch], cwd=REPO, check=True)
    # 只提 OKF 文件——state.json 走 main 单独提交，避免两头写同一文件 merge 时回退
    subprocess.run(["git", "add", "data/firsthand/"], cwd=REPO, check=True)
    # 注意：commit message 绝不用 daily: 前缀
    subprocess.run(["git", "commit", "-m", f"firsthand: 内参新动态 {branch}"],
                   cwd=REPO, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=REPO, check=True)
    by_source = {}
    for a in articles:
        by_source.setdefault(a["source"], []).append(a)
    counts = ", ".join(f"{k} {len(v)}篇" for k, v in by_source.items())
    title = f"📡 内参新动态 | {branch[-10:]} ({counts})"
    body_lines = []
    for sid, arts in by_source.items():
        body_lines.append(f"## {sid}")
        for a in arts:
            body_lines.append(f"- [{a['title']}]({a['url']})")
            body_lines.append(f"  > {a['summary']}")
    subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", "\n".join(body_lines),
         "--reviewer", "yinjialu", "--label", "firsthand-intel", "--base", "main"],
        cwd=REPO, check=True,
    )
    # 回到 main 供下一源/下一轮
    subprocess.run(["git", "checkout", "main"], cwd=REPO, check=True)


def _real_commit_state():
    """state.json 直接提交 main（本机无 403）。"""
    subprocess.run(["git", "add", "data/firsthand-state.json"], cwd=REPO, check=False)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if r.returncode != 0:  # 有变更
        subprocess.run(["git", "commit", "-m", "chore: firsthand state"], cwd=REPO, check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO, check=False)


def main():
    import datetime
    # Asia/Shanghai
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec="seconds")
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=REPO, check=False)
    result = run_once(
        DEFAULT_SOURCES, DEFAULT_OKF_ROOT, DEFAULT_STATE, now,
        open_pr_fn=_real_open_pr, commit_state_fn=_real_commit_state,
    )
    print(f"[firsthand] {now} new={result['new_count']}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/firsthand/test_monitor_dryrun.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: 全量测试**

Run: `python3 -m pytest tests/firsthand/ -v`
Expected: 全 PASS。

- [ ] **Step 6: Commit**

```bash
git add scripts/monitor_firsthand.py tests/firsthand/test_monitor_dryrun.py
git commit -m "feat(firsthand): 主脚本编排 + git/PR"
```

---

## Task 9: .gitignore 与首刊端到端验证

**Files:**
- Modify: `.gitignore`（如需）

- [ ] **Step 1: 确认 state.json 与 OKF 目录是要提交的（不忽略）**

spec 要求 `data/firsthand-state.json` 与 `data/firsthand/` 都提交 git。确认 `.gitignore` 没有忽略 `data/`：
```bash
git check-ignore data/firsthand-state.json data/firsthand/ || echo "未忽略，符合预期"
```
Expected: 打印"未忽略，符合预期"。若被忽略，加 `!data/firsthand/` 例外。

- [ ] **Step 2: 真实首刊干跑（只本地，不推送）**

临时把 `_real_open_pr` / `_real_commit_state` 换成打印，验证首刊不开 PR：
```bash
python3 -c "
from pathlib import Path
from scripts.monitor_firsthand import run_once
import datetime
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
r = run_once(
    Path('firsthand-sources.yaml'),
    Path('/tmp/firsthand-test/okf'),
    Path('/tmp/firsthand-test/state.json'),
    now,
    open_pr_fn=lambda b,a: print('WOULD OPEN PR', b, len(a)),
    commit_state_fn=lambda: print('WOULD COMMIT STATE'),
)
print('result', r)
"
```
Expected: 打印 `WOULD COMMIT STATE`、`result {'new_count': 0}`，**不**打印 `WOULD OPEN PR`（首刊静默）。`/tmp/firsthand-test/state.json` 里 claude-blog 的 `open_pr_urls` 含 20+ URL。

- [ ] **Step 3: 第二轮验证（模拟新文章）**

```bash
# 从 state 里删掉一个 URL，模拟"新文章出现"
python3 -c "
import json
p = '/tmp/firsthand-test/state.json'
s = json.load(open(p))
removed = s['claude-blog']['open_pr_urls'].pop()
json.dump(s, open(p,'w'), ensure_ascii=False, indent=2)
print('removed', removed)
"
# 再跑一轮，应识别出 1 篇新文章并 WOULD OPEN PR
python3 -c "
from pathlib import Path
from scripts.monitor_firsthand import run_once
import datetime
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
r = run_once(Path('firsthand-sources.yaml'), Path('/tmp/firsthand-test/okf'),
    Path('/tmp/firsthand-test/state.json'), now,
    open_pr_fn=lambda b,a: print('WOULD OPEN PR', b, [x['url'] for x in a]),
    commit_state_fn=lambda: None)
print(r)
"
```
Expected: 打印 `WOULD OPEN PR firsthand/2026-06-23 ['...被删的URL...']`，`new_count: 1`，且 `/tmp/firsthand-test/okf/claude-blog/` 下生成了对应 .md（真实调了 claude 摘要，约 1 分钟）。

- [ ] **Step 4: 清理临时目录**

```bash
rm -rf /tmp/firsthand-test
```

- [ ] **Step 5: Commit（若改了 .gitignore）**

```bash
git add .gitignore 2>/dev/null && git commit -m "chore(firsthand): 确保 state/OKF 不被忽略" || echo "无需改动"
```

---

## Task 10: launchd 安装

**Files:**
- Create: `scripts/com.jialu.monitor-firsthand.plist`
- Create: `scripts/install-monitor-launchd.sh`

- [ ] **Step 1: 写 plist 模板**

`scripts/com.jialu.monitor-firsthand.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.jialu.monitor-firsthand</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/jialu/ai-frontier-daily/scripts/monitor_firsthand.py</string>
  </array>
  <key>WorkingDirectory</key>
  <string>/Users/jialu/ai-frontier-daily</string>
  <key>RunAtLoad</key>
  <true/>
  <key>StartInterval</key>
  <integer>3600</integer>
  <key>StandardOutPath</key>
  <string>/Users/jialu/Library/Logs/monitor-firsthand.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/jialu/Library/Logs/monitor-firsthand.log</string>
</dict>
</plist>
```

- [ ] **Step 2: 写安装脚本**

`scripts/install-monitor-launchd.sh`:
```bash
#!/bin/bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/com.jialu.monitor-firsthand.plist"
DST="$HOME/Library/LaunchAgents/com.jialu.monitor-firsthand.plist"
cp "$SRC" "$DST"
launchctl unload "$DST" 2>/dev/null || true
launchctl load "$DST"
echo "已安装并加载：$DST"
echo "查看日志：tail -f ~/Library/Logs/monitor-firsthand.log"
echo "手动触发一次：launchctl start com.jialu.monitor-firsthand"
```

- [ ] **Step 3: 校验 plist 格式**

Run: `plutil -lint scripts/com.jialu.monitor-firsthand.plist`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
chmod +x scripts/install-monitor-launchd.sh
git add scripts/com.jialu.monitor-firsthand.plist scripts/install-monitor-launchd.sh
git commit -m "feat(firsthand): launchd 安装脚本与 plist"
```

- [ ] **Step 5: 安装并端到端真跑（产生真实 PR，最终验证）**

```bash
bash scripts/install-monitor-launchd.sh
launchctl start com.jialu.monitor-firsthand
sleep 90
tail -30 ~/Library/Logs/monitor-firsthand.log
```
Expected: 日志显示 `[firsthand] ... new=0`（首刊静默，state 已提交 main）。检查 `git log --oneline -3` 有 `chore: firsthand state` 提交。后续真有新文章时会自动开 `firsthand/<date>` PR 并邮件通知。

---

## Task 11: 两个 skill 骨架（接口预留）

MVP 实现 source-manager 的 add/list 与 source-subscriber 的 Level 1 适配器文档。browser-* 仅在 SKILL.md 标"阶段二"。

**Files:**
- Create: `skills/firsthand-source-subscriber/SKILL.md`
- Create: `skills/firsthand-source-manager/SKILL.md`

- [ ] **Step 1: 写 subscriber SKILL.md**

`skills/firsthand-source-subscriber/SKILL.md`:
```markdown
---
name: firsthand-source-subscriber
description: 一手信源订阅适配器。给定信源 URL，探测最稳的订阅方式（RSS / HTML 链接提取），返回统一的文章列表 [{url,title}]。用于 ai-frontier-daily 内参监控的新增信源探测与抓取。
---

# 一手信源订阅适配器

按 `type` 分派抓取策略，统一输出 `[{url, title}]`。

## MVP 适配器（Level 1，已实现于 scripts/firsthand/adapters.py）

- `html-links`：requests 抓页面，提取 `link_prefix` 开头的 href，拼 `base_url`。适合 SSR 站（claude.com/blog）。
- `rss`：feedparser 解析 feed。适合有 RSS/Atom 的源（OpenAI、GitHub releases.atom）。

## 探测新源订阅方式（add 时调用）

给定 URL，依次尝试：
1. 试 `<url>/rss.xml`、`/feed`、`/feed.xml`、`/sitemap.xml`，feedparser 能解析 → 用 `rss`。
2. 否则 requests 抓 HTML，统计最密集的文章链接前缀 → 用 `html-links`，推断 `link_prefix` 与 `base_url`。
3. 都不行（JS 渲染/403）→ 标记需阶段二 browser 适配器。

## 阶段二适配器（未实现）

`browser-headless` / `browser-auto`（Playwright MCP，**依赖未装组件，需先验证**）、`browser-live`（Claude in Chrome MCP，用户授权触发）、`manual`。详见 spec。
```

- [ ] **Step 2: 写 manager SKILL.md**

`skills/firsthand-source-manager/SKILL.md`:
```markdown
---
name: firsthand-source-manager
description: 维护 ai-frontier-daily 的一手信源清单 firsthand-sources.yaml。新增信源（探测订阅方式并写入）、列出信源健康状态。用户说"帮我监控这个网页 / 加个信源 / 看看信源健康度"时使用。
---

# 一手信源管理

## add <url>

1. 调 firsthand-source-subscriber 探测订阅方式（rss / html-links）。
2. 生成 source 条目（id 用域名+路径推导的 kebab-case），追加到 `firsthand-sources.yaml`。
3. 提示用户：下一轮 launchd（每小时）或手动 `launchctl start com.jialu.monitor-firsthand` 生效；该源首刊静默（只记录不开 PR）。

## list

读 `data/firsthand-state.json`，每个源输出：id、last_checked、last_fetch_ok（失败显示 last_fetch_error）、last_new_article、已入库篇数。

## 阶段二

- `health`：标记 last_fetch_ok=false 或异常沉默的源。
- `remove <id>`：从 yaml 移除并归档 state。
```

- [ ] **Step 3: Commit**

```bash
git add skills/firsthand-source-manager/ skills/firsthand-source-subscriber/
git commit -m "feat(firsthand): source-manager / source-subscriber skill 骨架"
```

---

## Task 12: 文档串联

**Files:**
- Modify: `CLAUDE.md`（追加内参链路说明）

- [ ] **Step 1: 在 CLAUDE.md 追加章节**

在 `CLAUDE.md` 末尾追加：
```markdown
## 一手信源内参监控（独立于每日日报）

- launchd `com.jialu.monitor-firsthand` 每小时跑 `scripts/monitor_firsthand.py`：
  抓 `firsthand-sources.yaml` 信源 → 新文章 claude -p 摘要 → 写 `data/firsthand/<id>/*.md`（OKF）
  → 开 `firsthand/<date>` 分支 PR（reviewer=yinjialu）。
- **去重真相 = `data/firsthand/<id>/` 实际文件**（扫 frontmatter resource），不是独立账本。
- **内参 PR 分支必须 `firsthand/` 前缀、commit 不带 `daily:`**——否则触发/误触发 auto-merge-daily。
- `data/firsthand-state.json`（健康统计 + 防重复）直接提交 main，本机无 403。
- 新增信源走 `firsthand-source-manager` skill；新源首刊静默（只记录不开 PR）。
- 阶段二（browser-* 登录态源 + 菜单栏/快捷键授权）见 `docs/superpowers/specs/2026-06-23-firsthand-monitor-design.md`。
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(firsthand): CLAUDE.md 补充内参监控链路说明"
```

---

## 完成标准

- [ ] `python3 -m pytest tests/firsthand/ -v` 全绿
- [ ] launchd 已装，日志显示首刊 `new=0` 且 state 提交进 main
- [ ] 模拟新文章时能正确开 `firsthand/<date>` PR、reviewer=yinjialu、含中文摘要
- [ ] 内参分支前缀 `firsthand/`、commit 无 `daily:` 前缀（不干扰 auto-merge-daily）
- [ ] 两个 skill 骨架可被 `/firsthand-source-manager` 等触发
```
