from cognition_store.governance.approval_gate import requires_approval
from cognition_store.governance.secret_redactor import has_secret_marker, redact_text


def test_secret_detection_and_redaction():
    assert has_secret_marker("api_key=abc123")
    assert "[REDACTED]" in redact_text("api_key=abc123")


def test_approval_gate():
    assert requires_approval("production_change")
    assert not requires_approval("local_simulation")

