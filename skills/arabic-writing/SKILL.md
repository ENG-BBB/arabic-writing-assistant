---
name: arabic-writing
description: Review Arabic grammar, spelling, punctuation, quotation, formatting, and ambiguous-word diacritics with sourced guidance.
---

# Arabic Writing Assistant

Use this plugin when the user asks for Arabic proofreading, language rules, punctuation, quotation, formatting, or meanings of ambiguous unvowelled Arabic words.

- For a full review, call `review_arabic_text` and present the original, proposed correction, reason, and confidence.
- Call `search_arabic_rules` for a specific rule; preserve the returned source and distinguish common conventions from style preferences.
- Call `audit_arabic_punctuation` for mechanical punctuation and spacing only. Do not describe it as a complete grammar checker.
- Call `disambiguate_arabic_word` with sentence context. Show only marks that distinguish the remaining meanings. If context is insufficient, show alternatives or ask; do not guess or add full diacritics unless requested.
- Preserve the author's meaning and voice. The current profile is Modern Standard Arabic; ask before changing dialect or house style.
- When creating formatted HTML, set Arabic blocks to RTL and isolate Latin links, identifiers, email addresses, and code as LTR. The host application's plain-text display direction is outside this server's control.
