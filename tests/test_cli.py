import json

from hermes_operator.cli import build_headers, make_payload, summarize_response


def test_build_headers_includes_bearer_token_when_present():
    headers = build_headers("secret")

    assert headers == {
        "content-type": "application/json",
        "Authorization": "Bearer secret",
    }


def test_build_headers_omits_authorization_when_token_blank():
    assert build_headers("") == {"content-type": "application/json"}


def test_make_payload_preserves_task_and_session():
    assert make_payload("check server", "voice-local") == {
        "task": "check server",
        "session_id": "voice-local",
    }


def test_summarize_response_returns_spoken_summary_for_success():
    body = json.dumps({"ok": True, "spoken_summary": "Server is healthy."})

    assert summarize_response(body) == "Server is healthy."


def test_summarize_response_returns_failure_summary():
    body = json.dumps({"ok": False, "spoken_summary": "Hermes failed."})

    assert summarize_response(body) == "Hermes failed."
