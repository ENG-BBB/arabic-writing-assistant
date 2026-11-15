"""Mechanical Arabic typography checks; linguistic judgment stays with the host model."""

import re

from rules import RULES, search_rules

PUNCTUATION = set("،؛؟.!:…")
OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}", "«": "»", "“": "”"}
QUOTE_PAIRS = [("«", "»"), ("“", "”"), ("\"", "\""), ("'", "'")]


def _finding(code: str, message: str, start: int, end: int, suggestion: str | None = None) -> dict:
    item = {"code": code, "message": message, "start": start, "end": end}
    if suggestion:
        item["suggestion"] = suggestion
    return item


def audit_punctuation(text: str) -> dict:
    findings = []

    for match in re.finditer(r"[ \t]+([،؛؟.!:…])", text):
        findings.append(_finding(
            "space-before-punctuation",
            "توجد مسافة قبل علامة الترقيم؛ تحذف عادةً في النثر العربي.",
            match.start(), match.end(), match.group(1),
        ))

    for match in re.finditer(r"([،؛؟.!:…])(?=\S)", text):
        following = text[match.end():match.end() + 1]
        if following in "»”)]}،؛؟.!:…" or match.group(1) == "…":
            continue
        findings.append(_finding(
            "missing-space-after-punctuation",
            "إذا استمر النص بعد العلامة، أضف مسافة للفصل بين الكلمات أو الجمل.",
            match.start(), match.end() + 1, match.group(1) + " " + following,
        ))

    for match in re.finditer(r"([!?؟.،؛!])\1+", text):
        findings.append(_finding(
            "repeated-punctuation",
            "تكرار العلامة قد لا يناسب الأسلوب التحريري؛ تحقّق من دليل الأسلوب المقصود.",
            match.start(), match.end(), match.group(1),
        ))

    stack = []
    for index, char in enumerate(text):
        if char in OPEN_TO_CLOSE:
            stack.append((char, index))
        elif char in OPEN_TO_CLOSE.values():
            if not stack or OPEN_TO_CLOSE[stack[-1][0]] != char:
                findings.append(_finding(
                    "unmatched-closing-delimiter", "علامة إغلاق بلا علامة فتح مطابقة.", index, index + 1,
                ))
            else:
                stack.pop()
    for char, index in stack:
        findings.append(_finding(
            "unclosed-delimiter", f"علامة الفتح {char} بلا علامة إغلاق مطابقة.", index, index + 1,
        ))

    for opening, closing in QUOTE_PAIRS:
        if opening == closing:
            count = text.count(opening)
            if count % 2:
                index = text.rfind(opening)
                findings.append(_finding(
                    "unpaired-quotation-mark", "عدد علامات التنصيص المستقيمة فردي؛ تحقق من الاقتباس.", index, index + 1,
                ))
        elif text.count(opening) != text.count(closing):
            findings.append(_finding(
                "unpaired-quotation-mark", f"تحقق من توازن علامتي التنصيص {opening}{closing}.", 0, len(text),
            ))

    return {
        "findings": findings,
        "checked": ["spacing", "repeated punctuation", "parentheses", "quotation mark pairing"],
        "not_checked": ["whether punctuation matches intended meaning", "grammar", "spelling", "factual accuracy", "text direction and layout in the host application"],
    }


def prepare_review(text: str, style: str = "modern_standard") -> dict:
    if style != "modern_standard":
        return {"error": "النمط المدعوم حاليًا هو العربية الفصحى الحديثة فقط.", "supported_styles": ["modern_standard"]}
    relevant_rules = [
        rule for rule in RULES
        if rule["category"] in {"grammar", "spelling", "quotation", "formatting"}
    ]
    relevant_rules += search_rules("الترقيم الفاصلة الاستفهام التنصيص", "punctuation")
    return {
        "text": text,
        "style": style,
        "mechanical_audit": audit_punctuation(text),
        "review_checklist": [
            "النحو: تركيب الجمل، المطابقة، الضمائر، وحروف الجر والعطف.",
            "الإملاء: الهمزات، الألف اللينة، التاء، التنوين، والوصل والفصل.",
            "الترقيم: هل تعكس العلامات المعنى؟ وهل مواضعها ومسافاتها سليمة؟",
            "التنصيص: هل الاقتباس حرفي؟ وهل العلامتان متطابقتان؟",
            "التنسيق: اتساق العناوين والقوائم، واتجاه الفقرات (RTL للعربية)، وعزل الروابط والأكواد اللاتينية، والأرقام والمسافات.",
            "احفظ المعنى والنبرة، وميّز التصحيح المؤكد من الاقتراح الأسلوبي.",
        ],
        "reference_rules": relevant_rules,
        "response_format": ["الموضع", "النص الأصلي", "المقترح", "السبب", "درجة الثقة"],
        "scope_note": "التدقيق الآلي هنا يفحص التنسيق السطحي فقط؛ النحو والإملاء الدلالي يحتاجان إلى مراجعة النموذج والسياق.",
    }
