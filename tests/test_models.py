import pytest
from pydantic import ValidationError

from hermes_operator.models import OperatorRequest, OperatorResponse


def test_operator_request_strips_task_whitespace():
    req = OperatorRequest(task="  check the model server  ")

    assert req.task == "check the model server"


def test_operator_request_rejects_blank_task():
    with pytest.raises(ValidationError):
        OperatorRequest(task="   ")


def test_operator_response_allows_optional_raw_fields():
    resp = OperatorResponse(ok=True, spoken_summary="Done.")

    assert resp.ok is True
    assert resp.spoken_summary == "Done."
    assert resp.raw_text is None
    assert resp.artifact_path is None
