import os

from fastapi import FastAPI, Header, HTTPException

from hermes_operator.client import HermesClient, HermesClientError
from hermes_operator.models import OperatorRequest, OperatorResponse
from hermes_operator.voice import make_voice_safe


def build_client() -> HermesClient:
    return HermesClient(
        base_url=os.getenv("HERMES_API_BASE_URL", "http://127.0.0.1:8642/v1"),
        api_key=os.getenv("HERMES_API_KEY", "local"),
        model=os.getenv("HERMES_API_MODEL", "hermes-agent"),
    )


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _require_bearer_token(authorization: str | None) -> None:
    expected_token = os.getenv("HERMES_OPERATOR_TOKEN", "").strip()
    if not expected_token:
        return

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")

    actual_token = authorization.removeprefix("Bearer ").strip()
    if actual_token != expected_token:
        raise HTTPException(status_code=403, detail="invalid bearer token")


def create_app(client: HermesClient | None = None) -> FastAPI:
    app = FastAPI(title="OpenHome Hermes Operator Bridge")
    hermes_client = client or build_client()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/run", response_model=OperatorResponse)
    async def run_operator_task(
        request: OperatorRequest,
        authorization: str | None = Header(default=None),
    ) -> OperatorResponse:
        _require_bearer_token(authorization)

        if _truthy(os.getenv("HERMES_OPERATOR_FAKE_MODE")):
            raw_text = f"Hermes fake mode is working. I received: {request.task}"
            return OperatorResponse(ok=True, spoken_summary=make_voice_safe(raw_text), raw_text=raw_text)

        try:
            raw_text = await hermes_client.run_task(request.task, session_id=request.session_id)
        except HermesClientError as exc:
            return OperatorResponse(ok=False, spoken_summary="I could not reach Hermes successfully.", raw_text=str(exc))

        return OperatorResponse(ok=True, spoken_summary=make_voice_safe(raw_text), raw_text=raw_text)

    return app


app = create_app()
