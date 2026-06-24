import json
from pathlib import Path
from scripts.deepdive.xhs_validate import validate_xhs

FIX = Path(__file__).parent / "fixtures" / "xhs_sample.json"

def load():
    return json.loads(FIX.read_text(encoding="utf-8"))

def test_valid_sample_has_no_errors():
    assert validate_xhs(load()) == []

def test_title_too_long():
    d = load(); d["title"] = "标" * 21
    assert any("标题" in e for e in validate_xhs(d))

def test_caption_too_long():
    d = load(); d["caption"] = "字" * 1001
    assert any("文案" in e for e in validate_xhs(d))

def test_too_few_cards():
    d = load(); d["cards"] = d["cards"][:3]
    assert any("卡片数" in e for e in validate_xhs(d))

def test_too_many_cards():
    d = load(); d["cards"] = [d["cards"][0]] * 9
    assert any("卡片数" in e for e in validate_xhs(d))

def test_heading_too_long():
    d = load(); d["cards"][0]["heading"] = "标" * 15
    assert any("heading" in e for e in validate_xhs(d))

def test_too_many_lines():
    d = load(); d["cards"][0]["lines"] = ["x"] * 5
    assert any("行数" in e for e in validate_xhs(d))

def test_line_too_long():
    d = load(); d["cards"][0]["lines"] = ["字" * 23]
    assert any("每行" in e for e in validate_xhs(d))

# 健壮性：脏输入应友好报错而非崩栈（校验器是稳定性闸门，拦的就是脏输入）
def test_null_title_does_not_crash():
    d = load(); d["title"] = None
    errs = validate_xhs(d)   # 不应抛 TypeError
    assert any("标题" in e for e in errs)

def test_null_caption_does_not_crash():
    d = load(); d["caption"] = None
    assert any("文案" in e for e in validate_xhs(d))

def test_non_dict_card_does_not_crash():
    d = load(); d["cards"][0] = "我不是对象"
    errs = validate_xhs(d)   # 不应抛 AttributeError
    assert any("必须是对象" in e for e in errs)

def test_null_line_does_not_crash():
    d = load(); d["cards"][0]["lines"] = [None]
    assert any("每行" in e for e in validate_xhs(d))
