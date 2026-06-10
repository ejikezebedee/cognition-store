from __future__ import annotations

import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from cognition_store.domains.agentshield.buyer_committee import run_demo as run_agentshield_demo
from cognition_store.domains.energy.market_simulation import run_energy_demo
from cognition_store.runtime.task_hook import run_task_completion_hook
from cognition_store.storage.json_store import read_json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATIC_ROOT = PROJECT_ROOT / "prototypes" / "saas-dashboard"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "artifacts" / "runs"


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    *,
    output_root: Path | None = None,
    static_root: Path | None = None,
) -> ThreadingHTTPServer:
    handler = _make_handler(output_root or DEFAULT_OUTPUT_ROOT, static_root or DEFAULT_STATIC_ROOT)
    return ThreadingHTTPServer((host, port), handler)


def serve(
    host: str = "127.0.0.1",
    port: int = 8765,
    *,
    output_root: Path | None = None,
    static_root: Path | None = None,
) -> None:
    server = create_server(host, port, output_root=output_root, static_root=static_root)
    print(f"Cognition Store dashboard: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def list_runs(output_root: Path) -> list[dict[str, Any]]:
    if not output_root.exists():
        return []
    runs: list[dict[str, Any]] = []
    for run_dir in sorted((path for path in output_root.iterdir() if path.is_dir()), key=lambda path: path.stat().st_mtime, reverse=True):
        summary = read_json(run_dir / "summary.json", {})
        verdict = read_json(run_dir / "verdict.json", {})
        manifest = read_json(run_dir / "manifest.json", {})
        runs.append(
            {
                "run_id": run_dir.name,
                "run_dir": _portable_path(run_dir),
                "domain": manifest.get("domain") or verdict.get("domain") or "local_runtime_learning",
                "question": manifest.get("question", ""),
                "summary": summary,
                "verdict": verdict,
                "counts": _counts_for_run(run_dir, summary),
            }
        )
    return runs


def create_memory_record(payload: dict[str, Any], output_root: Path) -> dict[str, Any]:
    notes = str(payload.get("notes") or "").strip()
    if not notes:
        raise ValueError("notes is required")
    title = str(payload.get("title") or "Memory record").strip()
    template = str(payload.get("template") or "Project decision").strip()
    project = str(payload.get("project") or title or template).strip()
    run_id = _safe_run_id(str(payload.get("run_id") or f"{_slug(template)}_{_slug(title)}"))
    summary = f"{template}: {title}. {notes}"
    return run_task_completion_hook(summary, project, output_root, run_id)


def _make_handler(output_root: Path, static_root: Path) -> type[BaseHTTPRequestHandler]:
    output_root = output_root.resolve()
    static_root = static_root.resolve()

    class CognitionStoreHandler(BaseHTTPRequestHandler):
        server_version = "CognitionStoreHTTP/0.3.1"

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                self._send_json({"status": "ok", "service": "cognition-store", "output_root": _portable_path(output_root)})
                return
            if parsed.path == "/api/runs":
                self._send_json({"runs": list_runs(output_root)})
                return
            self._serve_static(parsed.path, static_root)

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            try:
                payload = self._read_json_body()
                if parsed.path == "/api/records":
                    self._send_json(create_memory_record(payload, output_root), HTTPStatus.CREATED)
                    return
                if parsed.path == "/api/agentshield-demo":
                    self._send_json(run_agentshield_demo(output_root), HTTPStatus.CREATED)
                    return
                if parsed.path == "/api/energy-demo":
                    self._send_json(run_energy_demo(output_root), HTTPStatus.CREATED)
                    return
                self._send_json({"error": "not_found", "message": f"Unknown endpoint: {parsed.path}"}, HTTPStatus.NOT_FOUND)
            except ValueError as exc:
                self._send_json({"error": "bad_request", "message": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:  # pragma: no cover - defensive HTTP boundary
                self._send_json({"error": "server_error", "message": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _read_json_body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length <= 0:
                return {}
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError("request body must be valid JSON") from exc
            if not isinstance(payload, dict):
                raise ValueError("request body must be a JSON object")
            return payload

        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _serve_static(self, request_path: str, root: Path) -> None:
            relative = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
            candidate = (root / relative).resolve()
            if root not in candidate.parents and candidate != root:
                self.send_error(HTTPStatus.FORBIDDEN)
                return
            if candidate.is_dir():
                candidate = candidate / "index.html"
            if not candidate.exists() or not candidate.is_file():
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            body = candidate.read_bytes()
            content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return CognitionStoreHandler


def _counts_for_run(run_dir: Path, summary: dict[str, Any]) -> dict[str, int]:
    return {
        "evidence": int(summary.get("evidence_count") or _json_len(run_dir / "evidence_index.json")),
        "claims": int(summary.get("claim_count") or _json_len(run_dir / "claims.json")),
        "lessons": int(summary.get("lesson_count") or _json_len(run_dir / "lessons.json")),
        "approvals": int(summary.get("approval_draft_count") or _json_len(run_dir / "approval_drafts.json")),
        "events": int(summary.get("event_count") or _jsonl_len(run_dir / "actions.jsonl")),
    }


def _json_len(path: Path) -> int:
    value = read_json(path, [])
    return len(value) if isinstance(value, list) else 0


def _jsonl_len(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:40] or "record"


def _safe_run_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")[:64] or "memory_record"


def _portable_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name
