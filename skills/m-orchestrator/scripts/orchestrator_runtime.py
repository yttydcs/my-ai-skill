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


SCHEMA_VERSION = 1
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
class ProjectConfig:
    project_root: Path
    config_path: Path
    raw: dict[str, Any]
    project_id: str
    docs_root: Path
    base_branch: str
    environment_namespace: str
    commands: dict[str, dict[str, Any]]
    pools: dict[str, dict[str, Any]]
    host_budget: dict[str, Any] | None
    git_common_dir: Path
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


def resolve_git_common_dir(project_root: Path) -> Path:
    process = subprocess.run(
        ["git", "-C", str(project_root), "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "unknown Git error"
        raise OrchestratorError(f"Cannot resolve Git common directory: {detail}")
    raw_path = Path(process.stdout.strip())
    resolved = raw_path.resolve() if raw_path.is_absolute() else (project_root / raw_path).resolve()
    if not resolved.is_dir():
        raise OrchestratorError(f"Git common directory does not exist: {resolved}")
    return resolved


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

    reject_unknown_keys(
        raw,
        {
            "schema_version",
            "project_id",
            "docs_root",
            "base_branch",
            "commands",
            "pools",
            "environment",
            "host_budget",
        },
        "root config",
    )
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise OrchestratorError(
            f"schema_version must be {SCHEMA_VERSION}; got {raw.get('schema_version')!r}"
        )
    project_id = validate_identifier(raw.get("project_id"), "project_id", ID_PATTERN)
    docs_root = resolve_docs_root(root, raw.get("docs_root"))
    base_branch = require_string(raw.get("base_branch"), "base_branch")

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

    git_common_dir = resolve_git_common_dir(root)
    runtime_root = git_common_dir / "codex" / "m-orchestrator" / "projects" / project_id
    return ProjectConfig(
        project_root=root,
        config_path=config_path,
        raw=raw,
        project_id=project_id,
        docs_root=docs_root,
        base_branch=base_branch,
        environment_namespace=environment_namespace,
        commands=validated_commands,
        pools=validated_pools,
        host_budget=host_budget,
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
    config.runtime_root.mkdir(parents=True, exist_ok=True)
    (config.runtime_root / "tasks").mkdir(exist_ok=True)
    (config.runtime_root / "pools").mkdir(exist_ok=True)
    metadata_path = config.runtime_root / "project.json"
    lock_path = config.runtime_root / ".state.lock"
    with directory_lock(lock_path):
        if metadata_path.exists():
            metadata = read_json(metadata_path)
            if metadata.get("project_id") != config.project_id:
                raise OrchestratorError("Runtime project ID does not match validated config")
            if Path(metadata.get("git_common_dir", "")).resolve() != config.git_common_dir:
                raise OrchestratorError("Runtime Git common directory does not match this repository")
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
                    "schema_version": SCHEMA_VERSION,
                    "project_id": config.project_id,
                    "git_common_dir": str(config.git_common_dir),
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


def task_path(config: ProjectConfig, task_id: str) -> Path:
    validated = validate_identifier(task_id, "task_id", TASK_ID_PATTERN)
    return config.runtime_root / "tasks" / f"{validated}.json"


def load_task(config: ProjectConfig, task_id: str) -> dict[str, Any]:
    path = task_path(config, task_id)
    if not path.is_file():
        raise OrchestratorError(f"Task does not exist: {task_id}")
    return read_json(path)


def create_task(config: ProjectConfig, task_id: str, plan_path_value: str) -> dict[str, Any]:
    ensure_runtime(config)
    path = task_path(config, task_id)
    plan = file_evidence(plan_path_value)
    assert plan is not None
    with directory_lock(config.runtime_root / ".state.lock"):
        if path.exists():
            existing = read_json(path)
            if existing.get("plan", {}).get("sha256") != plan["sha256"]:
                raise OrchestratorError(f"Task {task_id} already exists with a different plan")
            return existing
        now = utc_now()
        task = {
            "schema_version": SCHEMA_VERSION,
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
        if not allowed_transition(expected, target):
            if not (expected == "BLOCKED" and reason):
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
    if expected_state == "WAITING_FOR_TESTER" and not (task.get("gate") and task.get("change_id")):
        raise OrchestratorError("Tester enqueue requires a current passing gate")
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
    metadata_path = root / "pool.json"
    budget = config.host_budget
    assert budget is not None
    expected = {
        "host_id": budget["host_id"],
        "resource": budget["resource"],
        "capacity": budget["capacity"],
        "lease_timeout_seconds": budget["lease_timeout_seconds"],
    }
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


def acquire_host_lease(config: ProjectConfig, task_id: str) -> dict[str, Any] | None:
    root = ensure_host_pool(config)
    if root is None:
        return None
    budget = config.host_budget
    assert budget is not None
    with directory_lock(root / ".lock"):
        records = list_records(root / "leases")
        owner = f"{config.project_id}:{task_id}"
        existing = [(path, item) for path, item in records if item.get("owner") == owner]
        if len(existing) > 1:
            raise OrchestratorError(f"Multiple host leases exist for owner {owner}")
        if existing:
            return existing[0][1]
        if len(records) >= budget["capacity"]:
            return {"status": "Waiting"}
        lease_id = uuid.uuid4().hex
        now = utc_now()
        lease = {
            "host_id": budget["host_id"],
            "resource": budget["resource"],
            "owner": owner,
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
    owner = f"{config.project_id}:{task_id}"
    with directory_lock(root / ".lock"):
        if not path.exists():
            return
        lease = read_json(path)
        if lease.get("owner") != owner or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Host lease ownership mismatch")
        path.unlink()


def heartbeat_host_lease(config: ProjectConfig, lease_id: str, task_id: str) -> None:
    root = ensure_host_pool(config)
    if root is None:
        return
    path = root / "leases" / f"{lease_id}.json"
    owner = f"{config.project_id}:{task_id}"
    with directory_lock(root / ".lock"):
        if not path.exists():
            raise OrchestratorError(f"Host lease does not exist: {lease_id}")
        lease = read_json(path)
        if lease.get("owner") != owner:
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
            return {"status": "Acquired", "lease": existing_lease[1], "idempotent": True}
        task = load_task(config, task_id)
        if task.get("state") != expected_state:
            raise OrchestratorError(
                f"Task {task_id} must be {expected_state} before acquire; found {task.get('state')}"
            )
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
    root = pool_root(config, pool_name)
    path = root / "leases" / f"{lease_id}.json"
    with directory_lock(root / ".lock"):
        if not path.exists():
            other = find_owned_record(list_records(root / "leases"), task_id)
            if other:
                raise OrchestratorError(
                    f"Task {task_id} owns a different active lease: {other[1].get('lease_id')}"
                )
            return {"status": "Released", "lease_id": lease_id, "idempotent": True}
        lease = read_json(path)
        if lease.get("task_id") != task_id or lease.get("lease_id") != lease_id:
            raise OrchestratorError("Project lease ownership mismatch")
        if lease.get("host_lease_id"):
            release_host_lease(config, lease["host_lease_id"], task_id)
        path.unlink()
        return {"status": "Released", "lease_id": lease_id, "idempotent": False}


def stale_leases(config: ProjectConfig, pool_name: str) -> dict[str, Any]:
    ensure_runtime(config)
    root = pool_root(config, pool_name)
    now = datetime.now(timezone.utc)
    stale: list[dict[str, Any]] = []
    for _, lease in list_records(root / "leases"):
        heartbeat = parse_time(require_string(lease.get("heartbeat_at"), "lease heartbeat_at"))
        timeout = require_int(
            lease.get("lease_timeout_seconds"), "lease_timeout_seconds", 60, 86400
        )
        age = (now - heartbeat).total_seconds()
        if age > timeout:
            stale.append({**lease, "age_seconds": int(age)})
    return {"status": "Inspected", "pool": pool_name, "stale": stale}


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
        "runtime_root": str(config.runtime_root),
        "planner": read_json(planner_path) if planner_path.exists() else None,
        "tasks": tasks,
        "pools": pools,
    }


def config_result(config: ProjectConfig) -> dict[str, Any]:
    ensure_runtime(config)
    return {
        "status": "Valid",
        "project_id": config.project_id,
        "project_root": str(config.project_root),
        "docs_root": str(config.docs_root),
        "git_common_dir": str(config.git_common_dir),
        "runtime_root": str(config.runtime_root),
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
    task_create_parser.add_argument("--task-id", required=True)
    task_create_parser.add_argument("--plan", required=True)
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
    for action in ("enqueue", "try-acquire", "heartbeat", "release"):
        action_parser = pool_actions.add_parser(action)
        add_project_root(action_parser)
        action_parser.add_argument("--pool", required=True)
        action_parser.add_argument("--task-id", required=True)
        if action in {"heartbeat", "release"}:
            action_parser.add_argument("--lease-id", required=True)
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
        return create_task(config, args.task_id, args.plan)
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
