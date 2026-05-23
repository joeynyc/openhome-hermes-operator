from hermes_operator.voice import make_voice_safe


def test_make_voice_safe_strips_markdown_and_collapses_whitespace():
    text = """# Result\n\n**Server** is   healthy.\n\n```bash\nsecret command\n```"""

    assert make_voice_safe(text) == "Result Server is healthy."


def test_make_voice_safe_preserves_urls_from_markdown_links():
    text = "Open [the app](http://192.168.1.201:7860) on your phone."

    assert make_voice_safe(text) == "Open the app, http://192.168.1.201:7860 on your phone."


def test_make_voice_safe_limits_long_text_at_sentence_boundary():
    text = "First sentence is useful. " + "second " * 200

    assert make_voice_safe(text, max_chars=80) == "First sentence is useful."


def test_make_voice_safe_handles_empty_text():
    assert make_voice_safe("   ") == "I finished, but there was no spoken summary."
