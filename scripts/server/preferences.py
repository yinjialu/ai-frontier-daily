"""Explicit owner feedback, persisted separately from factual editorial decisions.

Callers must resolve ``item`` from a trusted server item or checked-in archive.
Client supplied company/tag fields are not a trusted preference training source.
"""
import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ACTIONS = {"useful", "less", "clear"}
TAGS = {"模型发布", "开发者", "研究", "企业", "生态", "政策", "安全"}
HALF_LIFE_DAYS = 30
_IDENTIFIER = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_TRACKING = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def canonical_url(url):
    """Normalize URL identity, retaining meaningful query and changelog anchors."""
    if not isinstance(url, str) or len(url) > 4096 or any(ord(c) < 32 for c in url):
        raise ValueError("invalid content URL")
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname or parts.username is not None:
        raise ValueError("invalid content URL")
    scheme, host = parts.scheme.lower(), parts.hostname.lower().encode("idna").decode()
    port = parts.port  # Also rejects malformed ports.
    if ":" in host:
        host = "[" + host + "]"
    if port and (scheme, port) not in {("http", 80), ("https", 443)}:
        host += ":" + str(port)
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.lower().startswith("utm_") and k.lower() not in _TRACKING)
    return urlunsplit((scheme, host, parts.path.rstrip("/") or "/", urlencode(query), parts.fragment))


def content_key(url):
    return "url:" + hashlib.sha256(canonical_url(url).encode()).hexdigest()


def init_schema(db):
    db.executescript("""
      CREATE TABLE IF NOT EXISTS feedback_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor TEXT NOT NULL, request_id TEXT NOT NULL, content_key TEXT NOT NULL,
        action TEXT NOT NULL CHECK(action IN ('useful','less','clear')),
        url TEXT NOT NULL, company TEXT NOT NULL, tag TEXT NOT NULL, created_at TEXT NOT NULL,
        UNIQUE(actor, request_id));
      CREATE TABLE IF NOT EXISTS feedback_current (
        actor TEXT NOT NULL, content_key TEXT NOT NULL, event_id INTEGER NOT NULL,
        PRIMARY KEY(actor, content_key), FOREIGN KEY(event_id) REFERENCES feedback_events(id));
      CREATE INDEX IF NOT EXISTS feedback_events_actor ON feedback_events(actor, id);
    """)


def _actor(actor):
    if not isinstance(actor, str) or not _IDENTIFIER.fullmatch(actor):
        raise ValueError("invalid feedback actor")
    return actor


def _now(value=None):
    value = value or datetime.now(timezone.utc)
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("timezone-aware feedback timestamp required")
    return value.astimezone(timezone.utc)


def _metadata(item):
    url = canonical_url(item.get("url"))
    company = item.get("company", "")
    tag = item.get("editorial", {}).get("tag", item.get("tag", ""))
    if not isinstance(company, str) or len(company) > 120:
        raise ValueError("invalid trusted company")
    if not isinstance(tag, str) or len(tag) > 80:
        raise ValueError("invalid trusted tag")
    # Unknown archive labels remain recordable but do not train taxonomy weights.
    return url, " ".join(company.split()), tag.strip()


def _entry(row):
    return {"content_key": row["content_key"], "url": row["url"],
            "company": row["company"], "tag": row["tag"], "action": row["action"],
            "updated_at": row["created_at"], "version": row["id"]}


def record_feedback(db, item, action, request_id, *, actor="owner", now=None):
    """Append one idempotent action; replay returns current, not stale, state.

    ``item`` is trusted metadata with url/company and editorial.tag or tag.
    Reusing a request_id for a different content/action raises ValueError.
    ``clear`` removes the current training signal but retains its audit trail.
    """
    actor = _actor(actor)
    if not isinstance(action, str) or action not in ACTIONS:
        raise ValueError("invalid feedback action")
    if not isinstance(request_id, str) or not _IDENTIFIER.fullmatch(request_id):
        raise ValueError("invalid feedback request_id")
    url, company, tag = _metadata(item)
    key, timestamp = content_key(url), _now(now).isoformat()
    # The first statement is a write: SQLite serializes concurrent writers before
    # we inspect/reuse the idempotency key or update the current-action pointer.
    with db:
        inserted = db.execute("""INSERT INTO feedback_events
          (actor,request_id,content_key,action,url,company,tag,created_at)
          VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(actor,request_id) DO NOTHING""",
          (actor, request_id, key, action, url, company, tag, timestamp)).rowcount
        event = db.execute("SELECT * FROM feedback_events WHERE actor=? AND request_id=?",
                           (actor, request_id)).fetchone()
        if event["content_key"] != key or event["action"] != action:
            raise ValueError("feedback request_id already used for another action")
        if inserted:
            db.execute("""INSERT INTO feedback_current(actor,content_key,event_id) VALUES (?,?,?)
              ON CONFLICT(actor,content_key) DO UPDATE SET event_id=excluded.event_id""",
              (actor, key, event["id"]))
        current = db.execute("""SELECT e.* FROM feedback_current c JOIN feedback_events e ON e.id=c.event_id
          WHERE c.actor=? AND c.content_key=?""", (actor, key)).fetchone()
    return dict(_entry(current), request_id=request_id, request_action=action, duplicate=not bool(inserted))


def list_feedback(db, *, actor="owner", include_cleared=False):
    rows = db.execute("""SELECT e.* FROM feedback_current c JOIN feedback_events e ON e.id=c.event_id
      WHERE c.actor=? ORDER BY e.id DESC""", (_actor(actor),))
    return [_entry(r) for r in rows if include_cleared or r["action"] != "clear"]


def preference_summary(db, *, actor="owner", now=None):
    """One active signal per URL; 30-day decay and shrinkage bound generalization."""
    actor, current = _actor(actor), _now(now)
    entries = list_feedback(db, actor=actor)
    groups = {"company": {}, "tag": {}}
    for entry in entries:
        age = max(0, (current - _now(entry["updated_at"])).total_seconds() / 86400)
        weight = 2 ** (-age / HALF_LIFE_DAYS)
        sign = 1 if entry["action"] == "useful" else -1
        for kind in groups:
            label = entry[kind].casefold() if kind == "company" else entry[kind]
            if not label or kind == "tag" and label not in TAGS:
                continue
            positive, total = groups[kind].get(label, (0, 0))
            groups[kind][label] = positive + sign * weight, total + weight
    weights = {kind + "_weights": {
        label: round(limit * signed / (4 + total), 6)
        for label, (signed, total) in values.items()}
        for kind, values in groups.items()
        for limit in [0.35 if kind == "company" else 0.20]}
    latest = db.execute("SELECT id,created_at FROM feedback_events WHERE actor=? ORDER BY id DESC LIMIT 1",
                        (actor,)).fetchone()
    return dict(version=latest["id"] if latest else 0,
                updated_at=latest["created_at"] if latest else None,
                count=len(entries), useful=sum(e["action"] == "useful" for e in entries),
                less=sum(e["action"] == "less" for e in entries), **weights)


def rank_items(db, items, *, actor="owner", now=None):
    """Rerank factual candidates only; never drop candidates or lower important items.

    Freshness retains a 72-hour range. One new company/tag sample can contribute
    at most 0.11, and direct feedback 0.25; there is no vendor-wide penalty.
    Breaking-alert delivery explicitly bypasses this owner preference ranking.
    """
    current = _now(now)
    summary = preference_summary(db, actor=actor, now=current)
    active = {e["content_key"]: e for e in list_feedback(db, actor=actor)}
    if not active:
        return sorted(items, key=lambda i: not i.get("editorial", {}).get("important", False))

    def order(item):
        editorial = item.get("editorial", {})
        important = bool(editorial.get("important", False))
        url, company, tag = _metadata(item)
        learned = summary["company_weights"].get(company.casefold(), 0) + summary["tag_weights"].get(tag, 0)
        direct = active.get(content_key(url))
        if direct:
            days = max(0, (current - _now(direct["updated_at"])).total_seconds() / 86400)
            learned += (0.25 if direct["action"] == "useful" else -0.25) * 2 ** (-days / HALF_LIFE_DAYS)
        try:
            published = datetime.fromisoformat(item["published"].replace("Z", "+00:00"))
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
            age_hours = max(0, (current - published).total_seconds() / 3600)
            freshness = max(0, 1 - age_hours / 72)
        except (AttributeError, KeyError, TypeError, ValueError):
            freshness = 0
        return not important, -(freshness + max(-0.8, min(0.8, learned)))

    return sorted(items, key=order)
