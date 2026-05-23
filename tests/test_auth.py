from fastapi.testclient import TestClient

from hermes_operator.app import create_app


class FakeHermesClient:
    async def run_task(self, task, session_id=None):
        return "Hermes finished."


def test_run_allows_request_when_token_not_configured(monkeypatch):
    monkeypatch.delenv("HERMES_OPERATOR_TOKEN", raising=False)
    client = TestClient(create_app(FakeHermesClient()))

    response = client.post("/run", json={"task": "check server"})

    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_run_rejects_request_when_token_configured_but_missing(monkeypatch):
    monkeypatch.setenv("HERMES_OPERATOR_TOKEN", "secret-token")
    client = TestClient(create_app(FakeHermesClient()))

    response = client.post("/run", json={"task": "check server"})

    assert response.status_code == 401
    assert response.json()["detail"] == "missing bearer token"


def test_run_rejects_request_when_token_is_wrong(monkeypatch):
    monkeypatch.setenv("HERMES_OPERATOR_TOKEN", "secret-token")
    client = TestClient(create_app(FakeHermesClient()))

    response = client.post(
        "/run",
        headers={"Authorization": "Bearer wrong"},
        json={"task": "check server"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "invalid bearer token"


def test_run_accepts_request_when_token_is_correct(monkeypatch):
    monkeypatch.setenv("HERMES_OPERATOR_TOKEN", "secret-token")
    client = TestClient(create_app(FakeHermesClient()))

    response = client.post(
        "/run",
        headers={"Authorization": "Bearer secret-token"},
        json={"task": "check server"},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
