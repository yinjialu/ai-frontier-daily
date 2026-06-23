from scripts.firsthand.urls import canonical_url, make_absolute

def test_canonical_strips_query_and_trailing_slash():
    assert canonical_url("https://claude.com/blog/foo/?utm=x") == "https://claude.com/blog/foo"

def test_canonical_keeps_clean_url():
    assert canonical_url("https://claude.com/blog/foo") == "https://claude.com/blog/foo"

def test_make_absolute_joins_base():
    assert make_absolute("/blog/foo", "https://claude.com") == "https://claude.com/blog/foo"

def test_make_absolute_passes_through_absolute():
    assert make_absolute("https://x.com/a", "https://claude.com") == "https://x.com/a"
