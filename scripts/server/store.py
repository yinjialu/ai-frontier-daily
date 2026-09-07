import json
import hashlib
import sqlite3
from datetime import datetime, timezone


def connect(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
      PRAGMA journal_mode=WAL;
      CREATE TABLE IF NOT EXISTS sources (id TEXT PRIMARY KEY, initialized INTEGER DEFAULT 0,
        checked TEXT, error TEXT, failures INTEGER DEFAULT 0, count INTEGER DEFAULT 0);
      CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, payload TEXT NOT NULL,
        detected TEXT NOT NULL, baseline INTEGER NOT NULL, curated TEXT, error TEXT);
      CREATE TABLE IF NOT EXISTS deliveries (id TEXT PRIMARY KEY, message_id TEXT NOT NULL, sent TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS editions (date TEXT PRIMARY KEY, payload TEXT NOT NULL);
    """)
    if "fingerprint" not in {r[1] for r in db.execute("PRAGMA table_info(sources)")}:
        db.execute("ALTER TABLE sources ADD COLUMN fingerprint TEXT")
    from .preferences import init_schema
    init_schema(db)
    return db


def ingest(db, results, now=None):
    now = now or datetime.now(timezone.utc).isoformat()
    added = 0
    with db:
        for result in results:
            sid = result["source"]["id"]
            db.execute("INSERT OR IGNORE INTO sources(id) VALUES (?)", (sid,))
            old = db.execute("SELECT * FROM sources WHERE id=?", (sid,)).fetchone()
            if result["error"]:
                db.execute("UPDATE sources SET checked=?,error=?,failures=failures+1 WHERE id=?", (now, result["error"], sid))
                continue
            fingerprint = hashlib.sha256(json.dumps(result["source"], sort_keys=True).encode()).hexdigest()
            baseline = int(not old["initialized"] or old["fingerprint"] != fingerprint)
            for item in result["items"]:
                cur = db.execute("INSERT OR IGNORE INTO items VALUES (?,?,?,?,NULL,NULL)",
                                 (item["id"], json.dumps(item, ensure_ascii=False), now, baseline))
                added += cur.rowcount if not baseline else 0
            db.execute("UPDATE sources SET initialized=1,checked=?,error=NULL,failures=0,count=?,fingerprint=? WHERE id=?", (now, len(result["items"]), fingerprint, sid))
    return added


def pending(db, limit=24):
    return [json.loads(row[0]) for row in db.execute(
        "SELECT payload FROM items WHERE baseline=0 AND curated IS NULL ORDER BY error IS NOT NULL,detected LIMIT ?", (limit,))]


def record_delivery(db, key, message_id):
    with db:
        db.execute("INSERT OR IGNORE INTO deliveries VALUES (?,?,?)", (key, message_id, datetime.now(timezone.utc).isoformat()))


def delivered(db, key):
    return db.execute("SELECT 1 FROM deliveries WHERE id=?", (key,)).fetchone() is not None
