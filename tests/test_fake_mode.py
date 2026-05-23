from fastapi.testclient import TestClient

from hermes_operator.app import create_app


class ExplodingHermesClient:
    async def run_task(self, task, session_id=None):
        raise AssertionError("fake mode should not call Hermes client")


def test_fake_mode_returns_success_without_calling_hermes(monkeypatch):
    monkeypatch.setenv("HERMES_OPERATOR_FAKE_MODE", "true")
    monkeypatch.delenv("HERMES_OPERATOR_TOKEN", raising=False)
    client = TestClient(create_app(ExplodingHermesClient()))

    response = client.post("/run", json={"task": "check server"})

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "spoken_summary": "Hermes fake mode is working. I received: check server",
        "raw_text": "Hermes fake mode is working. I received: check server",
        "artifact_path": None,
    }
