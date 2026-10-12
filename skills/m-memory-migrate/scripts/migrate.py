"""Preview, resume and verify explicit Markdown source migrations; no local body cache."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from uuid import UUID, uuid4, uuid5

COMPANION = Path(__file__).resolve().parents[2] / "m-memory/scripts/memory_client.py"
spec = importlib.util.spec_from_file_location("migration_memory_client", COMPANION)
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)

TRANSIENT = {
    "plan",
    "plans",
    "todo",
    "context",
    "contexts",
    "logs",
    "log",
    "node_modules",
    "__pycache__",
    "venv",
    "dist",
    "build",
}
LOCAL_NAMES = {"plan.md", "todo.md", "agents.md", "review.md"}
CATEGORIES = {
    "intake",
    "features",
    "requirements",
    "specs",
    "decisions",
    "lessons",
    "change",
}
MAX_SOURCE = 1024 * 1024


class MigrationError(Exception):
    pass


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode()
    ).hexdigest()


def object_id(library, collection, path):
    identity = json.dumps(
        ["migrate", collection, path], ensure_ascii=False, separators=(",", ":")
    )
    return str(uuid5(UUID(library), identity))


def file_hash(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            result.update(chunk)
    return result.hexdigest()


def linked(path):
    return (
        path.is_symlink()
        or getattr(path, "is_junction", lambda: False)()
        or path.resolve() != path.absolute()
    )


def inventory(root, files=None):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise MigrationError("source root must be a directory")
    entries, deferred = [], []

    if files is not None:
        if not isinstance(files, list) or not files:
            raise MigrationError("explicit file scope must be a nonempty list")
        seen = set()
        for name in files:
            if not isinstance(name, str):
                raise MigrationError("explicit file paths must be strings")
            relative = Path(name)
            if (
                relative.is_absolute()
                or relative.drive
                or ".." in relative.parts
                or relative.as_posix() != name
                or ":" in name
            ):
                raise MigrationError(
                    "explicit files must use normalized root-relative paths"
                )
            if name.casefold() in seen:
                raise MigrationError("duplicate explicit file")
            seen.add(name.casefold())
            path = root / relative
            if (
                not path.is_file()
                or path.suffix.casefold() != ".md"
                or path.name.casefold() in LOCAL_NAMES
                or any(p.startswith(".") for p in relative.parts)
                or any(p.casefold() in TRANSIENT for p in relative.parts[:-1])
            ):
                raise MigrationError("explicit file is missing or excluded")
            cursor = path
            while cursor != root:
                if linked(cursor):
                    raise MigrationError("linked source paths are excluded")
                cursor = cursor.parent
            entries.append(
                {"path": name, "sha256": file_hash(path), "bytes": path.stat().st_size}
            )
        return sorted(entries, key=lambda x: x["path"]), deferred

    def walk_error(error):
        raise MigrationError(
            "source directory cannot be enumerated completely"
        ) from error

    for parent, dirs, filenames in os.walk(root, followlinks=False, onerror=walk_error):
        for name in list(dirs):
            path = Path(parent) / name
            if name.startswith(".") or name.casefold() in TRANSIENT or linked(path):
                dirs.remove(name)
                deferred.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "reason": "excluded_directory",
                    }
                )
        for name in filenames:
            path = Path(parent) / name
            rel = path.relative_to(root).as_posix()
            if name.startswith(".") or name.casefold() in LOCAL_NAMES or linked(path):
                deferred.append({"path": rel, "reason": "excluded_file"})
            elif path.suffix.casefold() != ".md":
                deferred.append(
                    {"path": rel, "reason": "non_markdown_manual_disposition"}
                )
            else:
                entries.append(
                    {
                        "path": rel,
                        "sha256": file_hash(path),
                        "bytes": path.stat().st_size,
                    }
                )
    return sorted(entries, key=lambda x: x["path"]), sorted(
        deferred, key=lambda x: x["path"]
    )


def outside(path, root):
    resolved = Path(path).resolve()
    if resolved == root or root in resolved.parents:
        raise MigrationError("manifest and journal must be outside the source tree")
    return resolved


def save(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    try:
        with temporary.open("x", encoding="utf-8") as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def preview(root, client, collection, manifest, files=None):
    root = Path(root).resolve(strict=True)
    target = outside(manifest, root)
    if target.exists():
        raise MigrationError("manifest already exists; choose a new output path")
    if not collection.strip():
        raise MigrationError("collection must be a stable nonempty project label")
    library = client.library(write=True)
    client.library(library)
    rows, deferred = inventory(root, files)
    entries = []
    for row in rows:
        categories = [
            part for part in Path(row["path"]).parts[:-1] if part in CATEGORIES
        ]
        entries.append(
            {
                **row,
                "selected": False,
                "category": categories[0] if categories else None,
                "title": Path(row["path"]).stem,
                "object_id": object_id(library, collection, row["path"]),
            }
        )
    data = {
        "version": 1,
        "migration_id": str(uuid4()),
        "root": str(root),
        "url": client.url,
        "library": library,
        "collection": collection,
        "inventory": rows,
        "entries": entries,
        "deferred": deferred,
    }
    if files is not None:
        data["files"] = sorted(files)
    save(target, data)
    return {
        "status": "preview",
        "candidates": len(entries),
        "selected": 0,
        "deferred": len(deferred),
        "manifest": str(target),
    }


def scan(root, manifest, files=None):
    root = Path(root).resolve(strict=True)
    target = outside(manifest, root)
    if target.exists():
        raise MigrationError("inventory output already exists")
    rows, deferred = inventory(root, files)
    save(
        target,
        {
            "version": "inventory-only",
            "root": str(root),
            "inventory": rows,
            "deferred": deferred,
            "files": files,
        },
    )
    return {
        "status": "local_inventory",
        "candidates": len(rows),
        "deferred": len(deferred),
        "manifest": str(target),
        "target": "not_selected",
    }


def preflight(data, client):
    if (
        data["version"] != 1
        or client.url != data["url"]
        or client.library(write=True) != data["library"]
    ):
        raise MigrationError(
            "binding service/library differs from the migration manifest"
        )
    client.library(data["library"])
    root = Path(data["root"]).resolve(strict=True)
    current, deferred = inventory(root, data.get("files"))
    if current != data["inventory"] or deferred != data["deferred"]:
        raise MigrationError(
            "source inventory changed; review a new manifest before continuing"
        )
    expected = {row["path"]: row for row in current}
    seen = set()
    selected = []
    for row in data["entries"]:
        name = row["path"]
        if name in seen or name not in expected:
            raise MigrationError("duplicate or out-of-inventory path")
        seen.add(name)
        for key in ("sha256", "bytes"):
            if row[key] != expected[name][key]:
                raise MigrationError("entry content identity differs from inventory")
        identity = object_id(data["library"], data["collection"], name)
        if row["object_id"] != identity or type(row["selected"]) is not bool:
            raise MigrationError(
                "invalid selected flag or deterministic object identity"
            )
        if not row["selected"]:
            continue
        if (
            row["category"] not in CATEGORIES
            or not isinstance(row["title"], str)
            or not 1 <= len(row["title"]) <= 300
        ):
            raise MigrationError("selected sources require a valid category and title")
        if row["bytes"] > MAX_SOURCE:
            raise MigrationError("source exceeds one MiB; split and review explicitly")
        source_bytes(data, row).decode("utf-8")
        selected.append(row)
    if seen != expected.keys() or not selected:
        raise MigrationError(
            "manifest must retain its full inventory and select at least one source"
        )
    return selected


def source_bytes(data, row):
    root = Path(data["root"]).resolve(strict=True)
    relative = Path(row["path"])
    if relative.is_absolute() or relative.drive or ".." in relative.parts:
        raise MigrationError("unsafe source path")
    source = root / relative
    cursor = source
    while cursor != root:
        if linked(cursor):
            raise MigrationError("linked source paths are excluded")
        cursor = cursor.parent
    resolved = source.resolve(strict=True)
    if root not in resolved.parents:
        raise MigrationError("source escapes selected root")
    body = resolved.read_bytes()
    if len(body) != row["bytes"] or hashlib.sha256(body).hexdigest() != row["sha256"]:
        raise MigrationError(
            "source changed after preview; no write attempted for this file"
        )
    return body


def verify_object(client, library, row, revision):
    hasher, position = hashlib.sha256(), 0
    while True:
        part = client.request(
            "GET",
            f"objects/{row['object_id']}/chunk",
            library=library,
            params={"start_byte": position},
        )
        if part["revision"] != revision or part["object_id"] != row["object_id"]:
            raise MigrationError("remote object revision changed; do not overwrite it")
        chunk = part["chunk"].encode("utf-8")
        end = position + len(chunk)
        if (
            part["start_byte"] != position
            or part["end_byte"] != end
            or part["total_bytes"] != row["bytes"]
            or end > row["bytes"]
        ):
            raise MigrationError("invalid source chunk boundaries")
        hasher.update(chunk)
        if part["next_start_byte"] is None:
            if end != row["bytes"]:
                raise MigrationError("incomplete remote source")
            break
        if not chunk or part["next_start_byte"] != end:
            raise MigrationError("source chunk did not advance")
        position = end
    if hasher.hexdigest() != row["sha256"]:
        raise MigrationError("remote content hash mismatch")


def execute(manifest, client, journal, *, verify_only=False):
    data = json.loads(Path(manifest).read_text(encoding="utf-8-sig"))
    root = Path(data["root"]).resolve(strict=True)
    outside(manifest, root)
    journal = outside(journal, root)
    if journal == Path(manifest).resolve():
        raise MigrationError("journal must differ from manifest")
    fingerprint = digest(data)
    state = None
    if journal.exists():
        state = json.loads(journal.read_text(encoding="utf-8"))
        if state["manifest_sha256"] != fingerprint:
            raise MigrationError(
                "manifest changed since migration began; preserve the original journal"
            )
        state["status"] = "in_progress"
        save(journal, state)
    rows = preflight(data, client)
    if state is None:
        if verify_only:
            raise MigrationError("verification requires the original import journal")
        state = {"manifest_sha256": fingerprint, "status": "in_progress", "objects": {}}
        save(journal, state)
    for row in rows:
        identity = row["object_id"]
        entry = state["objects"].get(identity)
        if entry and entry.get("revision"):
            verify_object(client, data["library"], row, entry["revision"])
            continue
        if verify_only:
            raise MigrationError("selected source has no completed import receipt")
        key = "migration-" + digest([fingerprint, identity])
        if entry and entry["idempotency_key"] != key:
            raise MigrationError("journal receipt identity mismatch")
        receipt = None
        if entry:
            try:
                receipt = client.request(
                    "GET", f"commits/{key}", library=data["library"]
                )
            except memory.MemoryError as error:
                if error.status != 404:
                    raise
        if receipt is None:
            body = source_bytes(data, row).decode("utf-8")
            operation = {
                "action": "create",
                "object_id": identity,
                "kind": "source",
                "title": row["title"],
                "content": body,
                "metadata": {
                    "category": row["category"],
                    "migration": {
                        "collection": data["collection"],
                        "path": row["path"],
                        "sha256": row["sha256"],
                    },
                },
            }
            state["objects"][identity] = {"idempotency_key": key, "status": "pending"}
            save(journal, state)
            receipt = client.commit(
                {"idempotency_key": key, "operations": [operation]},
                library=data["library"],
            )
        # The receipt lookup endpoint returns the stored result, same as commit.
        results = receipt["results"]
        if (
            len(results) != 1
            or results[0]["object_id"] != identity
            or results[0]["action"] != "created"
        ):
            raise MigrationError("unexpected import receipt")
        revision = str(UUID(results[0]["revision"]))
        verify_object(client, data["library"], row, revision)
        state["objects"][identity] = {
            "idempotency_key": key,
            "status": "verified",
            "revision": revision,
            "sha256": row["sha256"],
        }
        save(journal, state)
    preflight(data, client)
    state["status"] = "sources_verified"
    state["verified_count"] = len(rows)
    state["remaining"] = (
        "Agent must assess references, summaries, attachments and authority cutover"
    )
    save(journal, state)
    return {
        "status": state["status"],
        "verified": len(rows),
        "journal": str(journal),
        "cutover": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    first = sub.add_parser("preview")
    first.add_argument("--root", required=True)
    first.add_argument("--collection", required=True)
    first.add_argument(
        "--file",
        action="append",
        help="Exact root-relative Markdown path; repeat to limit scope without traversing other directories",
    )
    for name in ("apply", "verify"):
        command = sub.add_parser(name)
        command.add_argument("--journal", required=True)
    for command in sub.choices.values():
        command.add_argument("--manifest", required=True)
        command.add_argument("--binding", required=True)
    local = sub.add_parser(
        "scan", help="Inventory sources before a target library exists"
    )
    local.add_argument("--root", required=True)
    local.add_argument("--manifest", required=True)
    local.add_argument("--file", action="append")
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            print(
                json.dumps(
                    scan(args.root, args.manifest, args.file), ensure_ascii=False
                )
            )
            return 0
        client = memory.MemoryClient(args.binding)
        if args.command == "preview":
            result = preview(
                args.root, client, args.collection, args.manifest, args.file
            )
        else:
            result = execute(
                args.manifest,
                client,
                args.journal,
                verify_only=args.command == "verify",
            )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (
        MigrationError,
        memory.MemoryError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
    ) as error:
        message = (
            str(error)
            if isinstance(error, (MigrationError, memory.MemoryError))
            else f"invalid input or inaccessible source ({type(error).__name__})"
        )
        print(
            f"m-memory-migrate: {message}; stopped, no cleanup or cutover",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
