"""去重器：用 SQLite 记录已处理条目，保证每天只推增量。
指纹 = sha1(归一化标题)，避免同一条动态被不同源/不同措辞重复推送。"""
import sqlite3, hashlib, re, datetime, os
from pathlib import Path

DB = Path(os.environ.get("DIGEST_OUT") or os.getcwd()) / "seen.db"

def _fp(item, vendor="anthropic"):
    # 指纹按厂商命名空间，避免两个厂商的同名条目互相误判为重复。
    t = vendor + "|" + re.sub(r"\s+", "", (item["title"] or "").lower())
    return hashlib.sha1(t.encode("utf-8")).hexdigest()

def _conn():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS seen(fp TEXT PRIMARY KEY, url TEXT, title TEXT, first_seen TEXT)")
    return c

def filter_new(items, vendor="anthropic"):
    c = _conn()
    seen = {r[0] for r in c.execute("SELECT fp FROM seen")}
    fresh = [it for it in items if _fp(it, vendor) not in seen]
    c.close()
    return fresh

def mark_seen(items, vendor="anthropic"):
    c = _conn()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    c.executemany("INSERT OR IGNORE INTO seen(fp,url,title,first_seen) VALUES(?,?,?,?)",
                  [(_fp(it, vendor), it["url"], it["title"], now) for it in items])
    c.commit(); c.close()

if __name__ == "__main__":
    import collector
    items = collector.collect(mock=True)
    print("collected:", len(items), "| new:", len(filter_new(items)))
