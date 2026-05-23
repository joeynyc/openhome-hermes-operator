import httpx
import pytest

from hermes_operator.client import HermesClient, HermesClientError


@pytest.mark.asyncio
async def test_run_task_posts_openai_compatible_request(monkeypatch):
    captured = {}

    async def fake_post(self, url, headers=None, json=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Server is healthy."}}]},
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    client = HermesClient("http://127.0.0.1:8642/v1", "secret", "hermes-agent")
    result = await client.run_task("check server", session_id="voice-1")

    assert result == "Server is healthy."
    assert captured["url"] == "http://127.0.0.1:8642/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["headers"]["X-Hermes-Session-Id"] == "voice-1"
    assert captured["json"]["model"] == "hermes-agent"
    assert captured["json"]["messages"][-1] == {"role": "user", "content": "check server"}


@pytest.mark.asyncio
async def test_run_task_raises_on_http_error(monkeypatch):
    async def fake_post(self, url, headers=None, json=None):
        return httpx.Response(500, text="boom")

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    client = HermesClient("http://127.0.0.1:8642/v1", "secret")
    with pytest.raises(HermesClientError, match="HTTP 500"):
        await client.run_task("check server")


@pytest.mark.asyncio
async def test_run_task_raises_on_malformed_response(monkeypatch):
    async def fake_post(self, url, headers=None, json=None):
        return httpx.Response(200, json={"bad": "shape"})

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    client = HermesClient("http://127.0.0.1:8642/v1", "secret")
    with pytest.raises(HermesClientError, match="malformed"):
        await client.run_task("check server")
