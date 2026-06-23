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
