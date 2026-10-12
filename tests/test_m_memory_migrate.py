import importlib.util
import json
from pathlib import Path
from uuid import uuid4

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1] / "skills/m-memory-migrate/scripts/migrate.py"
)
spec = importlib.util.spec_from_file_location("migrate", SCRIPT)
migrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migrate)
LIBRARY = "55555555-5555-4555-8555-555555555555"


def test_explicit_scope_does_not_walk_unselected_trees(tmp_path, monkeypatch):
    root = tmp_path / "mixed"
    root.mkdir()
    (root / "REQUIREMENTS.md").write_text("approved source", encoding="utf-8")
    (root / "runtime").mkdir()
    (root / "runtime/private.md").write_text("unselected", encoding="utf-8")

    def no_walk(*args, **kwargs):
        raise AssertionError("explicit selection must not walk the root")

    monkeypatch.setattr(migrate.os, "walk", no_walk)
    manifest, journal = tmp_path / "manifest.json", tmp_path / "journal.json"
    server = Server()
    migrate.preview(root, server, "mixed", manifest, ["REQUIREMENTS.md"])
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["entries"][0].update(selected=True, category="requirements")
    manifest.write_text(json.dumps(data), encoding="utf-8")
    (root / "runtime/new.md").write_text("out of scope")
    assert migrate.execute(manifest, server, journal)["verified"] == 1
    (root / "REQUIREMENTS.md").write_text("changed")
    with pytest.raises(migrate.MigrationError, match="inventory changed"):
        migrate.execute(manifest, server, journal, verify_only=True)
    assert server.writes == 1


@pytest.mark.parametrize(
    "files",
    [
        [],
        ["../escape.md"],
        ["C:/outside.md"],
        ["plan.md"],
        ["context/private.md"],
        ["missing.md"],
        ["REQUIREMENTS.md", "REQUIREMENTS.md"],
        ["./REQUIREMENTS.md"],
    ],
)
def test_explicit_scope_rejects_unsafe_or_excluded_files(tmp_path, files):
    (tmp_path / "REQUIREMENTS.md").write_text("source")
    (tmp_path / "plan.md").write_text("local")
    (tmp_path / "context").mkdir()
    (tmp_path / "context/private.md").write_text("private")
    with pytest.raises(migrate.MigrationError):
        migrate.inventory(tmp_path, files)


class Server:
    url = "https://fixture.invalid"

    def __init__(self):
        self.objects = {}
        self.receipts = {}
        self.writes = 0
        self.lose_response = False
        self.stall = False

    def library(self, selected=None, write=False):
        assert selected in {None, LIBRARY}
        return LIBRARY

    def commit(self, body, library=None):
        key = body["idempotency_key"]
        if key in self.receipts:
            return self.receipts[key]
        operation = body["operations"][0]
        identity = operation["object_id"]
        if identity in self.objects:
            raise migrate.memory.MemoryError("object_exists", 409)
        assert operation["action"] == "create" and operation["kind"] == "source"
        revision = str(uuid4())
        self.objects[identity] = {**operation, "revision": revision}
        result = {
            "results": [
                {"object_id": identity, "revision": revision, "action": "created"}
            ]
        }
        self.receipts[key] = result
        self.writes += 1
        if self.lose_response:
            self.lose_response = False
            raise migrate.memory.MemoryError("connection lost after commit")
        return result

    def request(self, method, path, *, library=None, params=None):
        assert method == "GET" and library == LIBRARY
        if path.startswith("commits/"):
            key = path.split("/")[1]
            if key not in self.receipts:
                raise migrate.memory.MemoryError("commit_not_found", 404)
            return self.receipts[key]
        identity = path.split("/")[1]
        document = self.objects[identity]
        content = document["content"].encode("utf-8")
        start = params["start_byte"]
        text = content[start:].decode("utf-8")[:3]
        if self.stall:
            text = ""
        end = start + len(text.encode())
        return {
            "object_id": identity,
            "revision": document["revision"],
            "start_byte": start,
            "end_byte": end,
            "total_bytes": len(content),
            "chunk": text,
            "next_start_byte": end if end < len(content) else None,
        }


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "docs"
    (root / "specs").mkdir(parents=True)
    (root / "specs/a.md").write_bytes("# 限制\r\n最多45分钟。\r\n".encode())
    (root / "specs/b.md").write_bytes(b"")
    (root / "context").mkdir()
    (root / "context/private.md").write_text("do not import fixture credential")
    (root / "plan.md").write_text("execution only")
    (root / "image.png").write_bytes(b"opaque fixture")
    server = Server()
    manifest, journal = tmp_path / "manifest.json", tmp_path / "journal.json"
    migrate.preview(root, server, "project", manifest)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for row in data["entries"]:
        row["selected"] = True
    manifest.write_text(json.dumps(data), encoding="utf-8")
    return root, server, manifest, journal


def test_preview_excludes_transient_context_and_reports_attachments(source):
    _, server, manifest, _ = source
    data = json.loads(manifest.read_text())
    assert [r["path"] for r in data["entries"]] == ["specs/a.md", "specs/b.md"]
    assert {r["path"] for r in data["deferred"]} == {"context", "plan.md", "image.png"}
    assert server.writes == 0 and "credential" not in manifest.read_text()


def test_source_only_scan_needs_no_binding_or_service(source, capsys):
    root, server, manifest, _ = source
    target = manifest.with_name("source-only.json")
    result = migrate.main(["scan", "--root", str(root), "--manifest", str(target)])
    assert result == 0 and server.writes == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "local_inventory" and output["target"] == "not_selected"
    assert json.loads(target.read_text())["version"] == "inventory-only"


def test_import_roundtrip_resume_and_journal_contains_no_bodies(source):
    root, server, manifest, journal = source
    assert migrate.execute(manifest, server, journal)["verified"] == 2
    assert migrate.execute(manifest, server, journal)["verified"] == 2
    assert migrate.execute(manifest, server, journal, verify_only=True)["verified"] == 2
    assert server.writes == 2
    assert (root / "specs/a.md").read_bytes().decode() == next(
        iter(server.objects.values())
    )["content"]
    assert "最多45" not in journal.read_text(encoding="utf-8")
    assert not (root / "binding.json").exists()


def test_lost_commit_response_resumes_from_receipt_without_duplicate(source):
    _, server, manifest, journal = source
    server.lose_response = True
    with pytest.raises(migrate.memory.MemoryError, match="connection lost"):
        migrate.execute(manifest, server, journal)
    assert server.writes == 1
    assert migrate.execute(manifest, server, journal)["verified"] == 2
    assert server.writes == 2


def test_source_changes_prevent_any_import(source):
    root, server, manifest, journal = source
    (root / "specs/a.md").write_text("new source")
    with pytest.raises(migrate.MigrationError, match="inventory changed"):
        migrate.execute(manifest, server, journal)
    assert server.writes == 0 and not journal.exists()


def test_new_source_file_is_detected_even_if_other_sources_unchanged(source):
    root, server, manifest, journal = source
    (root / "specs/new.md").write_text("new source")
    with pytest.raises(migrate.MigrationError, match="inventory changed"):
        migrate.execute(manifest, server, journal)
    assert server.writes == 0


def test_manifest_cannot_be_changed_mid_migration(source):
    _, server, manifest, journal = source
    server.lose_response = True
    with pytest.raises(migrate.memory.MemoryError):
        migrate.execute(manifest, server, journal)
    data = json.loads(manifest.read_text())
    data["entries"][0]["title"] = "different title"
    manifest.write_text(json.dumps(data))
    with pytest.raises(migrate.MigrationError, match="manifest changed"):
        migrate.execute(manifest, server, journal)
    assert server.writes == 1


def test_remote_edit_is_not_overwritten(source):
    _, server, manifest, journal = source
    migrate.execute(manifest, server, journal)
    document = next(iter(server.objects.values()))
    document.update(content="concurrent edit", revision=str(uuid4()))
    with pytest.raises(migrate.MigrationError, match="revision changed"):
        migrate.execute(manifest, server, journal, verify_only=True)
    assert document["content"] == "concurrent edit" and server.writes == 2
    assert json.loads(journal.read_text())["status"] == "in_progress"


def test_local_drift_invalidates_previous_verification_status(source):
    root, server, manifest, journal = source
    migrate.execute(manifest, server, journal)
    (root / "specs/a.md").write_text("local change")
    with pytest.raises(migrate.MigrationError, match="inventory changed"):
        migrate.execute(manifest, server, journal, verify_only=True)
    assert json.loads(journal.read_text())["status"] == "in_progress"


def test_existing_objects_are_not_adopted_or_overwritten(source):
    _, server, manifest, journal = source
    data = json.loads(manifest.read_text())
    identity = data["entries"][0]["object_id"]
    server.objects[identity] = {"content": "existing truth"}
    with pytest.raises(migrate.memory.MemoryError, match="object_exists"):
        migrate.execute(manifest, server, journal)
    assert (
        server.objects[identity]["content"] == "existing truth" and server.writes == 0
    )


def test_stalled_chunks_stop_instead_of_looping(source):
    _, server, manifest, journal = source
    server.stall = True
    with pytest.raises(migrate.MigrationError, match="did not advance"):
        migrate.execute(manifest, server, journal)


def test_unsafe_paths_cannot_be_added_to_manifest(source):
    _, server, manifest, journal = source
    data = json.loads(manifest.read_text())
    data["entries"][0]["path"] = "../outside.md"
    manifest.write_text(json.dumps(data))
    with pytest.raises(migrate.MigrationError, match="out-of-inventory"):
        migrate.execute(manifest, server, journal)
    assert server.writes == 0


def test_no_selection_and_output_inside_source_are_rejected(source):
    root, server, manifest, journal = source
    with pytest.raises(migrate.MigrationError, match="outside"):
        migrate.preview(root, server, "project", root / "migration.json")
    data = json.loads(manifest.read_text())
    for row in data["entries"]:
        row["selected"] = False
    manifest.write_text(json.dumps(data))
    with pytest.raises(migrate.MigrationError, match="select at least one"):
        migrate.execute(manifest, server, journal)
