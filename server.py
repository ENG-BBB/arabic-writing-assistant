"""MCP server for source-aware Arabic writing guidance."""

from mcp.server import MCPServer

from ambiguity import disambiguate_word as find_word_senses
from checker import audit_punctuation, prepare_review
from rules import search_rules


server = MCPServer(
    "Arabic Writing Assistant",
    instructions=(
        "Help users write and edit Modern Standard Arabic. For requested proofreading, "
        "inspect grammar, agreement, spelling, punctuation, quotation, and formatting. "
        "Use search_arabic_rules for applicable guidance and audit_arabic_punctuation "
        "for mechanical checks. When an unvowelled word may have different meanings, "
        "use disambiguate_arabic_word with sentence context. Add only the diacritic(s) "
        "on the letter(s) that distinguish the intended meaning; do not fully vocalize "
        "the word unless requested. The tool compares every catalogued candidate; if "
        "context rules out candidates, recompute the minimal marks among the remaining "
        "senses before replying. If context is insufficient, present alternatives "
        "or ask the user. Preserve the author's meaning and voice. Report each "
        "suggestion with the original, suggested edit, a short explanation, and a "
        "confidence label. Distinguish established conventions from style choices; "
        "do not invent a rule when the reference set is silent. Ask before changing "
        "dialect, register, or house style."
    ),
)


@server.tool()
def search_arabic_rules(query: str, category: str = "all") -> dict:
    """Search concise Arabic grammar, spelling, punctuation, quotation, and formatting guidance.

    Categories: all, grammar, spelling, punctuation, quotation, formatting.
    Returns sourced rules with examples and confidence labels.
    """
    return {"rules": search_rules(query, category)}


@server.tool()
def audit_arabic_punctuation(text: str) -> dict:
    """Check Arabic punctuation marks, their spacing, repeated marks, and paired delimiters.

    This is a mechanical check. It does not decide whether punctuation matches the intended meaning.
    """
    return audit_punctuation(text)


@server.tool()
def disambiguate_arabic_word(word: str, context: str = "") -> dict:
    """Find documented meanings of an ambiguous unvowelled Arabic word.

    Provide the sentence or phrase as context. The result shows only the short-vowel
    marks that distinguish candidate meanings, attached to the relevant letter(s).
    It does not add full diacritics or guess when the word is absent from the curated bank.
    """
    return find_word_senses(word, context)


@server.tool()
def review_arabic_text(text: str, style: str = "modern_standard") -> dict:
    """Prepare a full proofreading review of Arabic prose for the host model.

    Review syntax and grammar, agreement, spelling, punctuation, quotations, spacing,
    and ambiguous words that need selective diacritics,
    and document formatting. Returns the text, mechanical findings, review checklist,
    and sourced rules to consult. `style` is modern_standard for the initial release.
    """
    return prepare_review(text, style)


if __name__ == "__main__":
    server.run(transport="streamable-http", host="0.0.0.0", port=8000)
