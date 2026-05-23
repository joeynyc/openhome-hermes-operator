from pydantic import BaseModel, Field, field_validator


class OperatorRequest(BaseModel):
    task: str = Field(..., min_length=1)
    session_id: str | None = None
    require_confirmation: bool = True
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("task")
    @classmethod
    def task_must_not_be_blank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("task must not be blank")
        return normalized


class OperatorResponse(BaseModel):
    ok: bool
    spoken_summary: str
    raw_text: str | None = None
    artifact_path: str | None = None
