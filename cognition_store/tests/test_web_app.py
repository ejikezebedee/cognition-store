import json
from pathlib import Path
from urllib import request

from cognition_store.web_app import create_memory_record, create_server, list_runs


def test_create_memory_record_writes_artifacts(tmp_path: Path):
    result = create_memory_record(
        {
            "title": "Launch review",
            "template": "Project decision",
            "notes": "Delivered launch plan. Verified smoke test passed. Production changes require approval.",
        },
        tmp_path,
    )

    run_dir = tmp_path / "project-decision_launch-review"
    assert result["lesson_count"] >= 3
    assert result["approval_draft_count"] >= 1
    assert (run_dir / "summary.json").exists()
    assert (run_dir / "approval_drafts.json").exists()


def test_list_runs_returns_counts(tmp_path: Path):
    create_memory_record(
        {
            "title": "Risk review",
            "template": "Compliance review",
            "notes": "Verified review passed. Contract changes require approval.",
        },
        tmp_path,
    )

    runs = list_runs(tmp_path)

    assert len(runs) == 1
    assert runs[0]["counts"]["evidence"] >= 2
    assert runs[0]["counts"]["approvals"] >= 1


def test_http_health_and_record_creation(tmp_path: Path):
    server = create_server(port=0, output_root=tmp_path)
    host, port = server.server_address
    import threading

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with request.urlopen(f"http://{host}:{port}/api/health", timeout=5) as response:
            health = json.loads(response.read().decode("utf-8"))
        assert health["status"] == "ok"

        body = json.dumps(
            {
                "title": "HTTP record",
                "template": "AI work log",
                "notes": "Delivered HTTP API. Verified tests passed. External communication requires approval.",
            }
        ).encode("utf-8")
        req = request.Request(
            f"http://{host}:{port}/api/records",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=5) as response:
            created = json.loads(response.read().decode("utf-8"))
        assert response.status == 201
        assert created["lesson_count"] >= 3

        with request.urlopen(f"http://{host}:{port}/api/runs", timeout=5) as response:
            runs = json.loads(response.read().decode("utf-8"))["runs"]
        assert len(runs) == 1
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
