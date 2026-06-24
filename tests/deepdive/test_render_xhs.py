import json
from pathlib import Path
from scripts.deepdive.render_xhs import build_render_data

FIX = Path(__file__).parent / "fixtures" / "xhs_sample.json"

def load():
    return json.loads(FIX.read_text(encoding="utf-8"))

def test_sets_kind_deepdive(tmp_path):
    data = build_render_data(load(), tmp_path)
    assert data["kind"] == "deepdive"

def test_cover_resolved_to_abspath_when_exists(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "cover.png").write_bytes(b"x")
    data = build_render_data(load(), tmp_path)
    assert data["cover"] == str((tmp_path / "assets" / "cover.png").resolve())

def test_cover_null_when_missing_file(tmp_path):
    data = build_render_data(load(), tmp_path)   # 没建 cover 文件
    assert data["cover"] is None

def test_passthrough_fields(tmp_path):
    src = load()
    data = build_render_data(src, tmp_path)
    assert data["title"] == src["title"]
    assert data["cards"] == src["cards"]
    assert data["caption"] == src["caption"]
    assert data["tags"] == src["tags"]
