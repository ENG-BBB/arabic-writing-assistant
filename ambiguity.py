"""Curated, source-linked homograph and word-form disambiguation examples."""

import unicodedata

MARK_ORDER = {"ّ": 0, "َ": 1, "ُ": 1, "ِ": 1, "ْ": 1, "ً": 1, "ٌ": 1, "ٍ": 1, "ٰ": 2}
MARK_NAMES = {"َ": "فتحة", "ُ": "ضمة", "ِ": "كسرة", "ْ": "سكون", "ّ": "شدة", "ً": "تنوين فتح", "ٌ": "تنوين ضم", "ٍ": "تنوين كسر", "ٰ": "ألف خنجرية"}


ENTRIES = [
    {
        "lemma": "ملك",
        "source": "https://www.arabicacademy.gov.eg/ar/محرك-البحث/معجم/المَلْكُ?exact_search=true",
        "variants": [
            {"form": "مَلَك", "meaning": "واحد الملائكة.", "example": "نزل المَلَكُ بالوحي."},
            {"form": "مَلِك", "meaning": "صاحب الأمر والسلطة على أمة أو بلاد.", "example": "حكم المَلِكُ البلادَ."},
            {"form": "مُلْك", "meaning": "الحكم والسلطان أو ما يملكه المرء، بحسب السياق.", "example": "انتقل مُلْكُ العقار إلى الورثة."},
        ],
    },
    {
        "lemma": "علم",
        "source": "https://www.arabicacademy.gov.eg/ar/search_engine/roots/علم",
        "variants": [
            {"form": "عِلْم", "meaning": "معرفة الشيء وإدراكه.", "example": "طلبتُ العِلْمَ في صغري."},
            {"form": "عَلَم", "meaning": "علامة أو راية بحسب السياق.", "example": "رُفع عَلَمُ الدولة فوق المبنى."},
        ],
    },
    {
        "lemma": "علم",
        "source": "https://www.arabicacademy.gov.eg/ar/search_engine/roots/علم",
        "variants": [
            {"form": "عَلِمَ", "meaning": "عرف الشيء وأدركه.", "example": "عَلِمَ الطالبُ الجوابَ."},
            {"form": "عَلَّمَ", "meaning": "جعله يتعلم؛ درّسه.", "example": "عَلَّمَ المعلمُ الطالبَ القراءةَ."},
        ],
    },
    {
        "lemma": "فهم",
        "source": "https://www.arabicacademy.gov.eg/ar/search_engine/roots/فهم",
        "variants": [
            {"form": "فَهِمَ", "meaning": "أحسن تصور الأمر وأدركه.", "example": "فَهِمَ الطالبُ المسألةَ."},
            {"form": "فَهَّمَ", "meaning": "أفهمه الأمر؛ جعله يفهمه.", "example": "فَهَّمَ المعلمُ الطالبَ المسألةَ."},
        ],
    },
    {
        "lemma": "سلم",
        "source": "https://www.arabicacademy.gov.eg/ar/search_engine/roots/سلم",
        "variants": [
            {"form": "سَلِمَ", "meaning": "برئ من الآفة أو نجا من الخطر.", "example": "سَلِمَ المسافرُ من الحادث."},
            {"form": "سَلَّمَ", "meaning": "حيّا بالسلام، أو أعطى الشيءَ وأوصله، بحسب السياق.", "example": "سَلَّمَ الموظفُ الرسالةَ إلى صاحبها."},
        ],
    },
    {
        "lemma": "كتب",
        "source": "https://www.arabicacademy.gov.eg/ar/search_engine/roots/كتب",
        "variants": [
            {"form": "كَتَب", "meaning": "خطّ الكلام وسطره؛ فعل معلوم.", "example": "كَتَبَ المحررُ الخبرَ."},
            {"form": "كُتِب", "meaning": "خُطَّ أو سُطِّر؛ فعل مبني للمجهول.", "example": "كُتِبَ الخبرُ أمس."},
            {"form": "كُتُب", "meaning": "جمع كتاب.", "example": "وضعتُ الكُتُبَ على الرف."},
        ],
    },
]


def strip_marks(value: str) -> str:
    return "".join(
        char for char in value
        if not (unicodedata.category(char) == "Mn" or char == "ـ")
    ).strip()


def split_marks(value: str) -> list[tuple[str, tuple[str, ...]]]:
    parts: list[list] = []
    for char in value:
        if unicodedata.category(char) == "Mn":
            if parts:
                parts[-1][1].append(char)
        elif char != "ـ":
            parts.append([char, []])
    return [
        (letter, tuple(sorted(marks, key=lambda mark: MARK_ORDER.get(mark, 3))))
        for letter, marks in parts
    ]


def selective_forms(variants: list[dict]) -> list[dict]:
    """Render only vowel marks that differ between the listed forms."""
    parsed = [split_marks(item["form"]) for item in variants]
    if not parsed or any(len(parts) != len(parsed[0]) for parts in parsed):
        return [{**item, "selective_form": item["form"], "distinguishing_letters": []} for item in variants]

    changed_positions = set()
    for position in range(len(parsed[0])):
        mark_sets = {parts[position][1] for parts in parsed}
        if len(mark_sets) > 1:
            changed_positions.add(position)

    rendered = []
    for item, parts in zip(variants, parsed):
        selective = []
        changed_letters = []
        distinguishing_marks = []
        for position, (letter, marks) in enumerate(parts):
            selective.append(letter)
            if position in changed_positions:
                selective.extend(marks)
                changed_letters.append(letter)
                distinguishing_marks.append({
                    "letter": letter,
                    "marks": "".join(marks),
                    "mark_names": [MARK_NAMES.get(mark, "علامة تشكيل") for mark in marks] or ["بلا حركة ظاهرة"],
                })
        rendered.append({
            **item,
            "selective_form": "".join(selective),
            "distinguishing_letters": changed_letters,
            "distinguishing_marks": distinguishing_marks,
        })
    return rendered


def disambiguate_word(word: str, context: str = "") -> dict:
    """Find curated senses and expose only the marks that distinguish them."""
    key = strip_marks(word).replace(" ", "")
    matching = [entry for entry in ENTRIES if strip_marks(entry["lemma"]) == key]
    if not matching:
        return {
            "word": word,
            "context": context,
            "matches": [],
            "message": "لا توجد لهذه الكلمة مداخل موثقة في بنك الالتباس الحالي؛ لا تستنتج ضبطًا بلا قرينة أو مصدر.",
        }

    results = []
    for entry in matching:
        results.append({
            "lemma": entry["lemma"],
            "source": entry["source"],
            "source_name": "مجمع اللغة العربية بالقاهرة",
            "variants": selective_forms(entry["variants"]),
        })
    return {
        "word": word,
        "context": context,
        "matches": results,
        "selection_policy": (
            "السياق أُرسل للمساعد المضيف ليختار المعنى. أظهر فقط العلامات على الحروف "
            "التي تميّز الصيغ، ولا تضبط بقية الكلمة إلا إذا طلب المستخدم التشكيل الكامل. "
            "الصيغة الانتقائية المعادة تقارن جميع مرشحات المدخل؛ إذا استبعد السياق بعض "
            "المعاني، فأعد المقارنة بين المرشحات الباقية لتجنب تشكيل حرف مشترك بينها."
        ),
    }
