import httpx


class HermesClientError(RuntimeError):
    """Raised when Hermes API Server returns an unusable response."""


class HermesClient:
    def __init__(self, base_url: str, api_key: str, model: str = "hermes-agent", timeout: float = 180.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def run_task(self, task: str, session_id: str | None = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if session_id:
            headers["X-Hermes-Session-Id"] = session_id

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are speaking through an OpenHome voice device. Return a concise spoken result.",
                },
                {"role": "user", "content": task},
            ],
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)

        if response.status_code >= 400:
            raise HermesClientError(f"Hermes API returned HTTP {response.status_code}: {response.text[:300]}")

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise HermesClientError("Hermes API returned malformed chat completion response") from exc

        if not isinstance(content, str) or not content.strip():
            raise HermesClientError("Hermes API returned an empty assistant response")

        return content.strip()
