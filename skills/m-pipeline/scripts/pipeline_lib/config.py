"""Strict configuration and filesystem boundaries; never load context bodies."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


class PipelineError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def require(condition, message, code="invalid_input"):
    if not condition:
        raise PipelineError(code, message)


def fields(value, required, optional=()):
    require(isinstance(value, dict), "Expected a JSON object")
    require(set(required) <= value.keys(), f"Missing fields: {sorted(set(required) - value.keys())}")
    require(value.keys() <= set(required) | set(optional),
            f"Unknown fields: {sorted(value.keys() - set(required) - set(optional))}")
    return value


def label(value, name="identifier"):
    require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value),
            f"Invalid {name}; use letters, numbers, dots, underscores or hyphens")
    return value


def string(value, name="value"):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 4096
            and not any(ord(c) < 32 for c in value), f"Invalid {name}")
    return value


def strings(value, name="values", nonempty=False):
    require(isinstance(value, list), f"{name} must be an array")
    for item in value:
        string(item, name)
    require(len(value) == len(set(value)), f"Duplicate {name}")
    require(not nonempty or value, f"{name} must not be empty")
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)
    except (OSError, UnicodeError, ValueError) as exc:
        raise PipelineError("invalid_json", f"Cannot read JSON input: {type(exc).__name__}") from exc


def path_at(value, base, exists=True):
    string(value, "path")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path(base) / path
    try:
        path = path.resolve(strict=exists)
    except (OSError, RuntimeError) as exc:
        raise PipelineError("invalid_path", f"Cannot resolve path: {value}") from exc
    return path


def inside(path, root):
    try:
        return Path(path).resolve().is_relative_to(Path(root).resolve())
    except (OSError, RuntimeError):
        return False


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                            text=True, encoding="utf-8", timeout=20)
    require(result.returncode == 0, f"Git verification failed in {repo}: {args[0]}", "git_verification")
    return result.stdout.strip()


def git_identity(repo):
    return path_at(git(repo, "rev-parse", "--git-common-dir"), repo)


def path_key(path):
    return os.path.normcase(str(Path(path).resolve()))


def phase_contract(phase):
    skill_root = Path(__file__).resolve().parents[3]
    names = {"m-autoflow", "m-context", "m-docs"}
    if phase != "release":
        names.add(phase)
    if phase in ("m-go", "m-continue"):
        names.update(("m-execute", "m-test"))
    files = {}
    for name in sorted(names):
        package = skill_root / name
        require((package / "SKILL.md").is_file(), f"Required companion skill is missing: {name}", "missing_skill")
        for path in sorted(package.rglob("*")):
            if path.is_file() and path.suffix in (".md", ".py") and "__pycache__" not in path.parts:
                files[str(path.relative_to(skill_root)).replace("\\", "/")] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest(files)


def session_key(value):
    fields(value, ("host_id", "thread_id"))
    return f"{label(value['host_id'], 'host ID')}:{label(value['thread_id'], 'thread ID')}"


PHASES = {"m-discuss": 0, "m-plan": 1, "m-execute": 2, "m-go": 2,
          "m-continue": 2, "m-test": 3, "m-archive": 4, "release": 5}


def validate_blueprint(raw, base):
    fields(raw, ("version", "project_root", "docs_root", "repositories", "roles", "stages", "limits"))
    config = json.loads(canonical(raw))
    require(type(config["version"]) is int and config["version"] == 1, "Unsupported blueprint version")
    for key in ("project_root", "docs_root"):
        path = path_at(config[key], base)
        require(path.is_dir(), f"{key} must be a directory")
        config[key] = str(path)
    require(isinstance(config["repositories"], dict) and config["repositories"], "Declare repositories explicitly")
    identities = set()
    for key, repo in config["repositories"].items():
        label(key, "repository key")
        fields(repo, ("path", "base_ref", "worktree_root"))
        repo["path"] = str(path_at(repo["path"], base))
        identity = git_identity(repo["path"])
        require(identity not in identities, "Duplicate repository identity")
        identities.add(identity)
        require(not string(repo["base_ref"]).startswith("-"), "Invalid base ref")
        git(repo["path"], "rev-parse", "--verify", repo["base_ref"] + "^{commit}")
        repo["worktree_root"] = str(path_at(repo["worktree_root"], base, exists=False))
    require(isinstance(config["roles"], dict) and config["roles"], "Declare roles explicitly")
    for key, role in config["roles"].items():
        label(key, "role")
        fields(role, ("skill", "contexts", "sessions", "create"), ("environment", "procedure_ref", "initial"))
        require(string(role["skill"], "phase skill") in PHASES, "Unsupported phase skill")
        role.setdefault("initial", 1)
        require(type(role["initial"]) is int and 0 <= role["initial"] <= 10000, "Invalid initial role capacity")
        require(isinstance(role["sessions"], list), "sessions must be an array")
        keys = [session_key(item) for item in role["sessions"]]
        require(len(keys) == len(set(keys)), "Duplicate session binding")
        require(isinstance(role["contexts"], list), "contexts must be an array")
        for ctx in role["contexts"]:
            fields(ctx, ("scope", "name"), ("section",))
            require(ctx["scope"] in ("local", "global"), "Use explicit local/global context scope")
            name = string(ctx["name"], "context name")
            require(not any(c in name for c in "/\\:#") and not name.endswith((".md", "."))
                    and name not in (".", ".."), "Use an exact context name without path/extension")
            if "section" in ctx:
                string(ctx["section"], "context section")
        creation = role["create"]
        if creation is not None:
            fields(creation, ("target",))
            target = creation["target"]
            require(isinstance(target, dict), "Invalid creation target")
            if target.get("type") == "projectless":
                fields(target, ("type", "directoryName"))
                label(target["directoryName"], "directory name")
            else:
                fields(target, ("type", "projectId", "base_ref"))
                require(target["type"] == "project", "Creation supports local project or projectless only")
                label(target["projectId"], "project ID")
                require(not string(target["base_ref"]).startswith("-"), "Invalid creation base ref")
        if role["skill"] == "release":
            string(role.get("environment"), "release environment")
            fields(role.get("procedure_ref"), ("path", "sha256"))
            role["procedure_ref"]["path"] = str(path_at(role["procedure_ref"]["path"], base))
        else:
            require("environment" not in role and "procedure_ref" not in role, "Release fields belong to release roles")
    limits = config["limits"]
    fields(limits, ("max_live", "max_created", "max_depth", "max_nonprogress", "reuse_after"))
    for key, value in limits.items():
        require(type(value) is int and 0 <= value <= 10000, f"Invalid limit: {key}")
    require(limits["max_live"] >= 1 and limits["max_nonprogress"] >= 1
            and limits["reuse_after"] >= 1 and limits["max_depth"] <= 1, "Invalid capacity/depth/progress limits")
    stages = config["stages"]
    require(isinstance(stages, list) and stages, "stages must be a nonempty array")
    seen = {}
    for stage in stages:
        fields(stage, ("id", "role", "after", "routing"))
        key = label(stage["id"], "stage")
        require(key not in seen, "Duplicate stage")
        require(label(stage["role"], "stage role") in config["roles"], "Unknown stage role")
        require(stage["routing"] in ("any", "split", "join"), "Unsupported routing")
        strings(stage["after"], "stage dependencies")
        phase = config["roles"][stage["role"]]["skill"]
        require(stage["routing"] != "split" or PHASES[phase] == 2, "Only execution stages may split")
        for predecessor in stage["after"]:
            require(predecessor in seen, "Stages must be topologically ordered without cycles/dangling edges")
            previous = config["roles"][seen[predecessor]["role"]]["skill"]
            require(PHASES[previous] <= PHASES[phase], "Use runtime repair/replan, not backward stage edges")
            require(not (previous in ("m-go", "m-continue") and phase == "m-test"),
                    "Composite owns its test loop; do not attach a duplicate test stage")
        seen[key] = stage
    return config


def state_root(explicit=None):
    if explicit:
        return path_at(explicit, Path.cwd(), exists=False)
    root = os.environ.get("CODEX_HOME")
    require(root, "Pass --state-root or set CODEX_HOME; no state directory was inferred", "state_root_required")
    return path_at(root, Path.cwd(), exists=False) / "m-pipeline"


def artifact(ref, roots):
    fields(ref, ("path", "sha256"))
    path = path_at(ref["path"], Path.cwd())
    require(path.is_file() and any(inside(path, root) for root in roots), "Artifact is outside admitted roots")
    require("context" not in [p.casefold() for p in path.parts], "Context bodies cannot be evidence artifacts")
    require(isinstance(ref["sha256"], str) and re.fullmatch(r"[a-f0-9]{64}", ref["sha256"]), "Invalid SHA-256")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == ref["sha256"], "Artifact changed; refresh evidence", "stale_artifact")
    return {"path": str(path), "sha256": ref["sha256"]}


def plan_ref(value, worktree):
    fields(value, ("path", "sections"), ("revision",))
    path = path_at(value["path"], worktree)
    require(path.parent == Path(worktree).resolve() and path.name in ("plan.md", "todo.md"),
            "Each repository uses its worktree-root plan.md/todo.md")
    strings(value["sections"], "plan definition sections", nonempty=True)
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    headings = []
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        if fence is None:
            match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if match:
                headings.append((index, len(match[1]), match[2]))
    selected = []
    for section in value["sections"]:
        matches = [(i, level) for i, level, title in headings if title == section]
        require(len(matches) == 1, f"Plan section is absent or ambiguous: {section}")
        start, level = matches[0]
        end = next((i for i, depth, _ in headings if i > start and depth <= level), len(lines))
        selected.append("\n".join(re.sub(r"^(\s*- )\[[ xX]\]", r"\1[]", line)
                                  for line in lines[start:end]).strip())
    revision = digest(selected)
    if "revision" in value:
        require(value["revision"] == revision, "Plan definition changed; re-review affected tasks", "stale_plan")
    return {"path": str(path), "sections": value["sections"], "revision": revision}


def snapshot(config, value, allow_removed=False):
    require(isinstance(value, dict) and value, "Repository snapshot is required")
    result = {}
    for key, item in value.items():
        require(key in config["repositories"], "Undeclared repository")
        fields(item, ("worktree", "commit"))
        repo = config["repositories"][key]
        worktree = path_at(item["worktree"], config["project_root"], exists=not allow_removed)
        require(inside(worktree, repo["worktree_root"]) and worktree != Path(repo["path"]),
                "Use a dedicated worktree inside the configured worktree root")
        require(isinstance(item["commit"], str) and re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", item["commit"]),
                "Use an exact full commit ID")
        git(repo["path"], "cat-file", "-e", item["commit"] + "^{commit}")
        if worktree.exists():
            require(git_identity(worktree) == git_identity(repo["path"]), "Worktree belongs to another repository")
            require(path_key(git(worktree, "rev-parse", "--show-toplevel")) == path_key(worktree),
                    "Worktree must be its repository root")
            require(git(worktree, "rev-parse", "HEAD") == item["commit"], "Worktree HEAD differs from candidate", "stale_candidate")
            require(not git(worktree, "status", "--porcelain"), "Commit/checkpoint pending changes before handoff", "dirty_worktree")
        else:
            require(allow_removed, "Missing worktree")
        result[key] = {"worktree": str(worktree), "commit": item["commit"]}
    return result
