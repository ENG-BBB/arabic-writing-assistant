# Arabic Writing Assistant

An open MCP server for Arabic grammar guidance, punctuation, quotation marks, spelling, and editorial formatting. It is designed for AI hosts such as ChatGPT and Claude.

## What it does

- `search_arabic_rules`: find concise, sourced guidance by topic or question.
- `audit_arabic_punctuation`: flag mechanical punctuation and spacing issues.
- `disambiguate_arabic_word`: use context to distinguish documented meanings and show only the vowel marks on letters that change the meaning.
- `review_arabic_text`: provide a structured proofreading brief for a host model, including syntax, agreement, spelling, punctuation, quotation, and formatting checks.

The rule bank covers core syntax and inflection, spelling, punctuation, quotation, and editorial formatting. Each entry includes an original short summary, example, confidence label, source URL, and source name in search results. The bank is a curated starting point, not a claim that every Arabic grammar tradition or house style has one universal answer. The server distinguishes widely used conventions from style-dependent choices.

## Selective diacritics for ambiguous words

The disambiguation tool takes a word and its sentence context. It returns documented candidate meanings and marks only the letters whose vowels or shadda distinguish those meanings. Seed entries cover five unvowelled spellings: ملك (angel/ruler/sovereignty), علم (knowledge/flag; knew/taught), فهم (understood/explained), سلم (was safe/handed or greeted), and كتب (wrote/was written/books). Since ملك has three candidates, the marks on both م and ل distinguish all three; for only the angel/ruler pair, the distinction is on ل. The host model selects a candidate from context; if context is insufficient, it should show alternatives or ask rather than guess. This is selective disambiguation, not full tashkeel. The lexicon remains a seed set and each new entry needs a dictionary or reviewed grammatical source.

## Run locally

Requires Python 3.11+ and `uv`.

```sh
uv sync
uv run mcp dev server.py
```

For a deployed HTTP endpoint:

```sh
uv run python server.py
```

The server uses Streamable HTTP at `http://127.0.0.1:8000/mcp`. To expose it to a hosted assistant, deploy it behind HTTPS and follow that host's custom MCP setup. Claude Code can also run it locally over stdio with `uv run mcp run server.py`.

## Add it to Claude Code

```sh
claude mcp add --transport stdio arabic-writing -- uv run --directory "/path/to/Arabic Writing Assistant" mcp run server.py
```

## Rule sources

- [King Salman Global Academy for Arabic Language: *Spelling in the Arabic Writing System*](https://library.ksaa.gov.sa/links/epubs/aliimla_fi_nizam_alkitabat_alearabia.pdf)
- [King Salman Global Academy for Arabic Language: Arabic grammar curricula](https://library.ksaa.gov.sa/links/epubs/manahij_taelim_allughat_alearabiat_fi_aljamieat_alearabia.pdf)
- [Cairo Arabic Language Academy: definition of punctuation](https://www.arabicacademy.gov.eg/ar/%D9%85%D8%AD%D8%B1%D9%83-%D8%A7%D9%84%D8%A8%D8%AD%D8%AB/%D9%85%D8%B9%D8%AC%D9%85/dic-349/%D8%A7%D9%84%D8%AA%D8%B1%D9%82%D9%8A%D9%85)
- [Cairo Arabic Language Academy: roots علم، فهم، سلم، كتب، ملك](https://www.arabicacademy.gov.eg/ar/search_engine/roots)
- [Saudi Ministry of Health: editorial guide](https://www.moh.gov.sa/Documents/2019-11-24-002.pdf)
- [Saudi General Authority for Statistics: editorial policy](https://www.stats.gov.sa/documents/20117/2435069/%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9%2B%D8%A7%D9%84%D8%AA%D8%AD%D8%B1%D9%8A%D8%B1%D9%8A%D8%A9.pdf/3b2c0301-ffd4-8b1b-1916-c4b335deccf9?download=true&t=1729705430624)
- [Cairo Arabic Language Academy: root علم](https://www.arabicacademy.gov.eg/ar/search_engine/roots/%D8%B9%D9%84%D9%85)
- [Cairo Arabic Language Academy: الملك and الملك](https://www.arabicacademy.gov.eg/ar/%D9%85%D8%AD%D8%B1%D9%83-%D8%A7%D9%84%D8%A8%D8%AD%D8%AB/%D9%85%D8%B9%D8%AC%D9%85/%D8%A7%D9%84%D9%85%D9%8E%D9%84%D9%92%D9%83%D9%8F?exact_search=true)
- [Egyptian Ministry of Awqaf: punctuation overview and examples](https://awkafonline.gov.eg/content-sections/110/3217/%D8%B9%D9%84%D8%A7%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D8%B1%D9%82%D9%8A%D9%85)
- [Saudi General Authority for Statistics: editorial policy](https://www.stats.gov.sa/documents/20117/2435069/%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9%2B%D8%A7%D9%84%D8%AA%D8%AD%D8%B1%D9%8A%D8%B1%D9%8A%D8%A9.pdf/3b2c0301-ffd4-8b1b-1916-c4b335deccf9?download=true&t=1729705430624)

## Scope and style

The initial profile is Modern Standard Arabic. Regional dialects, academic citation formats, publishing house styles, and Qur'anic orthography need separate profiles. A host model should explain uncertain or style-dependent suggestions instead of silently rewriting them.

## Development

```sh
uv sync --extra dev
uv run python -m pytest
```

Rule contributions should include a short statement, at least one example, a directly relevant source, and a confidence label (`standard`, `common`, or `style-dependent`). Do not phrase a source-specific style choice as a universal grammar rule. For ambiguous-word entries, cite a dictionary or grammar source for every candidate meaning, include contextual examples, and verify that selective rendering adds marks only at positions where the candidate forms differ.
