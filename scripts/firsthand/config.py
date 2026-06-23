from pathlib import Path
import yaml


def load_sources(yaml_path: Path) -> list[dict]:
    """读 firsthand-sources.yaml，返回 source dict 列表；文件不存在返回 []。"""
    p = Path(yaml_path)
    if not p.exists():
        return []
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data.get("sources", []) or []
