import os

from fastapi import FastAPI

from hermes_operator.client import HermesClient, HermesClientError
from hermes_operator.models import OperatorRequest, OperatorResponse
from hermes_operator.voice import make_voice_safe


def build_client() -> HermesClient:
    return HermesClient(
        base_url=os.getenv("HERMES_API_BASE_URL", "http://127.0.0.1:8642/v1"),
        api_key=os.getenv("HERMES_API_KEY", "local"),
        model=os.getenv("HERMES_API_MODEL", "hermes-agent"),
    )


def create_app(client: HermesClient | None = None) -> FastAPI:
    app = FastAPI(title="OpenHome Hermes Operator Bridge")
    hermes_client = client or build_client()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/run", response_model=OperatorResponse)
    async def run_operator_task(request: OperatorRequest) -> OperatorResponse:
        try:
            raw_text = await hermes_client.run_task(request.task, session_id=request.session_id)
        except HermesClientError as exc:
            return OperatorResponse(ok=False, spoken_summary="I could not reach Hermes successfully.", raw_text=str(exc))

        return OperatorResponse(ok=True, spoken_summary=make_voice_safe(raw_text), raw_text=raw_text)

    return app


app = create_app()
