from fastapi.testclient import TestClient

from hermes_operator.app import create_app


class FakeHermesClient:
    def __init__(self, result="**Done**. Server is healthy."):
        self.result = result
        self.calls = []

    async def run_task(self, task, session_id=None):
        self.calls.append((task, session_id))
        return self.result


def test_health_endpoint_returns_ok():
    client = TestClient(create_app(FakeHermesClient()))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_run_endpoint_calls_hermes_and_returns_voice_safe_summary():
    fake = FakeHermesClient()
    client = TestClient(create_app(fake))

    response = client.post("/run", json={"task": "check server", "session_id": "voice-1"})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["spoken_summary"] == "Done. Server is healthy."
    assert fake.calls == [("check server", "voice-1")]


def test_run_endpoint_rejects_blank_task():
    client = TestClient(create_app(FakeHermesClient()))

    response = client.post("/run", json={"task": "   "})

    assert response.status_code == 422
