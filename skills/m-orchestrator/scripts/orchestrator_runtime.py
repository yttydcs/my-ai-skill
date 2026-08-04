#!/usr/bin/env python3
"""Deterministic local runtime for project-scoped m-orchestrator state."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import tomllib
from typing import Any, Iterator
import uuid


SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = {1, 2}
TASK_MANIFEST_VERSION = 1
CONFIG_RELATIVE_PATH = Path(".codex") / "m-orchestrator.toml"
EXPECTED_COMMANDS = {
    "discuss": "m-discuss",
    "plan": "m-plan",
    "execute": "m-execute",
    "test": "m-test",
    "archive": "m-archive",
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
LEASE_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")
CONTEXT_PATTERN = re.compile(r"^local:([^/\\#]+)(?:#([^/\\#]+))?$")
TERMINAL_STATES = {"COMPLETED"}
STATES = {
    "PLANNED",
    "DISPATCHING",
    "EXECUTING",
    "EXECUTE_GATE_FAILED",
    "WAITING_FOR_TESTER",
    "TESTING",
    "TEST_FAILED",
    "TEST_PASSED",
    "WAITING_FOR_MERGE",
    "ARCHIVING",
    "COMPLETED",
    "BLOCKED",
}
NORMAL_TRANSITIONS = {
    "PLANNED": {"DISPATCHING"},
    "DISPATCHING": set(),
    "EXECUTING": {"EXECUTE_GATE_FAILED", "WAITING_FOR_TESTER", "WAITING_FOR_MERGE"},
    "EXECUTE_GATE_FAILED": {"EXECUTING"},
    "WAITING_FOR_TESTER": {"TESTING"},
    "TESTING": {"TEST_FAILED", "TEST_PASSED"},
    "TEST_FAILED": {"EXECUTING"},
    "TEST_PASSED": {"WAITING_FOR_MERGE"},
    "WAITING_FOR_MERGE": {"ARCHIVING"},
    "ARCHIVING": {"COMPLETED"},
    "COMPLETED": set(),
    "BLOCKED": STATES - {"COMPLETED", "BLOCKED"},
}
LOCK_TIMEOUT_SECONDS = 5.0
LOCK_STALE_SECONDS = 30.0


class OrchestratorError(RuntimeError):
    pass


@dataclass(frozen=True)
class RepositoryConfig:
    repository_id: str
    root: Path
    base_branch: str
    git_common_dir: Path


@dataclass(frozen=True)
class ProjectConfig:
    project_root: Path
    config_path: Path
    raw: dict[str, Any]
    schema_version: int
    project_id: str
    docs_root: Path
    base_branch: str | None
    environment_namespace: str
    commands: dict[str, dict[str, Any]]
    pools: dict[str, dict[str, Any]]
    host_budget: dict[str, Any] | None
    repositories: dict[str, RepositoryConfig]
    git_common_dir: Path | None
    runtime_root: Path
    config_fingerprint: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise OrchestratorError(f"Invalid runtime timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise OrchestratorError(f"Runtime timestamp has no timezone: {value}")
    return parsed.astimezone(timezone.utc)


def lease_age_seconds(
    lease: dict[str, Any], now: datetime | None = None
) -> tuple[float, int]:
    heartbeat = parse_time(require_string(lease.get("heartbeat_at"), "lease heartbeat_at"))
    timeout = require_int(
        lease.get("lease_timeout_seconds"), "lease_timeout_seconds", 60, 86400
    )
    observed_at = now or datetime.now(timezone.utc)
    return (observed_at - heartbeat).total_seconds(), timeout


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OrchestratorError(f"{label} must be a TOML table")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OrchestratorError(f"{label} must be a non-empty string")
    return value.strip()


def require_int(value: Any, label: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise OrchestratorError(f"{label} must be an integer")
    if not minimum <= value <= maximum:
        raise OrchestratorError(
            f"{label} must be between {minimum} and {maximum}; got {value}"
        )
    return value


def reject_unknown_keys(table: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise OrchestratorError(f"{label} contains unsupported keys: {', '.join(unknown)}")


def paths_identical(first: Path, second: Path) -> bool:
    try:
        return first.samefile(second)
    except OSError:
        return os.path.normcase(str(first.resolve())) == os.path.normcase(str(second.resolve()))


def validate_identifier(value: Any, label: str, pattern: re.Pattern[str]) -> str:
    identifier = require_string(value, label)
    if not pattern.fullmatch(identifier):
        raise OrchestratorError(f"{label} contains unsafe characters: {identifier}")
    return identifier


def validate_context_selector(value: Any, label: str) -> str:
    selector = require_string(value, label)
    match = CONTEXT_PATTERN.fullmatch(selector)
    if not match or match.group(1) in {".", ".."}:
        raise OrchestratorError(
            f"{label} must use explicit local:<name> or local:<name>#<section> syntax"
        )
    return selector


def resolve_docs_root(project_root: Path, value: Any) -> Path:
    text = require_string(value, "docs_root")
    candidate = Path(text)
    if not candidate.is_absolute() and ".." in candidate.parts:
        raise OrchestratorError("Relative docs_root must not contain traversal segments")
    resolved = candidate.resolve() if candidate.is_absolute() else (project_root / candidate).resolve()
    if not resolved.is_dir():
        raise OrchestratorError(f"docs_root directory does not exist: {resolved}")
    return resolved


def run_git(repository_root: Path, arguments: list[str], label: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(repository_root), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "unknown Git error"
        raise OrchestratorError(f"{label}: {detail}")
    return process.stdout.strip()


def resolve_git_repository(repository_root: Path, label: str) -> Path:
    top_level = Path(
        run_git(repository_root, ["rev-parse", "--show-toplevel"], f"{label} is not a valid Git repository")
    ).resolve()
    if not paths_identical(top_level, repository_root.resolve()):
        raise OrchestratorError(
            f"{label} must point to the Git worktree root; resolved top level is {top_level}"
        )
    raw_path = Path(
        run_git(repository_root, ["rev-parse", "--git-common-dir"], f"Cannot resolve {label} Git common directory")
    )
    resolved = raw_path.resolve() if raw_path.is_absolute() else (repository_root / raw_path).resolve()
    if not resolved.is_dir():
        raise OrchestratorError(f"{label} Git common directory does not exist: {resolved}")
    return resolved


def resolve_git_common_dir(project_root: Path) -> Path:
    return resolve_git_repository(project_root, "project_root")


def resolve_repository_root(project_root: Path, value: Any, label: str) -> Path:
    text = require_string(value, f"{label}.path")
    candidate = Path(text)
    if candidate.is_absolute():
        raise OrchestratorError(f"{label}.path must be relative to project_root")
    if ".." in candidate.parts:
        raise OrchestratorError(f"{label}.path must not contain traversal segments")
    resolved = (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root)
    except ValueError as exc:
        raise OrchestratorError(f"{label}.path resolves outside project_root: {resolved}") from exc
    if not resolved.is_dir():
        raise OrchestratorError(f"{label}.path directory does not exist: {resolved}")
    return resolved


def validate_base_ref(repository_root: Path, base_branch: str, label: str) -> None:
    run_git(
        repository_root,
        ["rev-parse", "--verify", f"{base_branch}^{{commit}}"],
        f"{label}.base_branch does not resolve to a commit",
    )


def normalize_fingerprint(raw: dict[str, Any]) -> str:
    encoded = json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def load_config(project_root: str | os.PathLike[str]) -> ProjectConfig:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise OrchestratorError(f"Project root does not exist: {root}")
    config_path = root / CONFIG_RELATIVE_PATH
    if not config_path.is_file():
        raise OrchestratorError(f"Orchestrator config does not exist: {config_path}")
    try:
        raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise OrchestratorError(f"Cannot read orchestrator config {config_path}: {exc}") from exc

    schema_version = raw.get("schema_version")
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise OrchestratorError("schema_version must be an integer")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise OrchestratorError(
            f"schema_version must be one of {sorted(SUPPORTED_SCHEMA_VERSIONS)}; got {schema_version!r}"
        )
    allowed_root_keys = {
        "schema_version",
        "project_id",
        "docs_root",
        "commands",
        "pools",
        "environment",
        "host_budget",
    }
    allowed_root_keys.add("base_branch" if schema_version == 1 else "repositories")
    reject_unknown_keys(raw, allowed_root_keys, "root config")
    project_id = validate_identifier(raw.get("project_id"), "project_id", ID_PATTERN)
    docs_root = resolve_docs_root(root, raw.get("docs_root"))
    base_branch: str | None = None
    repositories: dict[str, RepositoryConfig] = {}
    git_common_dir: Path | None = None
    if schema_version == 1:
        base_branch = require_string(raw.get("base_branch"), "base_branch")
        try:
            git_common_dir = resolve_git_common_dir(root)
        except OrchestratorError as exc:
            raise OrchestratorError(
                "schema_version 1 supports only a single Git repository at project_root; "
                "for a non-Git umbrella project, use schema_version 2 with explicit [[repositories]] entries. "
                f"Details: {exc}"
            ) from exc
        repositories["default"] = RepositoryConfig(
            repository_id="default",
            root=root,
            base_branch=base_branch,
            git_common_dir=git_common_dir,
        )
    else:
        repository_entries = raw.get("repositories")
        if not isinstance(repository_entries, list) or not repository_entries:
            raise OrchestratorError("repositories must be a non-empty array of tables in schema_version 2")
        for index, repository_value in enumerate(repository_entries):
            label = f"repositories[{index}]"
            repository = require_mapping(repository_value, label)
            reject_unknown_keys(repository, {"id", "path", "base_branch"}, label)
            repository_id = validate_identifier(repository.get("id"), f"{label}.id", ID_PATTERN)
            if repository_id in repositories:
                raise OrchestratorError(f"Duplicate repository id: {repository_id}")
            repository_root = resolve_repository_root(root, repository.get("path"), label)
            for existing in repositories.values():
                if paths_identical(repository_root, existing.root):
                    raise OrchestratorError(
                        f"Repository {repository_id} resolves to the same path as "
                        f"{existing.repository_id}: {repository_root}"
                    )
            repository_base = require_string(repository.get("base_branch"), f"{label}.base_branch")
            repository_git_common_dir = resolve_git_repository(
                repository_root, f"repository {repository_id}"
            )
            validate_base_ref(repository_root, repository_base, f"repository {repository_id}")
            repositories[repository_id] = RepositoryConfig(
                repository_id=repository_id,
                root=repository_root,
                base_branch=repository_base,
                git_common_dir=repository_git_common_dir,
            )

    environment = require_mapping(raw.get("environment"), "environment")
    reject_unknown_keys(environment, {"namespace"}, "environment")
    environment_namespace = validate_identifier(
        environment.get("namespace"), "environment.namespace", ID_PATTERN
    )

    commands = require_mapping(raw.get("commands"), "commands")
    if set(commands) != set(EXPECTED_COMMANDS):
        missing = sorted(set(EXPECTED_COMMANDS) - set(commands))
        extra = sorted(set(commands) - set(EXPECTED_COMMANDS))
        raise OrchestratorError(
            f"commands must contain exactly {sorted(EXPECTED_COMMANDS)}; missing={missing}, extra={extra}"
        )
    validated_commands: dict[str, dict[str, Any]] = {}
    for command_name, expected_skill in EXPECTED_COMMANDS.items():
        command = require_mapping(commands[command_name], f"commands.{command_name}")
        allowed = {"skill", "contexts"}
        if command_name == "execute":
            allowed.add("require_lightweight_gate")
        if command_name in {"test", "archive"}:
            allowed.add("pool")
        reject_unknown_keys(command, allowed, f"commands.{command_name}")
        skill = require_string(command.get("skill"), f"commands.{command_name}.skill")
        if skill != expected_skill:
            raise OrchestratorError(
                f"commands.{command_name}.skill must be {expected_skill}; got {skill}"
            )
        contexts = command.get("contexts", [])
        if not isinstance(contexts, list):
            raise OrchestratorError(f"commands.{command_name}.contexts must be an array")
        normalized_contexts = [
            validate_context_selector(item, f"commands.{command_name}.contexts[{index}]")
            for index, item in enumerate(contexts)
        ]
        for selector in normalized_contexts:
            context_name = selector.removeprefix("local:").split("#", 1)[0]
            context_path = docs_root / "context" / f"{context_name}.md"
            if not context_path.is_file():
                raise OrchestratorError(
                    f"Configured local context does not exist for {command_name}: {context_path}"
                )
        normalized = {"skill": skill, "contexts": normalized_contexts}
        if command_name == "execute":
            if command.get("require_lightweight_gate") is not True:
                raise OrchestratorError(
                    "commands.execute.require_lightweight_gate must be true"
                )
            normalized["require_lightweight_gate"] = True
        if command_name in {"test", "archive"}:
            normalized["pool"] = require_string(
                command.get("pool"), f"commands.{command_name}.pool"
            )
        validated_commands[command_name] = normalized

    pools = require_mapping(raw.get("pools"), "pools")
    if not pools:
        raise OrchestratorError("pools must contain at least one configured pool")
    validated_pools: dict[str, dict[str, Any]] = {}
    for pool_name, pool_value in pools.items():
        validate_identifier(pool_name, f"pools.{pool_name}", ID_PATTERN)
        pool = require_mapping(pool_value, f"pools.{pool_name}")
        reject_unknown_keys(pool, {"capacity", "queue", "lease_timeout_seconds"}, f"pools.{pool_name}")
        capacity = require_int(pool.get("capacity"), f"pools.{pool_name}.capacity", 1, 64)
        queue = require_string(pool.get("queue"), f"pools.{pool_name}.queue")
        if queue != "fifo":
            raise OrchestratorError(f"pools.{pool_name}.queue must be fifo")
        timeout = require_int(
            pool.get("lease_timeout_seconds"),
            f"pools.{pool_name}.lease_timeout_seconds",
            60,
            86400,
        )
        validated_pools[pool_name] = {
            "capacity": capacity,
            "queue": queue,
            "lease_timeout_seconds": timeout,
        }

    test_pool = validated_commands["test"]["pool"]
    merge_pool = validated_commands["archive"]["pool"]
    if test_pool not in validated_pools:
        raise OrchestratorError(f"Configured test pool does not exist: {test_pool}")
    if merge_pool not in validated_pools:
        raise OrchestratorError(f"Configured archive pool does not exist: {merge_pool}")
    if validated_pools[merge_pool]["capacity"] != 1:
        raise OrchestratorError("The configured archive pool capacity must be 1")

    host_budget_raw = raw.get("host_budget")
    host_budget: dict[str, Any] | None = None
    if host_budget_raw is not None:
        table = require_mapping(host_budget_raw, "host_budget")
        reject_unknown_keys(
            table,
            {"enabled", "host_id", "resource", "capacity", "lease_timeout_seconds"},
            "host_budget",
        )
        enabled = table.get("enabled")
        if not isinstance(enabled, bool):
            raise OrchestratorError("host_budget.enabled must be a boolean")
        host_budget = {"enabled": enabled}
        if enabled:
            host_budget.update(
                {
                    "host_id": validate_identifier(table.get("host_id"), "host_budget.host_id", ID_PATTERN),
                    "resource": validate_identifier(
                        table.get("resource"), "host_budget.resource", ID_PATTERN
                    ),
                    "capacity": require_int(
                        table.get("capacity"), "host_budget.capacity", 1, 256
                    ),
                    "lease_timeout_seconds": require_int(
                        table.get("lease_timeout_seconds"),
                        "host_budget.lease_timeout_seconds",
                        60,
                        86400,
                    ),
                }
            )

    runtime_root = (
        git_common_dir / "codex" / "m-orchestrator" / "projects" / project_id
        if schema_version == 1 and git_common_dir is not None
        else root / ".codex-runtime" / "m-orchestrator" / "projects" / project_id
    )
    return ProjectConfig(
        project_root=root,
        config_path=config_path,
        raw=raw,
        schema_version=schema_version,
        project_id=project_id,
        docs_root=docs_root,
        base_branch=base_branch,
        environment_namespace=environment_namespace,
        commands=validated_commands,
        pools=validated_pools,
        host_budget=host_budget,
        repositories=repositories,
        git_common_dir=git_common_dir,
        runtime_root=runtime_root,
        config_fingerprint=normalize_fingerprint(raw),
    )


def global_runtime_root() -> Path:
    configured = os.environ.get("M_ORCHESTRATOR_HOME", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    codex_home = os.environ.get("CODEX_HOME", "").strip()
    if codex_home:
        return (Path(codex_home).expanduser().resolve() / "m-orchestrator")
    return (Path.home() / ".codex" / "m-orchestrator").resolve()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise OrchestratorError(f"Cannot read runtime JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise OrchestratorError(f"Runtime JSON must contain an object: {path}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


@contextmanager
def directory_lock(path: Path) -> Iterator[None]:
    deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS
    while True:
        try:
            path.mkdir(parents=False)
            break
        except FileExistsError:
            try:
                age = time.time() - path.stat().st_mtime
                if age > LOCK_STALE_SECONDS:
                    path.rmdir()
                    continue
            except FileNotFoundError:
                continue
            except OSError:
                pass
            if time.monotonic() >= deadline:
                raise OrchestratorError(f"Timed out waiting for runtime lock: {path}")
            time.sleep(0.02)
    try:
        yield
    finally:
        try:
            path.rmdir()
        except FileNotFoundError:
            pass


def task_files(runtime_root: Path) -> list[Path]:
    task_root = runtime_root / "tasks"
    if not task_root.is_dir():
        return []
    return sorted(path for path in task_root.glob("*.json") if path.is_file())


def has_active_runtime_work(runtime_root: Path) -> bool:
    for path in task_files(runtime_root):
        if read_json(path).get("state") not in TERMINAL_STATES:
            return True
    pool_root = runtime_root / "pools"
    return pool_root.is_dir() and any(pool_root.glob("*/leases/*.json"))


def ensure_runtime(config: ProjectConfig) -> None:
    if config.schema_version == 2:
        legacy_marker = config.project_root / ".git"
        has_legacy_marker = legacy_marker.is_file() or (
            legacy_marker.is_dir() and next(legacy_marker.iterdir(), None) is not None
        )
        if has_legacy_marker:
            try:
                legacy_git_common_dir = resolve_git_common_dir(config.project_root)
            except OrchestratorError:
                legacy_git_common_dir = None
        else:
            legacy_git_common_dir = None
        if legacy_git_common_dir is not None:
            legacy_runtime_root = (
                legacy_git_common_dir / "codex" / "m-orchestrator" / "projects" / config.project_id
            )
            if legacy_runtime_root != config.runtime_root and legacy_runtime_root.is_dir() and has_active_runtime_work(
                legacy_runtime_root
            ):
                raise OrchestratorError(
                    "A schema_version 1 runtime for this project_id still has non-terminal Tasks or leases; "
                    "converge that runtime before enabling schema_version 2"
                )
    config.runtime_root.mkdir(parents=True, exist_ok=True)
    (config.runtime_root / "tasks").mkdir(exist_ok=True)
    (config.runtime_root / "pools").mkdir(exist_ok=True)
    (config.runtime_root / "events").mkdir(exist_ok=True)
    metadata_path = config.runtime_root / "project.json"
    lock_path = config.runtime_root / ".state.lock"
    with directory_lock(lock_path):
        if metadata_path.exists():
            metadata = read_json(metadata_path)
            if metadata.get("project_id") != config.project_id:
                raise OrchestratorError("Runtime project ID does not match validated config")
            metadata_schema = metadata.get("schema_version", 1)
            if metadata_schema != config.schema_version:
                raise OrchestratorError(
                    "Runtime schema version does not match the validated config; automatic runtime migration is not supported"
                )
            if config.schema_version == 1:
                if not paths_identical(
                    Path(metadata.get("git_common_dir", "")).resolve(), config.git_common_dir
                ):
                    raise OrchestratorError("Runtime Git common directory does not match this repository")
            elif not paths_identical(
                Path(metadata.get("project_root", "")).resolve(), config.project_root
            ):
                raise OrchestratorError("Runtime project root does not match the validated umbrella project")
            previous = metadata.get("config_fingerprint")
            if previous != config.config_fingerprint and has_active_runtime_work(config.runtime_root):
                raise OrchestratorError(
                    "Project config changed while non-terminal tasks or leases exist; converge them before retrying"
                )
            if previous != config.config_fingerprint:
                metadata["config_fingerprint"] = config.config_fingerprint
                metadata["updated_at"] = utc_now()
                atomic_write_json(metadata_path, metadata)
        else:
            atomic_write_json(
                metadata_path,
                {
                    "schema_version": config.schema_version,
                    "project_id": config.project_id,
                    **(
                        {"git_common_dir": str(config.git_common_dir)}
                        if config.schema_version == 1
                        else {"project_root": str(config.project_root)}
                    ),
                    "config_fingerprint": config.config_fingerprint,
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                },
            )


def file_evidence(path_value: str | None) -> dict[str, Any] | None:
    if path_value is None:
        return None
    path = Path(path_value).resolve()
    if not path.is_file():
        raise OrchestratorError(f"Evidence file does not exist: {path}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path), "sha256": digest}


def load_evidence_json(path_value: str) -> tuple[dict[str, Any], dict[str, Any]]:
    evidence = file_evidence(path_value)
    assert evidence is not None
    body = read_json(Path(evidence["path"]))
    return evidence, body


TASK_MANIFEST_KEYS = {
    "schema_version",
    "task_id",
    "title",
    "plan",
    "repositories",
    "acceptance",
    "tests",
    "rollback",
    "planner",
}


def validate_task_manifest_header(manifest: dict[str, Any]) -> str:
    reject_unknown_keys(manifest, TASK_MANIFEST_KEYS, "Task manifest")
    manifest_schema_version = manifest.get("schema_version")
    if isinstance(manifest_schema_version, bool) or manifest_schema_version != TASK_MANIFEST_VERSION:
        raise OrchestratorError(
            f"Task manifest schema_version must be {TASK_MANIFEST_VERSION}; "
            f"got {manifest_schema_version!r}"
        )
    return validate_identifier(manifest.get("task_id"), "Task manifest task_id", TASK_ID_PATTERN)


def require_string_list(value: Any, label: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "an array" if allow_empty else "a non-empty array"
        raise OrchestratorError(f"{label} must be {qualifier} of non-empty strings")
    return [require_string(item, f"{label}[{index}]") for index, item in enumerate(value)]


def resolve_absolute_file(value: Any, label: str) -> Path:
    text = require_string(value, label)
    candidate = Path(text)
    if not candidate.is_absolute():
        raise OrchestratorError(f"{label} must be an absolute path")
    resolved = candidate.resolve()
    if not resolved.is_file():
        raise OrchestratorError(f"{label} does not exist: {resolved}")
    return resolved


def resolve_absolute_worktree(config: ProjectConfig, value: Any, label: str) -> Path:
    text = require_string(value, label)
    candidate = Path(text)
    if not candidate.is_absolute():
        raise OrchestratorError(f"{label} must be an absolute path")
    resolved = candidate.resolve()
    if not resolved.is_dir():
        raise OrchestratorError(f"{label} directory does not exist: {resolved}")
    allowed_root = (config.project_root / "worktrees").resolve()
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise OrchestratorError(
            f"{label} must be inside the project worktree root {allowed_root}; got {resolved}"
        ) from exc
    return resolved


def validate_write_set(value: Any, label: str) -> list[str]:
    entries = require_string_list(value, label)
    normalized: list[str] = []
    for index, entry in enumerate(entries):
        candidate = Path(entry)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise OrchestratorError(
                f"{label}[{index}] must be a traversal-free path or glob relative to its worktree"
            )
        normalized.append(entry.replace("\\", "/"))
    return normalized


def git_commit(repository_root: Path, ref: str, label: str) -> str:
    return run_git(
        repository_root,
        ["rev-parse", "--verify", f"{ref}^{{commit}}"],
        f"{label} does not resolve to a commit",
    )


def validate_task_manifest(
    config: ProjectConfig,
    manifest_path_value: str,
    manifest_evidence: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if manifest_evidence is None or manifest is None:
        manifest_evidence, manifest = load_evidence_json(manifest_path_value)
    task_id = validate_task_manifest_header(manifest)
    title = require_string(manifest.get("title"), "Task manifest title")
    canonical_plan_path = resolve_absolute_file(manifest.get("plan"), "Task manifest plan")
    canonical_plan = file_evidence(str(canonical_plan_path))
    assert canonical_plan is not None
    acceptance = require_string_list(manifest.get("acceptance"), "Task manifest acceptance")
    tests = require_string_list(manifest.get("tests"), "Task manifest tests")
    rollback = require_string(manifest.get("rollback"), "Task manifest rollback")

    planner_value = require_mapping(manifest.get("planner"), "Task manifest planner")
    reject_unknown_keys(planner_value, {"thread_id", "host_id"}, "Task manifest planner")
    planner = {
        "thread_id": require_string(planner_value.get("thread_id"), "Task manifest planner.thread_id"),
        "host_id": None,
    }
    if planner_value.get("host_id") is not None:
        planner["host_id"] = require_string(
            planner_value.get("host_id"), "Task manifest planner.host_id"
        )

    repository_values = manifest.get("repositories")
    if not isinstance(repository_values, list) or not repository_values:
        raise OrchestratorError("Task manifest repositories must be a non-empty array")
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    selected_worktrees: set[str] = set()
    for index, repository_value in enumerate(repository_values):
        label = f"Task manifest repositories[{index}]"
        repository = require_mapping(repository_value, label)
        reject_unknown_keys(
            repository,
            {"id", "worktree", "branch", "base_ref", "planning_ref", "plan", "write_set"},
            label,
        )
        repository_id = validate_identifier(repository.get("id"), f"{label}.id", ID_PATTERN)
        configured = config.repositories.get(repository_id)
        if configured is None:
            raise OrchestratorError(f"{label}.id is not configured for this project: {repository_id}")
        if repository_id in selected_ids:
            raise OrchestratorError(f"Task manifest selects repository more than once: {repository_id}")
        worktree = resolve_absolute_worktree(config, repository.get("worktree"), f"{label}.worktree")
        worktree_key = os.path.normcase(str(worktree))
        if worktree_key in selected_worktrees:
            raise OrchestratorError(f"Task manifest reuses a worktree path: {worktree}")
        worktree_git_common_dir = resolve_git_repository(worktree, f"Task repository {repository_id} worktree")
        if not paths_identical(worktree_git_common_dir, configured.git_common_dir):
            raise OrchestratorError(
                f"Task repository {repository_id} worktree belongs to a different Git repository"
            )
        branch = require_string(repository.get("branch"), f"{label}.branch")
        current_branch = run_git(
            worktree,
            ["branch", "--show-current"],
            f"Cannot resolve Task repository {repository_id} branch",
        )
        if not current_branch or current_branch != branch:
            raise OrchestratorError(
                f"Task repository {repository_id} branch mismatch: expected {branch}, found {current_branch or 'detached HEAD'}"
            )
        base_ref = require_string(repository.get("base_ref"), f"{label}.base_ref")
        if base_ref != configured.base_branch:
            raise OrchestratorError(
                f"Task repository {repository_id} base_ref must match configured base_branch "
                f"{configured.base_branch}; got {base_ref}"
            )
        planning_ref = require_string(repository.get("planning_ref"), f"{label}.planning_ref")
        planning_commit = git_commit(worktree, planning_ref, f"{label}.planning_ref")
        head_commit = git_commit(worktree, "HEAD", f"Task repository {repository_id} HEAD")
        if planning_commit != head_commit:
            raise OrchestratorError(
                f"Task repository {repository_id} planning_ref must identify the current committed planning state"
            )
        repository_plan_path = resolve_absolute_file(repository.get("plan"), f"{label}.plan")
        if repository_plan_path.parent != worktree or repository_plan_path.name not in {"plan.md", "todo.md"}:
            raise OrchestratorError(
                f"{label}.plan must be plan.md or todo.md at the selected worktree root"
            )
        repository_plan = file_evidence(str(repository_plan_path))
        assert repository_plan is not None
        selected.append(
            {
                "id": repository_id,
                "repository_root": str(configured.root),
                "git_common_dir": str(configured.git_common_dir),
                "base_ref": base_ref,
                "branch": branch,
                "planning_ref": planning_commit,
                "worktree": str(worktree),
                "plan": repository_plan,
                "write_set": validate_write_set(repository.get("write_set"), f"{label}.write_set"),
            }
        )
        selected_ids.add(repository_id)
        selected_worktrees.add(worktree_key)

    normalized = {
        "task_id": task_id,
        "title": title,
        "plan": canonical_plan,
        "manifest": manifest_evidence,
        "repositories": selected,
        "acceptance": acceptance,
        "tests": tests,
        "rollback": rollback,
        "planner": planner,
    }
    return manifest_evidence, normalized


def run_git_bytes(repository_root: Path, arguments: list[str], label: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(repository_root), *arguments],
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.decode(errors="replace").strip() or "unknown Git error"
        raise OrchestratorError(f"{label}: {detail}")
    return process.stdout


def worktree_snapshot(repository: dict[str, Any]) -> dict[str, Any]:
    worktree = Path(require_string(repository.get("worktree"), "Task repository worktree")).resolve()
    current_git_common_dir = resolve_git_repository(
        worktree, f"Task repository {repository.get('id')} worktree"
    )
    expected_git_common_dir = Path(
        require_string(repository.get("git_common_dir"), "Task repository git_common_dir")
    ).resolve()
    if not paths_identical(current_git_common_dir, expected_git_common_dir):
        raise OrchestratorError(
            f"Task repository {repository.get('id')} worktree no longer belongs to its configured Git repository"
        )
    head = git_commit(worktree, "HEAD", f"Task repository {repository.get('id')} HEAD")
    diff = run_git_bytes(
        worktree,
        ["diff", "--binary", "--no-ext-diff", "HEAD"],
        f"Cannot read Task repository {repository.get('id')} diff",
    )
    untracked_raw = run_git_bytes(
        worktree,
        ["ls-files", "--others", "--exclude-standard", "-z"],
        f"Cannot list Task repository {repository.get('id')} untracked files",
    )
    untracked: list[dict[str, str]] = []
    for raw_name in [item for item in untracked_raw.split(b"\0") if item]:
        relative_name = raw_name.decode("utf-8", errors="surrogateescape")
        relative_path = Path(relative_name)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise OrchestratorError(
                f"Git returned an unsafe untracked path for repository {repository.get('id')}: {relative_name}"
            )
        candidate = worktree / relative_path
        if candidate.is_symlink():
            body = os.readlink(candidate).encode("utf-8", errors="surrogateescape")
        else:
            resolved = candidate.resolve()
            try:
                resolved.relative_to(worktree)
            except ValueError as exc:
                raise OrchestratorError(
                    f"Untracked file resolves outside worktree for repository {repository.get('id')}: {candidate}"
                ) from exc
            body = resolved.read_bytes()
        untracked.append(
            {"path": relative_name.replace("\\", "/"), "sha256": hashlib.sha256(body).hexdigest()}
        )
    plan_value = require_mapping(repository.get("plan"), "Task repository plan")
    current_plan = file_evidence(require_string(plan_value.get("path"), "Task repository plan path"))
    assert current_plan is not None
    return {
        "id": repository.get("id"),
        "head": head,
        "diff_sha256": hashlib.sha256(diff).hexdigest(),
        "untracked": sorted(untracked, key=lambda item: item["path"]),
        "plan_sha256": current_plan["sha256"],
    }


def compute_task_change_id(config: ProjectConfig, task_id: str) -> str:
    task = load_task(config, task_id)
    repositories = task.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        raise OrchestratorError(f"Task {task_id} has no repository manifest for composite change identity")
    snapshots = sorted(
        [worktree_snapshot(require_mapping(item, "Task repository")) for item in repositories],
        key=lambda item: str(item["id"]),
    )
    encoded = json.dumps(snapshots, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def validate_repository_gate_evidence(task: dict[str, Any], evidence_body: dict[str, Any]) -> None:
    task_repositories = task.get("repositories")
    if not isinstance(task_repositories, list) or not task_repositories:
        return
    evidence_repositories = evidence_body.get("repositories")
    if not isinstance(evidence_repositories, list) or not evidence_repositories:
        raise OrchestratorError("Multi-repository gate evidence requires a repositories array")
    expected_ids = {str(item.get("id")) for item in task_repositories}
    actual_ids: set[str] = set()
    for index, item_value in enumerate(evidence_repositories):
        item = require_mapping(item_value, f"Gate evidence repositories[{index}]")
        repository_id = validate_identifier(
            item.get("id"), f"Gate evidence repositories[{index}].id", ID_PATTERN
        )
        if repository_id in actual_ids:
            raise OrchestratorError(f"Gate evidence contains duplicate repository: {repository_id}")
        if item.get("status") != "Passed":
            raise OrchestratorError(
                f"Gate evidence repository {repository_id} status must be Passed"
            )
        actual_ids.add(repository_id)
    if actual_ids != expected_ids:
        raise OrchestratorError(
            f"Gate evidence repository set does not match Task manifest; "
            f"expected={sorted(expected_ids)}, actual={sorted(actual_ids)}"
        )


def ensure_current_passing_gate(config: ProjectConfig, task: dict[str, Any]) -> None:
    if not (task.get("gate") and task.get("change_id")):
        raise OrchestratorError("Tester admission requires a current passing gate")
    gate = require_mapping(task.get("gate"), "Task gate")
    current_gate = file_evidence(require_string(gate.get("path"), "Task gate path"))
    assert current_gate is not None
    if current_gate.get("sha256") != gate.get("sha256"):
        raise OrchestratorError(
            "Lightweight gate evidence changed after Task transition; regenerate it before Tester admission"
        )
    if task.get("repositories"):
        current_change_id = compute_task_change_id(config, require_string(task.get("task_id"), "task_id"))
        if current_change_id != task.get("change_id"):
            raise OrchestratorError(
                "Task repository state changed after the lightweight gate; rerun the complete gate before Tester admission"
            )


def task_path(config: ProjectConfig, task_id: str) -> Path:
    validated = validate_identifier(task_id, "task_id", TASK_ID_PATTERN)
    return config.runtime_root / "tasks" / f"{validated}.json"


def load_task(config: ProjectConfig, task_id: str) -> dict[str, Any]:
    path = task_path(config, task_id)
    if not path.is_file():
        raise OrchestratorError(f"Task does not exist: {task_id}")
    return read_json(path)


def create_task(
    config: ProjectConfig,
    task_id: str | None = None,
    plan_path_value: str | None = None,
    manifest_path_value: str | None = None,
) -> dict[str, Any]:
    normalized_manifest: dict[str, Any] | None = None
    manifest_evidence: dict[str, Any] | None = None
    manifest_body: dict[str, Any] | None = None
    if manifest_path_value is not None:
        manifest_evidence, manifest_body = load_evidence_json(manifest_path_value)
        manifest_task_id = validate_task_manifest_header(manifest_body)
        if task_id is not None and task_id != manifest_task_id:
            raise OrchestratorError(
                f"Task ID argument {task_id} does not match manifest task_id {manifest_task_id}"
            )
        task_id = manifest_task_id
    elif config.schema_version == 2:
        raise OrchestratorError("schema_version 2 Task creation requires --manifest")
    if task_id is None:
        raise OrchestratorError("Task creation requires task_id")
    if manifest_path_value is None and plan_path_value is None:
        raise OrchestratorError("schema_version 1 Task creation requires --plan or --manifest")
    path = task_path(config, task_id)
    if manifest_evidence is not None and path.is_file():
        ensure_runtime(config)
        with directory_lock(config.runtime_root / ".state.lock"):
            if path.exists():
                existing = read_json(path)
                if existing.get("manifest", {}).get("sha256") != manifest_evidence["sha256"]:
                    raise OrchestratorError(f"Task {task_id} already exists with a different manifest")
                if plan_path_value is not None and file_evidence(plan_path_value) != existing.get("plan"):
                    raise OrchestratorError("--plan does not match the canonical plan in the Task manifest")
                return existing

    if manifest_path_value is not None:
        assert manifest_evidence is not None and manifest_body is not None
        _, normalized_manifest = validate_task_manifest(
            config, manifest_path_value, manifest_evidence, manifest_body
        )
        if plan_path_value is not None:
            supplied_plan = file_evidence(plan_path_value)
            if supplied_plan != normalized_manifest["plan"]:
                raise OrchestratorError("--plan does not match the canonical plan in the Task manifest")
    plan = normalized_manifest["plan"] if normalized_manifest else file_evidence(plan_path_value)
    assert plan is not None
    ensure_runtime(config)
    with directory_lock(config.runtime_root / ".state.lock"):
        if path.exists():
            existing = read_json(path)
            if normalized_manifest:
                if existing.get("manifest", {}).get("sha256") != normalized_manifest["manifest"]["sha256"]:
                    raise OrchestratorError(f"Task {task_id} already exists with a different manifest")
            elif existing.get("plan", {}).get("sha256") != plan["sha256"]:
                raise OrchestratorError(f"Task {task_id} already exists with a different plan")
            return existing
        now = utc_now()
        task = {
            "schema_version": config.schema_version,
            "project_id": config.project_id,
            "task_id": task_id,
            "state": "PLANNED",
            "plan": plan,
            "gate": None,
            "change_id": None,
            "created_at": now,
            "updated_at": now,
            "history": [{"from": None, "to": "PLANNED", "at": now}],
        }
        if normalized_manifest:
            for key in (
                "title",
                "manifest",
                "repositories",
                "acceptance",
                "tests",
                "rollback",
                "planner",
            ):
                task[key] = normalized_manifest[key]
        atomic_write_json(path, task)
        return task


def bind_worker(
    config: ProjectConfig, task_id: str, thread_id: str, host_id: str | None
) -> dict[str, Any]:
    ensure_runtime(config)
    thread = require_string(thread_id, "thread_id")
    path = task_path(config, task_id)
    with directory_lock(config.runtime_root / ".state.lock"):
        task = load_task(config, task_id)
        existing = task.get("worker")
        if task.get("state") == "EXECUTING" and existing:
            if existing.get("thread_id") == thread and existing.get("host_id") == host_id:
                return task
            raise OrchestratorError(
                f"Task {task_id} is already bound to Worker {existing.get('thread_id')}"
            )
        if task.get("state") != "DISPATCHING":
            raise OrchestratorError(
                f"Task {task_id} must be DISPATCHING before Worker binding; found {task.get('state')}"
            )
        now = utc_now()
        task["worker"] = {
            "thread_id": thread,
            "host_id": host_id,
            "bound_at": now,
        }
        task["state"] = "EXECUTING"
        task["updated_at"] = now
        task.setdefault("history", []).append(
            {"from": "DISPATCHING", "to": "EXECUTING", "at": now, "worker": task["worker"]}
        )
        atomic_write_json(path, task)
        return task


def allowed_transition(current: str, target: str) -> bool:
    if current not in STATES or target not in STATES:
        return False
    if target == "BLOCKED":
        return current not in TERMINAL_STATES and current != "BLOCKED"
    return target in NORMAL_TRANSITIONS[current]


def transition_task(
    config: ProjectConfig,
    task_id: str,
    expected: str,
    target: str,
    evidence_path: str | None = None,
    change_id: str | None = None,
    reason: str | None = None,
    internal_lease: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ensure_runtime(config)
    if expected not in STATES or target not in STATES:
        raise OrchestratorError(f"Unknown Task state: {expected} -> {target}")
    path = task_path(config, task_id)
    with directory_lock(config.runtime_root / ".state.lock"):
        task = load_task(config, task_id)
        if task.get("state") != expected:
            raise OrchestratorError(
                f"Task {task_id} state mismatch: expected {expected}, found {task.get('state')}"
            )
        if expected == "BLOCKED" and not reason:
            raise OrchestratorError("Leaving BLOCKED requires a recorded resolution reason")
        if not allowed_transition(expected, target):
            raise OrchestratorError(f"Invalid Task transition: {expected} -> {target}")
        if target in {"TESTING", "ARCHIVING"} and internal_lease is None:
            raise OrchestratorError(f"{target} may be entered only through pool acquisition")

        evidence: dict[str, Any] | None = None
        evidence_body: dict[str, Any] | None = None
        if evidence_path is not None:
            evidence, evidence_body = load_evidence_json(evidence_path)

        if target == "WAITING_FOR_TESTER":
            if not change_id:
                raise OrchestratorError("WAITING_FOR_TESTER requires a non-empty change_id")
            if evidence_body is None:
                raise OrchestratorError("WAITING_FOR_TESTER requires gate evidence")
            if evidence_body.get("status") != "Passed":
                raise OrchestratorError("Lightweight gate evidence status must be Passed")
            if evidence_body.get("change_id") != change_id:
                raise OrchestratorError("Gate evidence change_id does not match transition change_id")
            validate_repository_gate_evidence(task, evidence_body)
            if task.get("repositories"):
                current_change_id = compute_task_change_id(config, task_id)
                if current_change_id != change_id:
                    raise OrchestratorError(
                        "Gate evidence change_id does not match the current multi-repository Task state"
                    )
        if target in {"TEST_FAILED", "TEST_PASSED", "COMPLETED"} and evidence is None:
            raise OrchestratorError(f"{target} requires evidence")
        if expected == "EXECUTING" and target == "WAITING_FOR_MERGE":
            if evidence_body is None or evidence_body.get("status") != "Skipped":
                raise OrchestratorError("Direct merge waiting requires justified Skipped test evidence")
            if not evidence_body.get("skip_reason"):
                raise OrchestratorError("Skipped test evidence requires skip_reason")
        if target == "BLOCKED" and not (reason or evidence):
            raise OrchestratorError("BLOCKED requires a reason or evidence")

        now = utc_now()
        task["state"] = target
        task["updated_at"] = now
        if target == "WAITING_FOR_TESTER":
            task["gate"] = evidence
            task["change_id"] = change_id
        elif target in {"EXECUTING", "EXECUTE_GATE_FAILED"}:
            task["gate"] = None
            task["change_id"] = None
        if evidence is not None:
            task["latest_evidence"] = evidence
        if reason:
            task["latest_reason"] = reason
        if internal_lease is not None:
            task["active_lease"] = {
                "pool": internal_lease["pool"],
                "lease_id": internal_lease["lease_id"],
            }
        elif target not in {"TESTING", "ARCHIVING"}:
            task.pop("active_lease", None)
        task.setdefault("history", []).append(
            {
                "from": expected,
                "to": target,
                "at": now,
                "evidence": evidence,
                "reason": reason,
            }
        )
        atomic_write_json(path, task)
        return task


def register_planner(
    config: ProjectConfig,
    thread_id: str,
    host_id: str | None,
    replace: bool,
    reason: str | None,
) -> dict[str, Any]:
    ensure_runtime(config)
    thread = require_string(thread_id, "thread_id")
    path = config.runtime_root / "planner.json"
    with directory_lock(config.runtime_root / ".state.lock"):
        if path.exists():
            existing = read_json(path)
            if existing.get("thread_id") == thread and existing.get("host_id") == host_id:
                return existing
            if not replace:
                raise OrchestratorError(
                    f"Planner already registered as thread {existing.get('thread_id')}; inspect it before replacement"
                )
            if not reason:
                raise OrchestratorError("Planner replacement requires --reason")
        planner = {
            "project_id": config.project_id,
            "thread_id": thread,
            "host_id": host_id,
            "registered_at": utc_now(),
            "replacement_reason": reason if replace else None,
        }
        atomic_write_json(path, planner)
        return planner


def pool_root(config: ProjectConfig, pool_name: str) -> Path:
    if pool_name not in config.pools:
        raise OrchestratorError(f"Unknown configured pool: {pool_name}")
    root = config.runtime_root / "pools" / pool_name
    (root / "queue").mkdir(parents=True, exist_ok=True)
    (root / "leases").mkdir(exist_ok=True)
    return root


def pool_expected_state(config: ProjectConfig, pool_name: str) -> tuple[str, str]:
    if pool_name == config.commands["test"]["pool"]:
        return "WAITING_FOR_TESTER", "TESTING"
    if pool_name == config.commands["archive"]["pool"]:
        return "WAITING_FOR_MERGE", "ARCHIVING"
    raise OrchestratorError(f"Pool is not assigned to a command: {pool_name}")


def list_records(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    if not directory.is_dir():
        return []
    return [(path, read_json(path)) for path in sorted(directory.glob("*.json"))]


def find_owned_record(
    records: list[tuple[Path, dict[str, Any]]], task_id: str
) -> tuple[Path, dict[str, Any]] | None:
    matches = [(path, record) for path, record in records if record.get("task_id") == task_id]
    if len(matches) > 1:
        raise OrchestratorError(f"Multiple runtime records exist for Task {task_id}")
    return matches[0] if matches else None


def enqueue_task(config: ProjectConfig, pool_name: str, task_id: str) -> dict[str, Any]:
    ensure_runtime(config)
    root = pool_root(config, pool_name)
    expected_state, _ = pool_expected_state(config, pool_name)
    task = load_task(config, task_id)
    if task.get("state") != expected_state:
        raise OrchestratorError(
            f"Task {task_id} must be {expected_state} before enqueue; found {task.get('state')}"
        )
    if expected_state == "WAITING_FOR_TESTER":
        ensure_current_passing_gate(config, task)
    with directory_lock(root / ".lock"):
        existing = find_owned_record(list_records(root / "queue"), task_id)
        if existing:
            return {"status": "Queued", "ticket": existing[1], "idempotent": True}
        now_ns = time.time_ns()
        ticket_id = f"{now_ns:020d}-{uuid.uuid4().hex}"
        ticket = {
            "project_id": config.project_id,
            "pool": pool_name,
            "task_id": task_id,
            "ticket_id": ticket_id,
            "created_at": utc_now(),
        }
        atomic_write_json(root / "queue" / f"{ticket_id}.json", ticket)
        return {"status": "Queued", "ticket": ticket, "idempotent": False}


def host_pool_root(config: ProjectConfig) -> Path | None:
    budget = config.host_budget
    if not budget or not budget.get("enabled"):
        return None
    return global_runtime_root() / "hosts" / budget["host_id"] / "pools" / budget["resource"]


def ensure_host_pool(config: ProjectConfig) -> Path | None:
    root = host_pool_root(config)
    if root is None:
        return None
    root.mkdir(parents=True, exist_ok=True)
    (root / "leases").mkdir(exist_ok=True)
    budget = config.host_budget
    assert budget is not None
    expected = {
        "host_id": budget["host_id"],
        "resource": budget["resource"],
        "capacity": budget["capacity"],
        "lease_timeout_seconds": budget["lease_timeout_seconds"],
    }
    metadata_path = root / "pool.json"
    with directory_lock(root / ".lock"):
        if metadata_path.exists():
            actual = read_json(metadata_path)
            for key, value in expected.items():
                if actual.get(key) != value:
                    raise OrchestratorError(
                        f"Host budget mismatch for {key}: expected {value!r}, found {actual.get(key)!r}"
                    )
        else:
            atomic_write_json(metadata_path, {**expected, "created_at": utc_now()})
    return root


def project_instance_id(config: ProjectConfig) -> str:
    runtime_identity = os.path.normcase(str(config.runtime_root.resolve()))
    payload = f"{config.schema_version}\0{runtime_identity}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def host_lease_owner(config: ProjectConfig, task_id: str) -> str:
    validated_task_id = validate_identifier(task_id, "task_id", TASK_ID_PATTERN)
    payload = f"{project_instance_id(config)}\0{validated_task_id}".encode("utf-8")
    return f"v2:{hashlib.sha256(payload).hexdigest()}"


def legacy_host_lease_owner(config: ProjectConfig, task_id: str) -> str:
    return f"{config.project_id}:{task_id}"


def host_lease_owner_matches(
    config: ProjectConfig, task_id: str, owner: Any, *, allow_legacy: bool
) -> bool:
    if owner == host_lease_owner(config, task_id):
        return True
    return allow_legacy and owner == legacy_host_lease_owner(config, task_id)


def acquire_host_lease(config: ProjectConfig, task_id: str) -> dict[str, Any] | None:
    root = ensure_host_pool(config)
    if root is None:
        return None
    budget = config.host_budget
    assert budget is not None
    with directory_lock(root / ".lock"):
        records = list_records(root / "leases")
        owner = host_lease_owner(config, task_id)
        existing = [(path, item) for path, item in records if item.get("owner") == owner]
        if len(existing) > 1:
            raise OrchestratorError(f"Multiple host leases exist for owner {owner}")
        if existing:
            lease = existing[0][1]
            age, timeout = lease_age_seconds(lease)
            if age > timeout:
                raise OrchestratorError(
                    f"Host lease {lease.get('lease_id')} for owner {owner} is stale; inspect live Task status before recovery"
                )
            return lease
        legacy_owner = legacy_host_lease_owner(config, task_id)
        legacy = [item for _, item in records if item.get("owner") == legacy_owner]
        if legacy:
            raise OrchestratorError(
                f"Legacy host lease {legacy[0].get('lease_id')} cannot be safely attributed to this project instance; "
                "inspect the linked project lease and recover or release it before retrying"
            )
        if len(records) >= budget["capacity"]:
            return {"status": "Waiting"}
        lease_id = uuid.uuid4().hex
        now = utc_now()
        lease = {
            "host_id": budget["host_id"],
            "resource": budget["resource"],
            "owner": owner,
            "project_instance_id": project_instance_id(config),
            "lease_id": lease_id,
            "acquired_at": now,
            "heartbeat_at": now,
            "lease_timeout_seconds": budget["lease_timeout_seconds"],
        }
        atomic_write_json(root / "leases" / f"{lease_id}.json", lease)
        return lease


def release_host_lease(config: ProjectConfig, lease_id: str, task_id: str) -> None:
    root = ensure_host_pool(config)
    if root is None:
        return
    path = root / "leases" / f"{lease_id}.json"
    with directory_lock(root / ".lock"):
        if not path.exists():
            return
        lease = read_json(path)
        if not host_lease_owner_matches(
            config, task_id, lease.get("owner"), allow_legacy=True
        ) or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Host lease ownership mismatch")
        path.unlink()


def heartbeat_host_lease(config: ProjectConfig, lease_id: str, task_id: str) -> None:
    root = ensure_host_pool(config)
    if root is None:
        return
    path = root / "leases" / f"{lease_id}.json"
    with directory_lock(root / ".lock"):
        if not path.exists():
            raise OrchestratorError(f"Host lease does not exist: {lease_id}")
        lease = read_json(path)
        if not host_lease_owner_matches(
            config, task_id, lease.get("owner"), allow_legacy=True
        ):
            raise OrchestratorError("Host lease ownership mismatch")
        lease["heartbeat_at"] = utc_now()
        atomic_write_json(path, lease)


def try_acquire(config: ProjectConfig, pool_name: str, task_id: str) -> dict[str, Any]:
    ensure_runtime(config)
    root = pool_root(config, pool_name)
    expected_state, acquired_state = pool_expected_state(config, pool_name)
    with directory_lock(root / ".lock"):
        leases = list_records(root / "leases")
        existing_lease = find_owned_record(leases, task_id)
        if existing_lease:
            lease = existing_lease[1]
            task = load_task(config, task_id)
            active_lease = task.get("active_lease")
            if task.get("state") != acquired_state or active_lease != {
                "pool": pool_name,
                "lease_id": lease.get("lease_id"),
            }:
                raise OrchestratorError(
                    f"Task {task_id} has lease {lease.get('lease_id')} but is not consistently {acquired_state}; inspect and release explicitly"
                )
            age, timeout = lease_age_seconds(lease)
            if age > timeout:
                raise OrchestratorError(
                    f"Lease {lease.get('lease_id')} for Task {task_id} is stale; inspect live Task status before recovery"
                )
            return {"status": "Acquired", "lease": lease, "idempotent": True}
        task = load_task(config, task_id)
        if task.get("state") != expected_state:
            raise OrchestratorError(
                f"Task {task_id} must be {expected_state} before acquire; found {task.get('state')}"
            )
        if expected_state == "WAITING_FOR_TESTER":
            ensure_current_passing_gate(config, task)
        tickets = list_records(root / "queue")
        owned_ticket = find_owned_record(tickets, task_id)
        if not owned_ticket:
            raise OrchestratorError(f"Task {task_id} is not queued in pool {pool_name}")
        position = next(
            index for index, (_, ticket) in enumerate(tickets, start=1) if ticket.get("task_id") == task_id
        )
        if position != 1:
            return {"status": "Waiting", "position": position, "reason": "fifo"}
        if len(leases) >= config.pools[pool_name]["capacity"]:
            return {"status": "Waiting", "position": position, "reason": "project-capacity"}

        host_lease = acquire_host_lease(config, task_id)
        if host_lease and host_lease.get("status") == "Waiting":
            return {"status": "Waiting", "position": position, "reason": "host-capacity"}
        lease_id = uuid.uuid4().hex
        now = utc_now()
        lease = {
            "project_id": config.project_id,
            "pool": pool_name,
            "task_id": task_id,
            "lease_id": lease_id,
            "acquired_at": now,
            "heartbeat_at": now,
            "lease_timeout_seconds": config.pools[pool_name]["lease_timeout_seconds"],
            "host_lease_id": host_lease.get("lease_id") if host_lease else None,
        }
        lease_path = root / "leases" / f"{lease_id}.json"
        try:
            atomic_write_json(lease_path, lease)
            transition_task(
                config,
                task_id,
                expected_state,
                acquired_state,
                internal_lease=lease,
            )
            owned_ticket[0].unlink()
        except Exception:
            lease_path.unlink(missing_ok=True)
            if host_lease and host_lease.get("lease_id"):
                release_host_lease(config, host_lease["lease_id"], task_id)
            raise
        return {"status": "Acquired", "lease": lease, "idempotent": False}


def heartbeat_lease(
    config: ProjectConfig, pool_name: str, task_id: str, lease_id: str
) -> dict[str, Any]:
    ensure_runtime(config)
    lease_id = validate_identifier(lease_id, "lease_id", LEASE_ID_PATTERN)
    root = pool_root(config, pool_name)
    path = root / "leases" / f"{lease_id}.json"
    with directory_lock(root / ".lock"):
        if not path.exists():
            raise OrchestratorError(f"Lease does not exist: {lease_id}")
        lease = read_json(path)
        if lease.get("task_id") != task_id or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Project lease ownership mismatch")
        if lease.get("host_lease_id"):
            heartbeat_host_lease(config, lease["host_lease_id"], task_id)
        lease["heartbeat_at"] = utc_now()
        atomic_write_json(path, lease)
        return {"status": "Heartbeat", "lease": lease}


def release_lease(
    config: ProjectConfig, pool_name: str, task_id: str, lease_id: str
) -> dict[str, Any]:
    ensure_runtime(config)
    lease_id = validate_identifier(lease_id, "lease_id", LEASE_ID_PATTERN)
    root = pool_root(config, pool_name)
    path = root / "leases" / f"{lease_id}.json"
    _, acquired_state = pool_expected_state(config, pool_name)
    with directory_lock(root / ".lock"):
        if not path.exists():
            other = find_owned_record(list_records(root / "leases"), task_id)
            if other:
                raise OrchestratorError(
                    f"Task {task_id} owns a different active lease: {other[1].get('lease_id')}"
                )
            task = load_task(config, task_id)
            if task.get("state") == acquired_state:
                raise OrchestratorError(
                    f"Task {task_id} is still {acquired_state} but its lease is missing; inspect runtime state"
                )
            return {"status": "Released", "lease_id": lease_id, "idempotent": True}
        lease = read_json(path)
        if lease.get("task_id") != task_id or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Project lease ownership mismatch")
        task = load_task(config, task_id)
        if task.get("state") == acquired_state:
            raise OrchestratorError(
                f"Persist the Tester or archive result, or use explicit stale reclaim, before releasing {acquired_state}"
            )
        if lease.get("host_lease_id"):
            release_host_lease(config, lease["host_lease_id"], task_id)
        path.unlink()
        return {"status": "Released", "lease_id": lease_id, "idempotent": False}


def reclaim_lease(
    config: ProjectConfig,
    pool_name: str,
    task_id: str,
    lease_id: str,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    ensure_runtime(config)
    lease_id = validate_identifier(lease_id, "lease_id", LEASE_ID_PATTERN)
    actor = require_string(actor, "actor")
    reason = require_string(reason, "reason")
    root = pool_root(config, pool_name)
    path = root / "leases" / f"{lease_id}.json"
    event_path = config.runtime_root / "events" / f"lease-reclaim-{lease_id}.json"
    _, acquired_state = pool_expected_state(config, pool_name)
    resolution = f"Stale lease {lease_id} reclaimed by {actor}: {reason}"
    with directory_lock(root / ".lock"):
        if not path.exists():
            other = find_owned_record(list_records(root / "leases"), task_id)
            if other:
                raise OrchestratorError(
                    f"Task {task_id} owns a different active lease: {other[1].get('lease_id')}"
                )
            if event_path.exists():
                event = read_json(event_path)
                if all(
                    event.get(key) == value
                    for key, value in {
                        "project_id": config.project_id,
                        "pool": pool_name,
                        "task_id": task_id,
                        "lease_id": lease_id,
                        "actor": actor,
                        "reason": reason,
                    }.items()
                ):
                    task = load_task(config, task_id)
                    if task.get("state") != "BLOCKED" or task.get("latest_reason") != resolution:
                        raise OrchestratorError(
                            f"Reclaim audit for {lease_id} does not match Task {task_id} state"
                        )
                    if event.get("status") != "Completed":
                        event["status"] = "Completed"
                        event["completed_at"] = utc_now()
                        atomic_write_json(event_path, event)
                    return {
                        "status": "Reclaimed",
                        "lease_id": lease_id,
                        "event": event,
                        "idempotent": True,
                    }
            raise OrchestratorError(f"Lease does not exist and has no reclaim audit: {lease_id}")

        lease = read_json(path)
        if lease.get("task_id") != task_id or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Project lease ownership mismatch")
        age, timeout = lease_age_seconds(lease)
        if age <= timeout:
            raise OrchestratorError(
                f"Lease {lease_id} is not stale; heartbeat or persist the normal result instead"
            )
        task = load_task(config, task_id)
        expected_active = {"pool": pool_name, "lease_id": lease_id}
        recovery_started = (
            task.get("state") == "BLOCKED"
            and task.get("latest_reason") == resolution
            and not task.get("active_lease")
        )
        if not recovery_started and (
            task.get("state") != acquired_state
            or task.get("active_lease") != expected_active
        ):
            raise OrchestratorError(
                f"Task {task_id} and lease {lease_id} are inconsistent; inspect before recovery"
            )

        if event_path.exists():
            event = read_json(event_path)
            if any(
                event.get(key) != value
                for key, value in {
                    "project_id": config.project_id,
                    "pool": pool_name,
                    "task_id": task_id,
                    "lease_id": lease_id,
                    "actor": actor,
                    "reason": reason,
                }.items()
            ):
                raise OrchestratorError(f"Reclaim audit ownership mismatch: {event_path}")
        else:
            event = {
                "event": "lease-reclaimed",
                "status": "Started",
                "project_id": config.project_id,
                "pool": pool_name,
                "task_id": task_id,
                "lease_id": lease_id,
                "actor": actor,
                "reason": reason,
                "started_at": utc_now(),
            }
            atomic_write_json(event_path, event)
        if lease.get("host_lease_id"):
            release_host_lease(config, lease["host_lease_id"], task_id)
        if not recovery_started:
            transition_task(
                config,
                task_id,
                acquired_state,
                "BLOCKED",
                reason=resolution,
            )
        event["status"] = "Completed"
        event["completed_at"] = utc_now()
        atomic_write_json(event_path, event)
        path.unlink()
        return {
            "status": "Reclaimed",
            "lease_id": lease_id,
            "event": event,
            "idempotent": False,
        }


def reclaim_host_lease(
    config: ProjectConfig,
    pool_name: str,
    task_id: str,
    lease_id: str,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    ensure_runtime(config)
    lease_id = validate_identifier(lease_id, "lease_id", LEASE_ID_PATTERN)
    actor = require_string(actor, "actor")
    reason = require_string(reason, "reason")
    project_pool = pool_root(config, pool_name)
    expected_state, _ = pool_expected_state(config, pool_name)
    host_root = ensure_host_pool(config)
    if host_root is None:
        raise OrchestratorError("Host budget is not enabled for this project")
    path = host_root / "leases" / f"{lease_id}.json"
    event_path = config.runtime_root / "events" / f"host-lease-reclaim-{lease_id}.json"
    with directory_lock(project_pool / ".lock"):
        project_lease = find_owned_record(
            list_records(project_pool / "leases"), task_id
        )
        if project_lease:
            raise OrchestratorError(
                f"Task {task_id} has project lease {project_lease[1].get('lease_id')}; use project lease recovery"
            )
        task = load_task(config, task_id)
        if task.get("state") != expected_state or task.get("active_lease"):
            raise OrchestratorError(
                f"Task {task_id} is not an orphan-host candidate in {expected_state}"
            )

        with directory_lock(host_root / ".lock"):
            if not path.exists():
                if event_path.exists():
                    event = read_json(event_path)
                    if all(
                        event.get(key) == value
                        for key, value in {
                            "project_id": config.project_id,
                            "pool": pool_name,
                            "task_id": task_id,
                            "lease_id": lease_id,
                            "actor": actor,
                            "reason": reason,
                        }.items()
                    ) and host_lease_owner_matches(
                        config, task_id, event.get("owner"), allow_legacy=True
                    ):
                        return {
                            "status": "HostReclaimed",
                            "lease_id": lease_id,
                            "event": event,
                            "idempotent": True,
                        }
                raise OrchestratorError(
                    f"Host lease does not exist and has no reclaim audit: {lease_id}"
                )
            lease = read_json(path)
            if not host_lease_owner_matches(
                config, task_id, lease.get("owner"), allow_legacy=True
            ) or lease.get("lease_id") != lease_id:
                raise OrchestratorError("Host lease ownership mismatch")
            age, timeout = lease_age_seconds(lease)
            if age <= timeout:
                raise OrchestratorError(
                    f"Host lease {lease_id} is not stale; retry normal acquisition instead"
                )
            event = {
                "event": "orphan-host-lease-reclaimed",
                "project_id": config.project_id,
                "pool": pool_name,
                "task_id": task_id,
                "owner": lease.get("owner"),
                "lease_id": lease_id,
                "actor": actor,
                "reason": reason,
                "at": utc_now(),
            }
            atomic_write_json(event_path, event)
            path.unlink()
            return {
                "status": "HostReclaimed",
                "lease_id": lease_id,
                "event": event,
                "idempotent": False,
            }


def stale_leases(config: ProjectConfig, pool_name: str) -> dict[str, Any]:
    ensure_runtime(config)
    root = pool_root(config, pool_name)
    now = datetime.now(timezone.utc)
    stale: list[dict[str, Any]] = []
    for _, lease in list_records(root / "leases"):
        age, timeout = lease_age_seconds(lease, now)
        if age > timeout:
            stale.append({**lease, "age_seconds": int(age)})
    stale_host: list[dict[str, Any]] = []
    host_root = ensure_host_pool(config)
    if host_root is not None:
        instance_id = project_instance_id(config)
        legacy_owner_prefix = f"{config.project_id}:"
        with directory_lock(host_root / ".lock"):
            for _, lease in list_records(host_root / "leases"):
                if lease.get("project_instance_id") != instance_id and not str(
                    lease.get("owner", "")
                ).startswith(legacy_owner_prefix):
                    continue
                age, timeout = lease_age_seconds(lease, now)
                if age > timeout:
                    stale_host.append({**lease, "age_seconds": int(age)})
    return {
        "status": "Inspected",
        "pool": pool_name,
        "stale": stale,
        "stale_host": stale_host,
    }


def project_status(config: ProjectConfig) -> dict[str, Any]:
    ensure_runtime(config)
    planner_path = config.runtime_root / "planner.json"
    tasks = [record for _, record in [(path, read_json(path)) for path in task_files(config.runtime_root)]]
    pools: dict[str, Any] = {}
    for name in sorted(config.pools):
        root = pool_root(config, name)
        pools[name] = {
            "capacity": config.pools[name]["capacity"],
            "queued": [record for _, record in list_records(root / "queue")],
            "leases": [record for _, record in list_records(root / "leases")],
        }
    return {
        "status": "Ready",
        "project_id": config.project_id,
        "schema_version": config.schema_version,
        "runtime_root": str(config.runtime_root),
        "repositories": [
            {
                "id": repository.repository_id,
                "root": str(repository.root),
                "base_branch": repository.base_branch,
                "git_common_dir": str(repository.git_common_dir),
            }
            for repository in config.repositories.values()
        ],
        "planner": read_json(planner_path) if planner_path.exists() else None,
        "tasks": tasks,
        "pools": pools,
    }


def config_result(config: ProjectConfig) -> dict[str, Any]:
    ensure_runtime(config)
    return {
        "status": "Valid",
        "schema_version": config.schema_version,
        "project_id": config.project_id,
        "project_root": str(config.project_root),
        "docs_root": str(config.docs_root),
        "git_common_dir": str(config.git_common_dir) if config.git_common_dir else None,
        "runtime_root": str(config.runtime_root),
        "repositories": [
            {
                "id": repository.repository_id,
                "root": str(repository.root),
                "base_branch": repository.base_branch,
                "git_common_dir": str(repository.git_common_dir),
            }
            for repository in config.repositories.values()
        ],
        "commands": config.commands,
        "pools": config.pools,
        "host_budget": config.host_budget,
    }


def add_project_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    domains = parser.add_subparsers(dest="domain", required=True)

    config_parser = domains.add_parser("config")
    config_actions = config_parser.add_subparsers(dest="action", required=True)
    config_validate = config_actions.add_parser("validate")
    add_project_root(config_validate)

    planner_parser = domains.add_parser("planner")
    planner_actions = planner_parser.add_subparsers(dest="action", required=True)
    planner_register = planner_actions.add_parser("register")
    add_project_root(planner_register)
    planner_register.add_argument("--thread-id", required=True)
    planner_register.add_argument("--host-id")
    planner_register.add_argument("--replace", action="store_true")
    planner_register.add_argument("--reason")

    project_parser = domains.add_parser("project")
    project_actions = project_parser.add_subparsers(dest="action", required=True)
    project_status_parser = project_actions.add_parser("status")
    add_project_root(project_status_parser)

    task_parser = domains.add_parser("task")
    task_actions = task_parser.add_subparsers(dest="action", required=True)
    task_create_parser = task_actions.add_parser("create")
    add_project_root(task_create_parser)
    task_create_parser.add_argument("--task-id")
    task_create_parser.add_argument("--plan")
    task_create_parser.add_argument("--manifest")
    task_change_id_parser = task_actions.add_parser("change-id")
    add_project_root(task_change_id_parser)
    task_change_id_parser.add_argument("--task-id", required=True)
    task_bind_parser = task_actions.add_parser("bind-worker")
    add_project_root(task_bind_parser)
    task_bind_parser.add_argument("--task-id", required=True)
    task_bind_parser.add_argument("--thread-id", required=True)
    task_bind_parser.add_argument("--host-id")
    task_transition_parser = task_actions.add_parser("transition")
    add_project_root(task_transition_parser)
    task_transition_parser.add_argument("--task-id", required=True)
    task_transition_parser.add_argument("--from", dest="expected", required=True)
    task_transition_parser.add_argument("--to", dest="target", required=True)
    task_transition_parser.add_argument("--evidence")
    task_transition_parser.add_argument("--change-id")
    task_transition_parser.add_argument("--reason")

    pool_parser = domains.add_parser("pool")
    pool_actions = pool_parser.add_subparsers(dest="action", required=True)
    for action in (
        "enqueue",
        "try-acquire",
        "heartbeat",
        "release",
        "reclaim",
        "reclaim-host",
    ):
        action_parser = pool_actions.add_parser(action)
        add_project_root(action_parser)
        action_parser.add_argument("--pool", required=True)
        action_parser.add_argument("--task-id", required=True)
        if action in {"heartbeat", "release", "reclaim", "reclaim-host"}:
            action_parser.add_argument("--lease-id", required=True)
        if action in {"reclaim", "reclaim-host"}:
            action_parser.add_argument("--actor", required=True)
            action_parser.add_argument("--reason", required=True)
    pool_stale_parser = pool_actions.add_parser("stale")
    add_project_root(pool_stale_parser)
    pool_stale_parser.add_argument("--pool", required=True)
    return parser


def execute(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config(args.project_root)
    if args.domain == "config" and args.action == "validate":
        return config_result(config)
    if args.domain == "planner" and args.action == "register":
        return register_planner(
            config, args.thread_id, args.host_id, args.replace, args.reason
        )
    if args.domain == "project" and args.action == "status":
        return project_status(config)
    if args.domain == "task" and args.action == "create":
        return create_task(config, args.task_id, args.plan, args.manifest)
    if args.domain == "task" and args.action == "change-id":
        return {
            "status": "Computed",
            "task_id": args.task_id,
            "change_id": compute_task_change_id(config, args.task_id),
        }
    if args.domain == "task" and args.action == "bind-worker":
        return bind_worker(config, args.task_id, args.thread_id, args.host_id)
    if args.domain == "task" and args.action == "transition":
        return transition_task(
            config,
            args.task_id,
            args.expected,
            args.target,
            args.evidence,
            args.change_id,
            args.reason,
        )
    if args.domain == "pool" and args.action == "enqueue":
        return enqueue_task(config, args.pool, args.task_id)
    if args.domain == "pool" and args.action == "try-acquire":
        return try_acquire(config, args.pool, args.task_id)
    if args.domain == "pool" and args.action == "heartbeat":
        return heartbeat_lease(config, args.pool, args.task_id, args.lease_id)
    if args.domain == "pool" and args.action == "release":
        return release_lease(config, args.pool, args.task_id, args.lease_id)
    if args.domain == "pool" and args.action == "reclaim":
        return reclaim_lease(
            config,
            args.pool,
            args.task_id,
            args.lease_id,
            args.actor,
            args.reason,
        )
    if args.domain == "pool" and args.action == "reclaim-host":
        return reclaim_host_lease(
            config,
            args.pool,
            args.task_id,
            args.lease_id,
            args.actor,
            args.reason,
        )
    if args.domain == "pool" and args.action == "stale":
        return stale_leases(config, args.pool)
    raise OrchestratorError(f"Unsupported command: {args.domain} {args.action}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = execute(args)
    except OrchestratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: filesystem operation failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
