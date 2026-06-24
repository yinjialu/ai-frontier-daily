import json
from pathlib import Path
from scripts.deepdive.render_xhs import build_render_data, clean_render_outputs, update_index

FIX = Path(__file__).parent / "fixtures" / "xhs_sample.json"

def load():
    return json.loads(FIX.read_text(encoding="utf-8"))

def test_sets_kind_deepdive(tmp_path):
    data = build_render_data(load(), tmp_path)
    assert data["kind"] == "deepdive"

def test_cover_becomes_data_uri_when_exists(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "cover.png").write_bytes(b"x")
    data = build_render_data(load(), tmp_path)
    # 内联成 data URI（file:// 在 setContent 渲染下会被 Chromium 拦截）
    assert data["cover"].startswith("data:image/png;base64,")

def test_card_image_becomes_data_uri_when_exists(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "diagram.png").write_bytes(b"x")
    src = load()
    src["cards"][0]["image"] = "assets/diagram.png"
    data = build_render_data(src, tmp_path)
    assert data["cards"][0]["image"].startswith("data:image/png;base64,")

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

def test_update_index_creates_and_upserts(tmp_path):
    root = tmp_path / "deepdive"
    update_index(root, "a", "标题A")
    update_index(root, "b", "标题B")
    items = json.loads((root / "index.json").read_text(encoding="utf-8"))["items"]
    # 最新置顶 + 各一条
    assert [it["slug"] for it in items] == ["b", "a"]

def test_update_index_upsert_no_dup_and_moves_to_top(tmp_path):
    root = tmp_path / "deepdive"
    update_index(root, "a", "旧标题")
    update_index(root, "b", "标题B")
    items = update_index(root, "a", "新标题")  # 重渲 a：去重 + 置顶 + 更新 title
    assert [it["slug"] for it in items] == ["a", "b"]
    assert items[0]["title"] == "新标题"

def test_clean_render_outputs_removes_stale_card_images_only(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    for name in ["00-cover.jpg", "01-card.png", "manifest.json", "caption.txt", "notes.md"]:
        (out / name).write_text("x", encoding="utf-8")
    clean_render_outputs(out)
    assert not (out / "00-cover.jpg").exists()
    assert not (out / "01-card.png").exists()
    assert not (out / "manifest.json").exists()
    assert (out / "caption.txt").exists()
    assert (out / "notes.md").exists()
