# Arabic Writing Assistant

**مساعد للكتابة العربية يعمل عبر MCP**، يقدّم إرشادًا لغويًا موثقًا ويفحص الترقيم، والتنصيص، والتنسيق. يستطيع المستخدم ربطه بعميل ذكاء اصطناعي يدعم MCP.

**A source-aware Arabic writing assistant over MCP.** It provides language guidance, punctuation checks, quotation and formatting help, and selective diacritics for a small curated set of ambiguous words.

## بالعربية

### ماذا يقدم؟

- البحث عن قواعد عربية مع أمثلة وروابط للمصادر.
- فحص آلي محدود للمسافات وعلامات الترقيم والأقواس والتنصيص.
- عرض معاني بعض الكلمات الملتبسة، مع التشكيل على الحروف التي تميّز المعنى فقط.
- إعداد قائمة مراجعة تساعد النموذج المضيف على تدقيق النص. الحكم النحوي والدلالي النهائي يعتمد على النموذج والسياق، وليس على فحص آلي كامل.
- توجيه تنسيق الفقرات العربية RTL، وعزل الروابط والأكواد والمقاطع اللاتينية باتجاه LTR عند إنشاء HTML أو مستند منسق.

بنك القواعد والكلمات الملتبسة **بداية قابلة للتوسعة**، وليس مرجعًا شاملًا لكل مدارس النحو أو أدلة الأسلوب. مدخلات الالتباس الحالية تشمل خمس كلمات غير مضبوطة بالشكل: ملك، علم، فهم، سلم، كتب. نضيف المداخل مع مصادر مباشرة ومراجعة مناسبة.

### تشغيل سريع

يتطلب Python 3.11 أو أحدث و[uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/ENG-BBB/arabic-writing-assistant.git
cd arabic-writing-assistant
uv sync
uv run mcp dev server.py
```

للتشغيل مع عميل محلي يستخدم stdio:

```sh
uv run mcp run server.py
```

ولتشغيل واجهة HTTP محليًا:

```sh
uv run python server.py
```

يوجد شرح ربط Claude وChatGPT والعملاء الأخرى في [Integration Guide](Integration%20Guide.md).

### أمثلة لطلبات

- «ابحث عن قاعدة كتابة الهمزة المتوسطة مع مثال.»
- «افحص علامات الترقيم والمسافات في هذا النص.»
- «ما المعاني المحتملة لكلمة ملك في هذه الجملة؟»
- «راجع النص، وميّز التصحيح اللغوي المؤكد من الاقتراح الأسلوبي.»

## English

### What it does

- Searches a curated bank of Arabic grammar, spelling, punctuation, quotation, and formatting guidance.
- Checks mechanical punctuation patterns, spacing, and paired delimiters.
- Looks up documented meanings for selected ambiguous unvowelled words and marks only letters that distinguish candidate meanings.
- Prepares a sourced proofreading checklist for the connected host model.
- Provides guidance for right-to-left Arabic blocks and isolated left-to-right snippets in mixed-script HTML.

This is an actively maintained starting set, not a complete grammar authority. The current ambiguous-word bank covers five spellings: ملك, علم, فهم, سلم, and كتب. The host model makes context-sensitive language judgments; the server does not perform a complete automatic grammar analysis.

### Quick start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/ENG-BBB/arabic-writing-assistant.git
cd arabic-writing-assistant
uv sync
uv run mcp dev server.py
```

See the [Integration Guide](Integration%20Guide.md) for client-specific setup instructions.

## Available tools

- `search_arabic_rules`: search sourced guidance by topic or category.
- `audit_arabic_punctuation`: flag mechanical punctuation, spacing, repeated marks, and unmatched delimiters.
- `disambiguate_arabic_word`: return documented candidate meanings and selective diacritics.
- `review_arabic_text`: prepare a review checklist and relevant source rules for the host model.

The punctuation audit does not determine whether punctuation matches the intended meaning. The review tool returns guidance for the host model; it does not independently guarantee a correct proofread.

## Sources

Rule entries return source names and URLs. The bank draws on these references:

- [King Salman Global Academy for Arabic Language: spelling in the Arabic writing system](https://library.ksaa.gov.sa/links/epubs/aliimla_fi_nizam_alkitabat_alearabia.pdf)
- [King Salman Global Academy for Arabic Language: Arabic grammar curricula](https://library.ksaa.gov.sa/links/epubs/manahij_taelim_allughat_alearabiat_fi_aljamieat_alearabia.pdf)
- [Cairo Arabic Language Academy: punctuation definition](https://www.arabicacademy.gov.eg/ar/%D9%85%D8%AD%D8%B1%D9%83-%D8%A7%D9%84%D8%A8%D8%AD%D8%AB/%D9%85%D8%B9%D8%AC%D9%85/dic-349/%D8%A7%D9%84%D8%AA%D8%B1%D9%82%D9%8A%D9%85)
- [Cairo Arabic Language Academy: root search](https://www.arabicacademy.gov.eg/ar/search_engine/roots)
- [Saudi Ministry of Health: editorial guide](https://www.moh.gov.sa/Documents/2019-11-24-002.pdf)
- [Saudi General Authority for Statistics: editorial policy](https://www.stats.gov.sa/documents/20117/2435069/%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9%2B%D8%A7%D9%84%D8%AA%D8%AD%D8%B1%D9%8A%D8%B1%D9%8A%D8%A9.pdf/3b2c0301-ffd4-8b1b-1916-c4b335deccf9?download=true&t=1729705430624)
- [Egyptian Ministry of Awqaf: punctuation overview and examples](https://awkafonline.gov.eg/content-sections/110/3217/%D8%B9%D9%84%D8%A7%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D8%B1%D9%82%D9%8A%D9%85)
- [W3C: Authoring HTML for right-to-left scripts](https://www.w3.org/International/docs/bp-html-bidi/)
- [W3C: Inline markup and bidirectional text in HTML](https://www.w3.org/International/articles/inline-bidi-markup/)
- [Unicode: Unicode Bidirectional Algorithm, UAX #9](https://www.unicode.org/reports/tr9/)

## Text direction and mixed scripts

For structured HTML documents, set the base direction on Arabic blocks, for example `<p lang="ar" dir="rtl">…</p>`. Direction is separate from right alignment. Keep code, URLs, email addresses, and Latin identifiers left-to-right and isolate them from surrounding Arabic, for example `<bdi dir="ltr">https://example.com</bdi>`; use `<bdi dir="auto">` for unknown-direction inline content. Do not reverse characters manually. Avoid directional override controls such as RLO/LRO unless a specific, reviewed use requires them.

This MCP server returns text and formatting guidance; the host application controls how plain-text results are displayed. The punctuation audit does not verify visual RTL layout.

## Data handling and security

The application code has no database or file-writing logic and does not call an external model or language API. It processes text supplied for a tool call and returns language guidance. The connected AI client also receives the text under that service's own data policies.

The HTTP server currently has no authentication or rate limiting. Keep it on localhost or use a private tunnel unless you add appropriate access controls before exposing a hosted endpoint. Hosting providers may keep operational logs according to their own settings and policies; review those settings before deployment. Do not send confidential text to a hosted instance until you have reviewed its data handling.

## Scope

The initial profile is Modern Standard Arabic. Dialects, academic citation systems, publisher-specific styles, and Qur'anic orthography need separate profiles. When a source is silent or a choice depends on house style, the tool should say so rather than present one preference as a universal rule.

## Contributing

Rule contributions should include a short statement, at least one example, a directly relevant source, and a confidence label (`standard`, `common`, or `style-dependent`). For ambiguous-word entries, cite a dictionary or grammar source for every candidate meaning and verify that selective rendering marks only the letters that distinguish the candidate forms.

## License

This project is licensed under the [MIT License](LICENSE).
