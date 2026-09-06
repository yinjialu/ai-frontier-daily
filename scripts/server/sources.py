"""Bounded official-source adapters. RSSHub is a transport, not the publisher."""
import calendar
import hashlib
import json
import os
import re
import subprocess
import threading
import xml.etree.ElementTree as ET
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

from scripts.firsthand.adapters import extract_published, parse_human_date
from scripts.firsthand.urls import canonical_url

_BROWSER_LOCK = threading.Lock()


def published_date(value):
    value = re.sub(r"(January|February|March|April|June|July|August|September|October|November|December)", lambda m: m[0][:3], value or "")
    return parse_human_date(value)


def get(url):
    # Deliberately bounded: one broken source must not block a whole patrol.
    with requests.get(url, timeout=(8, 20), headers={
        "User-Agent": "Mozilla/5.0 (compatible; AIFrontierDaily/1.0)"}, stream=True) as r:
        r.raise_for_status()
        chunks, size = [], 0
        for chunk in r.iter_content(65536):
            size += len(chunk)
            if size > 6_000_000:
                raise ValueError("source exceeds 6 MB limit")
            chunks.append(chunk)
        return b"".join(chunks).decode(r.encoding if r.encoding and r.encoding != "ISO-8859-1" else "utf-8", errors="replace")


def text(html):
    soup = BeautifulSoup(html or "", "html.parser")
    for tag in soup.select("script,style,nav,footer,header,noscript"):
        tag.decompose()
    return " ".join(soup.stripped_strings)


def official(url, source):
    p = urlparse(url)
    return p.scheme == "https" and p.hostname in source["domains"] and not p.username


def entry(source, url, title, body="", published=None):
    # Preserve changelog anchors; canonical_url intentionally strips fragments.
    anchor = urlparse(url).fragment
    url = canonical_url(url) + ("#" + anchor if anchor else "")
    if not official(url, source):
        raise ValueError("article link outside configured official domains")
    return {"id": hashlib.sha256(url.encode()).hexdigest()[:24],
            "source_id": source["id"], "vendor": source["vendor"],
            "company": source.get("company") or {"openai": "OpenAI", "anthropic": "Anthropic", "gemini": "Google", "nvidia": "NVIDIA"}.get(source["vendor"], source["name"]), "url": url,
            "title": title[:300], "text": body[:14000], "published": published,
            "signal": source.get("signal", "announcement")}


def parse_feed(raw, source):
    feed = feedparser.parse(raw)
    if not feed.version or not feed.entries:
        raise ValueError("not a nonempty RSS/Atom feed (HTML/challenge/empty route)")
    items = []
    for e in feed.entries[:25]:
        if not e.get("link"):
            continue
        tm = e.get("published_parsed")  # updated is NOT a publication date
        published = datetime.fromtimestamp(calendar.timegm(tm), timezone.utc).isoformat() if tm else None
        body = e.get("content", [{}])[0].get("value") or e.get("summary", "")
        items.append(entry(source, e.link, e.get("title", e.link), text(body), published))
    if not items:
        raise ValueError("feed contains no usable official links")
    return items


def parse_links(raw, source):
    soup, seen, items = BeautifulSoup(raw, "html.parser"), set(), []
    for a in soup.select("a[href]"):
        href = a["href"]
        url = urljoin(source["url"], href)
        if not official(url, source) or not re.search(source["path_regex"], urlparse(url).path):
            continue
        url = canonical_url(url)
        if url in seen:
            continue
        seen.add(url)
        title = " ".join(a.stripped_strings) or urlparse(url).path.rsplit("/", 1)[-1]
        time = a.find("time")
        published = time.get("datetime") if time else published_date(title)
        items.append(entry(source, url, title, published=published))
    if not items:
        raise ValueError("no article links; selector or access needs attention")
    return items[:30]


def parse_changelog(raw, source):
    soup = BeautifulSoup(raw, "html.parser")
    main = soup.select_one("main,article") or soup
    items = []
    for h in main.find_all(["h2", "h3"]):
        title = h.get_text(" ", strip=True)
        date = published_date(title)
        if not date:
            m = re.search(r"20\d{2}-\d{2}-\d{2}", title)
            date = m.group() if m else None
        if not date:
            continue
        parts = []
        for sibling in h.next_siblings:
            if getattr(sibling, "name", None) in {"h2", "h3"}:
                break
            if hasattr(sibling, "get_text"):
                parts.append(sibling.get_text(" ", strip=True))
        body = " ".join(parts)
        if body:
            anchor = h.get("id") or date
            # Multiple additions to the same date must remain detectable.
            item = entry(source, source["url"] + "#" + anchor, title, body, date)
            item["id"] += "-" + hashlib.sha256(body.encode()).hexdigest()[:8]
            items.append(item)
    if not items:
        for block in main.select(".update-container[id]"):
            date = block.get("id", "")
            if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", date):
                continue
            body = block.get_text(" ", strip=True)
            i = entry(source, source["url"] + "#" + date, body[:120], body, date)
            i["id"] += "-" + hashlib.sha256(body.encode()).hexdigest()[:8]
            items.append(i)
    if not items:
        raise ValueError("no dated changelog entries")
    return items[:12]


def parse_markdown_changelog(raw, source):
    year, items = None, []
    for section in re.split(r"(?m)^(?=## )", raw):
        match = re.search(r"^## \w+,? (20\d{2})", section)
        if not match:
            continue
        year = match[1]
        for block in re.split(r"(?m)^### ", section)[1:]:
            title, _, body = block.partition("\n")
            date = published_date(f"{title}, {year}")
            if not date:
                continue
            i = entry(source, source["url"].removesuffix(".md") + "#" + date, title + " " + year, body.strip(), date)
            i["id"] += "-" + hashlib.sha256(body.encode()).hexdigest()[:8]
            items.append(i)
    if not items:
        raise ValueError("no dated markdown changelog entries")
    return items[:15]


def parse_sitemap(raw, source):
    root = ET.fromstring(raw)
    items = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "loc" or not element.text:
            continue
        url = element.text.strip()
        if official(url, source) and re.search(source["path_regex"], urlparse(url).path):
            # Sitemap lastmod is not publication time. Enrich from article metadata.
            items.append(entry(source, url, urlparse(url).path.rsplit("/", 1)[-1]))
    if not items:
        raise ValueError("no matching official articles in sitemap")
    return items[:500]


def search(source):
    # Hermes' existing search provider discovers leads. Only configured official
    # domains enter the editorial queue; snippets are never evidence of a release.
    from tools.web_tools import web_search_tool
    from zoneinfo import ZoneInfo
    date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
    query = source["query"] + " " + date
    response = json.loads(web_search_tool(query, limit=5))
    if not response.get("success"):
        query = source["query"].split(" (")[0] + " " + date + " site:" + source["domains"][0]
        response = json.loads(web_search_tool(query, limit=5))
    if not response.get("success"):
        raise ValueError("Hermes web search unavailable")
    results = response.get("data", {}).get("web", [])
    items = [entry(source, r["url"], r.get("title", r["url"])) for r in results if r.get("url") and official(r["url"], source)]
    return items, query, [{"url": r.get("url"), "title": r.get("title")} for r in results]


def fetch(source):
    if source["type"] == "web-search":
        try:
            items, query, leads = search(source)
            return {"source": source, "items": items, "error": None, "query": query, "leads": leads}
        except Exception as exc:
            return {"source": source, "items": [], "error": type(exc).__name__ + ": search failed"}
    errors = []
    primary_url = source["url"].replace("http://127.0.0.1:1200", os.getenv("RSSHUB_BASE_URL", "http://127.0.0.1:1200"))
    routes = [(source["type"], primary_url)]
    if source.get("rsshub"):
        routes.append(("rss", os.getenv("RSSHUB_BASE_URL", "http://127.0.0.1:1200").rstrip("/") + source["rsshub"]))
    if source.get("browser"):
        routes.append(("browser-links", primary_url))
    for kind, url in routes:
        try:
            if kind == "browser-links":
                with _BROWSER_LOCK:
                    proc = subprocess.run(["node", str(Path(__file__).with_name("fetch-page.cjs")), url, source["path_regex"]], capture_output=True, text=True, check=True, timeout=65)
                raw = proc.stdout
            else:
                raw = get(url)
            items = {"rss": parse_feed, "html-links": parse_links, "browser-links": parse_links, "changelog": parse_changelog, "markdown-changelog": parse_markdown_changelog, "sitemap": parse_sitemap}[kind](raw, source)
            if len(items) < source.get("min_items", 1):
                raise ValueError("listing contains too few articles; hydration may be incomplete")
            return {"source": source, "items": items, "transport": url, "error": None}
        except Exception as exc:
            # Do not log response bodies, request headers, or credentials.
            errors.append(type(exc).__name__ + ": " + str(exc).split("?")[0][:180])
    return {"source": source, "items": [], "error": " | ".join(errors)}


def collect(path):
    sources = yaml.safe_load(path.read_text())["sources"]
    with ThreadPoolExecutor(max_workers=2 if sources and sources[0]["type"] == "web-search" else 4) as pool:
        return list(pool.map(fetch, sources))


def enrich(item):
    if len(item["text"]) >= 100 and item.get("published"):
        return item
    raw = get(item["url"].split("#")[0])
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.find("h1")
    meta = soup.select_one('meta[property="article:published_time"],meta[name="date"],meta[itemprop="datePublished"]')
    time = soup.find("time")
    published = item.get("published") or extract_published(raw)
    if not published and meta:
        published = meta.get("content")
    if not published and time:
        published = time.get("datetime") or published_date(time.get_text(" ", strip=True))
    if not published and title:
        header = title.parent.get_text(" ", strip=True)
        if len(header) < 600:
            published = published_date(header)
    return dict(item, title=title.get_text(" ", strip=True) if title else item["title"],
                text=text(str(soup.select_one("article,main") or soup))[:14000],
                published=published)
