from checker import audit_punctuation, prepare_review


def test_well_spaced_arabic_punctuation_has_no_findings():
    result = audit_punctuation("قرأتُ الدرس، ثم حللتُ التمارين.")
    assert result["findings"] == []


def test_flags_space_before_punctuation_and_missing_space_after():
    result = audit_punctuation("مرحبًا ،كيف حالك")
    codes = {finding["code"] for finding in result["findings"]}
    assert "space-before-punctuation" in codes
    assert "missing-space-after-punctuation" in codes


def test_flags_repeated_punctuation():
    result = audit_punctuation("ما أجمل هذا!!!")
    assert any(finding["code"] == "repeated-punctuation" for finding in result["findings"])


def test_flags_unpaired_quote():
    result = audit_punctuation("قال: «مرحبًا")
    assert any(finding["code"] == "unclosed-delimiter" for finding in result["findings"])


def test_review_includes_rules_and_scope_note():
    result = prepare_review("إن العلم نافع.")
    assert result["review_checklist"]
    assert result["reference_rules"]
    assert result["mechanical_audit"]["not_checked"]
    assert "السياق" in result["scope_note"]


def test_review_rejects_unsupported_style_explicitly():
    result = prepare_review("كيف حالك؟", "dialect")
    assert result["supported_styles"] == ["modern_standard"]
