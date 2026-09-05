"""Disposable Git projects and a deterministic fake host; not real-host evidence."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = REPO_ROOT / "skills" / "m-pipeline" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from pipeline_lib.config import git, plan_ref
from pipeline_lib.store import Store
from pipeline_lib.workflow import Engine


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    return str(path)


def proof(path):
    return {"path": str(path), "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pipeline-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "project"
        self.docs = self.root / "docs"
        self.worktrees = self.root / "worktrees"
        self.repo.mkdir()
        self.docs.mkdir()
        self.worktrees.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Pipeline Fixture")
        git(self.repo, "config", "user.email", "fixture@example.invalid")
        git(self.repo, "config", "core.autocrlf", "false")
        self.plan_text = "# Fixture\n\n## Scope\nLocal fixture only.\n\n## Task A\n- [ ] Write a.txt\n\n## Task B\n- [ ] Write b.txt\n\n## Progress\nPending.\n"
        (self.repo / "plan.md").write_text(self.plan_text, encoding="utf-8")
        (self.repo / "a.txt").write_text("initial\n", encoding="utf-8")
        (self.repo / "b.txt").write_text("initial\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "fixture: initialize")
        self.commit = git(self.repo, "rev-parse", "HEAD")
        (self.docs / "brief.md").write_text("Disposable test scope only.\n", encoding="utf-8")
        self.actor = {"host_id": "local", "thread_id": "fixture-coordinator"}
        self.worker = {"host_id": "local", "thread_id": "fixture-worker"}
        self.worker2 = {"host_id": "local", "thread_id": "fixture-worker-2"}
        self.config = {
            "version": 1, "project_root": str(self.repo), "docs_root": str(self.docs),
            "repositories": {"code": {"path": str(self.repo), "base_ref": "main", "worktree_root": str(self.worktrees)}},
            "roles": {"executor": {"skill": "m-execute", "contexts": [], "sessions": [self.worker, self.worker2], "create": None}},
            "stages": [{"id": "execute", "role": "executor", "after": [], "routing": "split"}],
            "limits": {"max_live": 6, "max_created": 8, "max_depth": 1, "max_nonprogress": 3, "reuse_after": 20},
        }
        self.store = Store(self.root / "state")
        self.engine = Engine(self.store)
        self.run_id = "run-one"

    def request(self, action, payload=None, run_id=None):
        return {"action": action, "run_id": run_id or self.run_id, "actor": self.actor, "payload": payload or {}}

    def call(self, action, payload=None, run_id=None):
        return self.engine.apply(self.request(action, payload, run_id))

    def start(self, run_id=None, bind=True):
        run_id = run_id or self.run_id
        blueprint = save(self.root / (run_id + ".json"), self.config)
        self.call("init", {"blueprint": blueprint}, run_id)
        self.call("authorize", {"source_ref": "fixture:user-launch", "brief": proof(self.docs / "brief.md"),
                               "actions": sorted({r["skill"] for r in self.config["roles"].values()}),
                               "repositories": list(self.config["repositories"]), "environments": ["fixture"],
                               "review_mode": "user", "review_ref": "fixture:reviewed-plan", "creation_limit": 8,
                               "write_scope": {key: ["."] for key in self.config["repositories"]}}, run_id)
        if bind:
            self.call("bind", {"role": "executor", "session": self.worker, "cwd": str(self.root), "observation_ref": "fake-host:lookup"}, run_id)
            self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:idle"}, run_id)

    def tree(self, name):
        path = self.worktrees / name
        git(self.repo, "worktree", "add", "-b", "fixture-" + name, str(path), self.commit)
        return path

    def packet(self, name="job-a", stage="execute", tree=None, task="A", writes=None):
        tree = tree or self.tree(name)
        return {"id": name, "stage": stage, "kind": "work", "task_ids": [task], "requires": [], "parent": None,
                "repositories": {"code": {"worktree": str(tree), "commit": git(tree, "rev-parse", "HEAD")}},
                "plans": {"code": plan_ref({"path": str(tree / "plan.md"), "sections": ["Scope", "Task A", "Task B"]}, tree)},
                "write_set": [{"repo": "code", "path": writes or ("a.txt" if task == "A" else "b.txt")}],
                "resources": [], "inputs": [proof(self.docs / "brief.md")], "review_ref": "fixture:plan-review"}

    def admit(self, packets, run_id=None):
        return self.call("admit", {"jobs": packets, "seal_stages": list(dict.fromkeys(p["stage"] for p in packets))}, run_id)

    def result(self, dispatch, outcome="passed", packet=None):
        packet = packet or dispatch["envelope"]["packet"]
        report = self.docs / (dispatch["operation_id"] + ".md")
        report.write_text("Fake-host evidence for deterministic tests.\n", encoding="utf-8")
        receiver = dispatch["envelope"]["receiver"].split(":", 1)
        self.call("observe", {"session": {"host_id": receiver[0], "thread_id": receiver[1]},
                              "status": "idle", "observation_ref": "fake-host:completed-after-dispatch"}, dispatch["run_id"])
        return {"operation_id": dispatch["operation_id"], "session": {"host_id": receiver[0], "thread_id": receiver[1]},
                "outcome": outcome, "task_ids": packet["task_ids"], "plans": packet["plans"], "repositories": packet["repositories"],
                "report": proof(report), "evidence": [proof(report)], "review_ref": "fixture:semantic-review",
                "failure_signature": None if outcome == "passed" else "fixture-failure"}

    def delivered(self, dispatch):
        return self.call("operation_result", {"operation_id": dispatch["operation_id"], "outcome": "delivered", "observation_ref": "fake-host:sent"})
