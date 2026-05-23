import re

_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MARKDOWN_CHARS_RE = re.compile(r'[*_`#>"]')
_WHITESPACE_RE = re.compile(r"\s+")


def make_voice_safe(text: str, max_chars: int = 700) -> str:
    cleaned = _CODE_FENCE_RE.sub(" ", text or "")
    cleaned = _MARKDOWN_LINK_RE.sub(r"\1, \2", cleaned)
    cleaned = _MARKDOWN_CHARS_RE.sub("", cleaned)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned).strip()

    if len(cleaned) <= max_chars:
        return cleaned or "I finished, but there was no spoken summary."

    truncated = cleaned[: max_chars + 1]
    sentence_end = max(truncated.rfind(". "), truncated.rfind("! "), truncated.rfind("? "))
    if sentence_end > 0:
        return truncated[: sentence_end + 1].strip()
    return cleaned[:max_chars].rstrip() + "..."
