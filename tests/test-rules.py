from rules import RULES, search_rules


def test_every_rule_has_a_source_and_supported_confidence():
    allowed = {"standard", "common", "style-dependent"}
    assert RULES
    assert all(rule["source"].startswith("https://") for rule in RULES)
    assert all(rule["confidence"] in allowed for rule in RULES)
    assert len({rule["id"] for rule in RULES}) == len(RULES)


def test_search_finds_arabic_grammar_rules_with_source_name():
    result = search_rules("المبتدأ والخبر", "grammar")
    assert result
    assert any(rule["id"] == "nominal-sentence" for rule in result)
    assert all(rule["source_name"] for rule in result)


def test_search_respects_category_filter():
    result = search_rules("الفاصلة", "punctuation")
    assert result
    assert all(rule["category"] == "punctuation" for rule in result)


def test_search_unknown_category_returns_no_results():
    assert search_rules("فاصلة", "unknown") == []
