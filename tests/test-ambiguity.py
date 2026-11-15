from ambiguity import disambiguate_word


def variants_for(word, group=0):
    result = disambiguate_word(word, "جملة تجريبية")
    assert result["matches"]
    return result["matches"][group]["variants"]


def test_malik_lexicon_marks_only_the_contrastive_letters():
    variants = variants_for("ملك")
    assert [item["selective_form"] for item in variants] == ["مَلَك", "مَلِك", "مُلْك"]
    assert all(item["distinguishing_letters"] == ["م", "ل"] for item in variants)
    assert variants[0]["distinguishing_marks"][0]["mark_names"] == ["فتحة"]


def test_already_vowelled_input_still_matches():
    variants = variants_for("عَلِمَ", group=1)
    assert [item["selective_form"] for item in variants] == ["علِم", "علَّم"]
    assert variants[0]["distinguishing_letters"] == ["ل"]


def test_scientific_noun_and_flag_are_disambiguated():
    variants = variants_for("علم", group=0)
    assert [item["selective_form"] for item in variants] == ["عِلْم", "عَلَم"]
    assert variants[0]["distinguishing_letters"] == ["ع", "ل"]


def test_fahima_forms_differ_on_the_middle_letter():
    variants = variants_for("فهم")
    assert [item["selective_form"] for item in variants] == ["فهِم", "فهَّم"]
    assert all(item["distinguishing_letters"] == ["ه"] for item in variants)


def test_salama_forms_differ_on_the_middle_letter():
    variants = variants_for("سلم")
    assert [item["selective_form"] for item in variants] == ["سلِم", "سلَّم"]
    assert all(item["distinguishing_letters"] == ["ل"] for item in variants)


def test_kataba_forms_include_book_plural_and_mark_contrastive_letters():
    variants = variants_for("كتب")
    assert [item["selective_form"] for item in variants] == ["كَتَب", "كُتِب", "كُتُب"]
    assert all(item["distinguishing_letters"] == ["ك", "ت"] for item in variants)


def test_unknown_word_does_not_guess():
    result = disambiguate_word("مطر", "هطل المطر")
    assert result["matches"] == []
    assert "لا توجد" in result["message"]
