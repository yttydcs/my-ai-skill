import importlib.util
import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from uuid import UUID, uuid5

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/m-memory/scripts/memory_client.py"
CONTEXT = ROOT / "skills/m-context/scripts/context_loader.py"
spec = importlib.util.spec_from_file_location("memory_client", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
LIB = "11111111-1111-4111-8111-111111111111"
OTHER = "22222222-2222-4222-8222-222222222222"
REV = "33333333-3333-4333-8333-333333333333"


@pytest.fixture
def service(tmp_path):
    calls = []
    state = {"status": 200, "body": {"ok": True}}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond()

        def do_POST(self):
            self.respond()

        def respond(self):
            data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            calls.append((self.command, self.path, json.loads(data) if data else None))
            self.send_response(state["status"])
            self.send_header("Content-Type", "application/json")
            if state["status"] == 302:
                self.send_header(
                    "Location", f"http://127.0.0.1:{self.server.server_port}/redirected"
                )
            self.end_headers()
            self.wfile.write(json.dumps(state["body"], ensure_ascii=False).encode())

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    (tmp_path / "token").write_text("synthetic-client-test-token")
    path = tmp_path / "binding.json"
    config = {
        "version": 1,
        "backend": "agent-memory",
        "url": f"http://127.0.0.1:{server.server_port}",
        "token_file": "token",
        "read_libraries": [LIB],
        "write_library": LIB,
        "allowed_source_libraries": [LIB],
        "budget_bytes": 4096,
        "indexes": {LIB: {"id": OTHER, "revision": REV, "method": "bm25"}},
        "context_libraries": {"local": LIB},
    }
    path.write_text(json.dumps(config), encoding="utf-8")
    yield module.MemoryClient(path), state, calls, path, server
    server.shutdown()
    thread.join(5)
    server.server_close()


def run_context(path, *args):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    env.pop("M_MEMORY_BINDING", None)
    return subprocess.run(
        [sys.executable, str(CONTEXT), *args, "--memory-binding", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=15,
        check=False,
    )


def test_search_carries_selected_scope_and_index_without_writes(service):
    client, _, calls, _, _ = service
    client.search("导出", category="requirements")
    method, path, body = calls[0]
    assert method == "POST" and path.endswith("/document-search")
    assert body == {
        "method": "bm25",
        "expected_index_revision": REV,
        "query": "导出",
        "target": "both",
        "metadata_filter": {"category": "requirements"},
        "budget_bytes": 4096,
        "allowed_source_libraries": [LIB],
    }
    assert len(calls) == 1


@pytest.mark.parametrize(
    "path",
    [
        "../devices",
        "%2e%2e/devices",
        "objects?library=other",
        "//elsewhere",
        "objects\\..",
        "objects/#fragment",
    ],
)
def test_traversal_rejected_before_network(service, path):
    client, _, calls, _, _ = service
    with pytest.raises(module.MemoryError):
        client.request("GET", path)
    assert calls == []


def test_scope_budget_and_unguarded_archive_rejected(service):
    client, _, calls, _, _ = service
    for action in [
        lambda: client.read(REV, library=OTHER),
        lambda: client.search("x", extra={"allowed_source_libraries": [OTHER]}),
        lambda: client.request("GET", "objects", params={"libraries": [OTHER]}),
        lambda: client.search("x", extra={"budget_bytes": 9000}),
        lambda: client.search("x", extra={"method": "fts"}),
        lambda: client.commit(
            {"idempotency_key": "test-key", "operations": [{"action": "create"}]},
            archive=True,
        ),
        lambda: client.commit(
            {
                "idempotency_key": "test-key",
                "operations": [{"references": [{"target_library_id": OTHER}]}],
            }
        ),
    ]:
        with pytest.raises(module.MemoryError):
            action()
    assert not calls


def test_cas_and_lease_are_forwarded_unchanged(service):
    client, _, calls, _, _ = service
    body = {
        "idempotency_key": "one-logical-write",
        "operations": [
            {
                "action": "patch",
                "object_id": OTHER,
                "expected_revision": REV,
                "content": "保留人工摘要",
            }
        ],
        "lease_guard": {
            "name": "archive",
            "token": "synthetic-lease-token",
            "fence": 42,
        },
    }
    client.commit(body, archive=True)
    assert calls[0][2] == body


@pytest.mark.parametrize("status", [302, 403, 409, 503])
def test_errors_no_redirect_or_retry_and_no_cache(service, status):
    client, state, calls, path, _ = service
    state.update(status=status, body={"detail": "fixture_error"})
    before = set(path.parent.iterdir())
    with pytest.raises(module.MemoryError) as caught:
        client.read(OTHER)
    assert caught.value.status == status and len(calls) == 1
    assert set(path.parent.iterdir()) == before
    assert "synthetic-client-test-token" not in str(caught.value)


def test_oversized_response_and_revision_mismatch_fail(service):
    client, state, _, _, _ = service
    state["body"] = {"content": "x" * 5000}
    with pytest.raises(module.MemoryError, match="budget"):
        client.read(OTHER)
    state["body"] = {"revision": OTHER}
    with pytest.raises(module.MemoryError, match="revision changed"):
        client.read(OTHER, revision=REV)


def test_context_section_identity_and_no_local_fallback(service, tmp_path):
    _, state, calls, path, _ = service
    name = "部署偏好"
    state["body"] = {
        "kind": "source",
        "title": "context:" + name,
        "metadata": {"category": "context", "name": name},
        "revision": REV,
        "content": "# 部署\n只走私网\n## 端口\n8443\n# 其他\n不加载本节\n",
    }
    result = run_context(path, "load", name, "--section", "端口")
    assert result.returncode == 0, result.stderr
    assert "8443" in result.stdout and "其他" not in result.stdout
    assert str(uuid5(UUID(LIB), "m-context:" + name)) in calls[-1][1]
    assert REV in result.stderr and "local:" in result.stderr
    state.update(status=404, body={"detail": "object_not_found"})
    failed = run_context(path, "load", name)
    assert failed.returncode != 0 and failed.stdout == ""
    # Supplying file authority together with memory must fail before any request.
    count = len(calls)
    conflict = run_context(path, "load", name, "--docs-root", str(tmp_path))
    assert conflict.returncode != 0 and len(calls) == count


def test_context_discovery_reports_partial_page_and_scope(service):
    _, state, _, path, _ = service
    state["body"] = {
        "results": [
            {"kind": "source", "title": "context:部署偏好"},
            {"kind": "source", "title": "specs"},
        ],
        "truncated": True,
        "next_offset": 2,
    }
    result = run_context(path, "find", "部署")
    assert result.returncode == 0 and result.stdout.strip() == "local:部署偏好"
    assert "--offset 2" in result.stderr
    failed = run_context(path, "list", "--scope", "global")
    assert failed.returncode != 0 and not failed.stdout


def test_offline_context_does_not_use_local_files(service):
    _, _, _, path, server = service
    server.shutdown()
    server.server_close()
    result = run_context(path, "load", "missing")
    assert result.returncode != 0 and not result.stdout
    assert "no local fallback" in result.stderr


def test_read_only_and_multiple_libraries_require_explicit_choices(service):
    client, _, calls, path, _ = service
    config = client.config.copy()
    config.update(write_library=None, read_libraries=[LIB, OTHER])
    path.write_text(json.dumps(config), encoding="utf-8")
    selected = module.MemoryClient(path)
    with pytest.raises(module.MemoryError, match="read-only"):
        selected.commit(
            {"idempotency_key": "fixture-key", "operations": [{"action": "create"}]}
        )
    with pytest.raises(module.MemoryError, match="explicitly"):
        selected.search("x")
    assert not calls


@pytest.mark.parametrize(
    "url",
    [
        "http://192.0.2.1:8765",
        "https://user:secret@example.test",
        "https://example.test/path",
        "https://example.test?key=secret",
    ],
)
def test_unsafe_origin_rejected_before_reading_credentials(service, url):
    client, _, calls, path, _ = service
    config = {**client.config, "url": url, "token_file": "absent-token"}
    path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(module.MemoryError, match="HTTPS origin"):
        module.MemoryClient(path)
    assert not calls


@pytest.mark.parametrize(
    "value", [[], None, {"version": 1, "backend": "agent-memory", "url": 42}]
)
def test_malformed_binding_is_an_explicit_error(tmp_path, value):
    path = tmp_path / "binding.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(module.MemoryError, match="invalid or unreadable"):
        module.MemoryClient(path)
