from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = (
    REPO_ROOT
    / "skills"
    / "m-orchestrator"
    / "scripts"
    / "orchestrator_runtime.py"
)
SPEC = importlib.util.spec_from_file_location("m_orchestrator_runtime", RUNTIME_PATH)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


def config_text(
    project_id: str,
    tester_capacity: int = 1,
    host_enabled: bool = False,
    host_capacity: int = 1,
) -> str:
    enabled = "true" if host_enabled else "false"
    return f'''schema_version = 1
project_id = "{project_id}"
docs_root = "docs"
base_branch = "main"

[commands.discuss]
skill = "m-discuss"
contexts = ["local:planner"]

[commands.plan]
skill = "m-plan"
contexts = ["local:planner"]

[commands.execute]
skill = "m-execute"
contexts = ["local:worker"]
require_lightweight_gate = true

[commands.test]
skill = "m-test"
contexts = ["local:tester"]
pool = "tester"

[commands.archive]
skill = "m-archive"
contexts = ["local:archive"]
pool = "merge"

[pools.tester]
capacity = {tester_capacity}
queue = "fifo"
lease_timeout_seconds = 60

[pools.merge]
capacity = 1
queue = "fifo"
lease_timeout_seconds = 60

[environment]
namespace = "{project_id}"

[host_budget]
enabled = {enabled}
host_id = "local"
resource = "testers"
capacity = {host_capacity}
lease_timeout_seconds = 60
'''


def config_v2_text(
    project_id: str,
    repositories: list[tuple[str, str, str]],
    tester_capacity: int = 1,
    host_enabled: bool = False,
    host_capacity: int = 1,
) -> str:
    enabled = "true" if host_enabled else "false"
    repository_blocks = "\n".join(
        f'''[[repositories]]
id = "{repository_id}"
path = "{path}"
base_branch = "{base_branch}"
'''
        for repository_id, path, base_branch in repositories
    )
    return f'''schema_version = 2
project_id = "{project_id}"
docs_root = "docs"

{repository_blocks}
[commands.discuss]
skill = "m-discuss"
contexts = ["local:planner"]

[commands.plan]
skill = "m-plan"
contexts = ["local:planner"]

[commands.execute]
skill = "m-execute"
contexts = ["local:worker"]
require_lightweight_gate = true

[commands.test]
skill = "m-test"
contexts = ["local:tester"]
pool = "tester"

[commands.archive]
skill = "m-archive"
contexts = ["local:archive"]
pool = "merge"

[pools.tester]
capacity = {tester_capacity}
queue = "fifo"
lease_timeout_seconds = 60

[pools.merge]
capacity = 1
queue = "fifo"
lease_timeout_seconds = 60

[environment]
namespace = "{project_id}"

[host_budget]
enabled = {enabled}
host_id = "local"
resource = "testers"
capacity = {host_capacity}
lease_timeout_seconds = 60
'''


def run_fixture_git(repository: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return process.stdout.strip()


def start_archive_acquire(project_root: Path, task_id: str) -> subprocess.Popen[str]:
    return subprocess.Popen(
        [
            sys.executable,
            str(RUNTIME_PATH),
            "pool",
            "try-acquire",
            "--project-root",
            str(project_root),
            "--pool",
            "merge",
            "--task-id",
            task_id,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def finish_process(process: subprocess.Popen[str], timeout: float = 20) -> tuple[str, str]:
    try:
        return process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        raise


class ProjectFixture:
    def __init__(
        self,
        root: Path,
        project_id: str,
        tester_capacity: int = 1,
        host_enabled: bool = False,
        host_capacity: int = 1,
    ):
        self.root = root
        root.mkdir(parents=True)
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(root)],
            check=True,
            capture_output=True,
            text=True,
        )
        (root / "seed.txt").write_text("initial\n", encoding="utf-8")
        run_fixture_git(root, "add", "seed.txt")
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "user.name=Codex Tests",
                "-c",
                "user.email=codex-tests@example.invalid",
                "commit",
                "-q",
                "-m",
                "initial",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        context_root = root / "docs" / "context"
        context_root.mkdir(parents=True)
        for name in ("planner", "worker", "tester", "archive"):
            (context_root / f"{name}.md").write_text(
                f"# {name}\n\n## Constraints\n\n- project only\n", encoding="utf-8"
            )
        config_root = root / ".codex"
        config_root.mkdir()
        self.config_path = config_root / "m-orchestrator.toml"
        self.config_path.write_text(
            config_text(
                project_id,
                tester_capacity=tester_capacity,
                host_enabled=host_enabled,
                host_capacity=host_capacity,
            ),
            encoding="utf-8",
        )
        self.plan_path = root / "plan.md"
        self.plan_path.write_text("# Confirmed plan\n", encoding="utf-8")
        self.config = runtime.load_config(root)

    def evidence(self, name: str, body: dict) -> Path:
        path = self.root / f"{name}.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    def prepare_waiting_task(self, task_id: str, change_id: str | None = None):
        change = change_id or f"change-{task_id}"
        runtime.create_task(self.config, task_id, str(self.plan_path))
        runtime.transition_task(self.config, task_id, "PLANNED", "DISPATCHING")
        runtime.bind_worker(
            self.config, task_id, f"worker-{task_id}", "local"
        )
        gate = self.evidence(
            f"gate-{task_id}", {"status": "Passed", "change_id": change}
        )
        runtime.transition_task(
            self.config,
            task_id,
            "EXECUTING",
            "WAITING_FOR_TESTER",
            str(gate),
            change,
        )
        return runtime.enqueue_task(self.config, "tester", task_id)


class MultiRepoProjectFixture:
    def __init__(
        self,
        root: Path,
        project_id: str = "umbrella",
        repository_ids: tuple[str, ...] = ("service-a", "service-b"),
        empty_umbrella_git: bool = False,
        host_enabled: bool = False,
        host_capacity: int = 1,
    ):
        self.root = root
        root.mkdir(parents=True)
        if empty_umbrella_git:
            (root / ".git").mkdir()
        context_root = root / "docs" / "context"
        context_root.mkdir(parents=True)
        for name in ("planner", "worker", "tester", "archive"):
            (context_root / f"{name}.md").write_text(
                f"# {name}\n\n## Constraints\n\n- umbrella project only\n", encoding="utf-8"
            )
        self.repository_roots: dict[str, Path] = {}
        repository_config: list[tuple[str, str, str]] = []
        for repository_id in repository_ids:
            repository_root = root / "repo" / repository_id
            repository_root.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "init", "-q", "-b", "main", str(repository_root)],
                check=True,
                capture_output=True,
                text=True,
            )
            (repository_root / "seed.txt").write_text(f"{repository_id}\n", encoding="utf-8")
            run_fixture_git(repository_root, "add", "seed.txt")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository_root),
                    "-c",
                    "user.name=Codex Tests",
                    "-c",
                    "user.email=codex-tests@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    "initial",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.repository_roots[repository_id] = repository_root
            repository_config.append((repository_id, f"repo/{repository_id}", "main"))
        config_root = root / ".codex"
        config_root.mkdir()
        self.config_path = config_root / "m-orchestrator.toml"
        self.config_path.write_text(
            config_v2_text(
                project_id,
                repository_config,
                host_enabled=host_enabled,
                host_capacity=host_capacity,
            ),
            encoding="utf-8",
        )
        self.config = runtime.load_config(root)

    def create_manifest(self, task_id: str, selected: tuple[str, ...] | None = None) -> Path:
        selected_ids = selected or tuple(self.repository_roots)
        repository_entries: list[dict[str, object]] = []
        for repository_id in selected_ids:
            repository_root = self.repository_roots[repository_id]
            worktree = self.root / "worktrees" / task_id / repository_id
            worktree.parent.mkdir(parents=True, exist_ok=True)
            branch = f"feat/{task_id.lower()}-{repository_id}"
            run_fixture_git(repository_root, "worktree", "add", "-q", "-b", branch, str(worktree), "main")
            plan_path = worktree / "plan.md"
            plan_path.write_text(f"# Confirmed plan for {task_id}\n", encoding="utf-8")
            run_fixture_git(worktree, "add", "plan.md")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(worktree),
                    "-c",
                    "user.name=Codex Tests",
                    "-c",
                    "user.email=codex-tests@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    "plan",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            repository_entries.append(
                {
                    "id": repository_id,
                    "worktree": str(worktree),
                    "branch": branch,
                    "base_ref": "main",
                    "planning_ref": run_fixture_git(worktree, "rev-parse", "HEAD"),
                    "plan": str(plan_path),
                    "write_set": ["seed.txt"],
                }
            )
        manifest = {
            "schema_version": 1,
            "task_id": task_id,
            "title": f"Task {task_id}",
            "plan": repository_entries[0]["plan"],
            "repositories": repository_entries,
            "acceptance": ["All selected repositories pass their checks"],
            "tests": ["Run focused repository tests"],
            "rollback": "Revert the task commits in reverse integration order.",
            "planner": {"thread_id": "planner-thread", "host_id": "local"},
        }
        manifest_path = self.root / f"{task_id}-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest_path

    def evidence(self, name: str, body: dict) -> Path:
        path = self.root / f"{name}.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    def prepare_archive_task(self, task_id: str) -> dict:
        manifest = self.create_manifest(task_id)
        task = runtime.create_task(self.config, manifest_path_value=str(manifest))
        runtime.transition_task(self.config, task_id, "PLANNED", "DISPATCHING")
        runtime.bind_worker(self.config, task_id, f"worker-{task_id}", "local")
        change_id = runtime.compute_task_change_id(self.config, task_id)
        gate = self.evidence(
            f"gate-{task_id}",
            {
                "status": "Passed",
                "change_id": change_id,
                "repositories": [
                    {"id": item["id"], "status": "Passed"}
                    for item in task["repositories"]
                ],
            },
        )
        runtime.transition_task(
            self.config,
            task_id,
            "EXECUTING",
            "WAITING_FOR_TESTER",
            str(gate),
            change_id,
        )
        runtime.enqueue_task(self.config, "tester", task_id)
        tester_lease = runtime.try_acquire(self.config, "tester", task_id)["lease"]
        passed = self.evidence(f"test-passed-{task_id}", {"status": "Passed"})
        runtime.transition_task(
            self.config, task_id, "TESTING", "TEST_PASSED", str(passed)
        )
        runtime.release_lease(
            self.config, "tester", task_id, tester_lease["lease_id"]
        )
        runtime.transition_task(
            self.config, task_id, "TEST_PASSED", "WAITING_FOR_MERGE"
        )
        queued = runtime.enqueue_task(self.config, "merge", task_id)
        if queued["status"] != "Queued":
            raise AssertionError(f"Task {task_id} did not reach archive queue: {queued}")
        return runtime.load_task(self.config, task_id)


class MOrchestratorRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.previous_home = os.environ.get("M_ORCHESTRATOR_HOME")
        os.environ["M_ORCHESTRATOR_HOME"] = str(self.root / "global-runtime")

    def tearDown(self):
        if self.previous_home is None:
            os.environ.pop("M_ORCHESTRATOR_HOME", None)
        else:
            os.environ["M_ORCHESTRATOR_HOME"] = self.previous_home
        self.temporary.cleanup()

    def test_process_liveness_probe_is_safe_for_current_process(self):
        self.assertTrue(runtime.process_is_alive(os.getpid()))

    def test_stale_lock_from_exited_process_is_reclaimed(self):
        lock_path = self.root / "runtime" / ".lock"
        lock_path.parent.mkdir(parents=True)
        lock_path.mkdir()
        owner_path = lock_path / "owner.json"
        runtime.atomic_write_json(
            owner_path,
            {
                "owner_token": "abandoned",
                "pid": 2147483647,
                "acquired_at": runtime.utc_now(),
            },
        )
        stale_at = time.time() - 60
        os.utime(owner_path, (stale_at, stale_at))
        original_stale = runtime.LOCK_STALE_SECONDS
        runtime.LOCK_STALE_SECONDS = 0.01
        try:
            with runtime.directory_lock(lock_path):
                self.assertTrue(lock_path.is_dir())
        finally:
            runtime.LOCK_STALE_SECONDS = original_stale
        self.assertFalse(lock_path.exists())

    def test_live_lock_is_not_reclaimed_across_processes(self):
        lock_path = self.root / "runtime" / ".lock"
        lock_path.parent.mkdir(parents=True)
        ready_path = self.root / "lock-ready"
        program = """
import importlib.util
from pathlib import Path
import sys
import time

runtime_path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("lock_holder_runtime", runtime_path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
with module.directory_lock(Path(sys.argv[2])):
    Path(sys.argv[3]).write_text("ready", encoding="utf-8")
    time.sleep(0.5)
"""
        process = subprocess.Popen(
            [
                sys.executable,
                "-B",
                "-c",
                program,
                str(RUNTIME_PATH),
                str(lock_path),
                str(ready_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        original_stale = runtime.LOCK_STALE_SECONDS
        original_timeout = runtime.LOCK_TIMEOUT_SECONDS
        try:
            deadline = time.monotonic() + 5
            while not ready_path.exists() and process.poll() is None:
                if time.monotonic() >= deadline:
                    self.fail("Child process did not acquire the runtime lock")
                time.sleep(0.01)
            self.assertIsNone(process.poll())
            runtime.LOCK_STALE_SECONDS = 0.05
            runtime.LOCK_TIMEOUT_SECONDS = 2.0
            with runtime.directory_lock(lock_path):
                self.assertTrue(lock_path.is_dir())
        finally:
            runtime.LOCK_STALE_SECONDS = original_stale
            runtime.LOCK_TIMEOUT_SECONDS = original_timeout
            try:
                stdout, stderr = process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
        self.assertEqual(process.returncode, 0, f"{stdout}\n{stderr}")
        self.assertFalse(lock_path.exists())

    def test_valid_config_resolves_isolated_git_runtime(self):
        project = ProjectFixture(self.root / "project-a", "project-a")
        result = runtime.config_result(project.config)
        self.assertEqual(result["status"], "Valid")
        self.assertEqual(result["project_id"], "project-a")
        self.assertTrue(str(project.config.runtime_root).startswith(str(project.config.git_common_dir)))

    def test_cli_validate_emits_structured_json(self):
        project = ProjectFixture(self.root / "project", "project")
        process = subprocess.run(
            [
                sys.executable,
                str(RUNTIME_PATH),
                "config",
                "validate",
                "--project-root",
                str(project.root),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "Valid")
        self.assertEqual(payload["project_id"], "project")

    def test_project_ids_and_repositories_resolve_to_distinct_runtime_roots(self):
        first = ProjectFixture(self.root / "first", "shared-name")
        second = ProjectFixture(self.root / "second", "shared-name")
        self.assertNotEqual(first.config.runtime_root, second.config.runtime_root)

        first.config_path.write_text(config_text("second-logical-project"), encoding="utf-8")
        logical_second = runtime.load_config(first.root)
        self.assertNotEqual(first.config.runtime_root, logical_second.runtime_root)
        self.assertEqual(first.config.git_common_dir, logical_second.git_common_dir)

    def test_v2_non_git_umbrella_ignores_empty_git_and_registers_planner(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", empty_umbrella_git=True
        )
        result = runtime.config_result(project.config)
        self.assertEqual(result["schema_version"], 2)
        self.assertIsNone(result["git_common_dir"])
        self.assertEqual(
            {item["id"] for item in result["repositories"]},
            {"service-a", "service-b"},
        )
        self.assertEqual(
            project.config.runtime_root.relative_to(project.config.project_root),
            Path(".codex-runtime") / "m-orchestrator" / "projects" / "umbrella",
        )
        planner = runtime.register_planner(
            project.config, "planner-thread", "local", False, None
        )
        self.assertEqual(planner["thread_id"], "planner-thread")

    def test_v2_same_project_id_in_different_umbrellas_is_isolated(self):
        first = MultiRepoProjectFixture(self.root / "first", project_id="shared")
        second = MultiRepoProjectFixture(self.root / "second", project_id="shared")
        self.assertNotEqual(first.config.runtime_root, second.config.runtime_root)
        self.assertEqual(
            first.config.runtime_root.relative_to(first.config.project_root).parts[0],
            ".codex-runtime",
        )
        self.assertEqual(
            second.config.runtime_root.relative_to(second.config.project_root).parts[0],
            ".codex-runtime",
        )

    def test_v2_host_budget_isolates_same_project_and_task_ids_across_umbrellas(self):
        first = MultiRepoProjectFixture(
            self.root / "first",
            project_id="shared",
            repository_ids=("service-a",),
            host_enabled=True,
        )
        second = MultiRepoProjectFixture(
            self.root / "second",
            project_id="shared",
            repository_ids=("service-a",),
            host_enabled=True,
        )

        first_lease = runtime.acquire_host_lease(first.config, "T-1")
        self.assertIsNotNone(first_lease)
        self.assertNotIn("shared", first_lease["owner"])
        self.assertNotIn("T-1", first_lease["owner"])
        self.assertEqual(
            first_lease["project_instance_id"], runtime.project_instance_id(first.config)
        )
        self.assertNotEqual(
            runtime.project_instance_id(first.config),
            runtime.project_instance_id(second.config),
        )

        waiting = runtime.acquire_host_lease(second.config, "T-1")
        self.assertEqual(waiting, {"status": "Waiting"})
        runtime.release_host_lease(first.config, first_lease["lease_id"], "T-1")
        second_lease = runtime.acquire_host_lease(second.config, "T-1")
        self.assertNotEqual(first_lease["lease_id"], second_lease["lease_id"])

    def test_legacy_host_lease_can_be_heartbeated_and_released_by_exact_id(self):
        project = ProjectFixture(
            self.root / "project", "project", host_enabled=True, host_capacity=1
        )
        host_root = runtime.ensure_host_pool(project.config)
        lease_id = "a" * 32
        now = runtime.utc_now()
        runtime.atomic_write_json(
            host_root / "leases" / f"{lease_id}.json",
            {
                "host_id": "local",
                "resource": "testers",
                "owner": "project:T-1",
                "lease_id": lease_id,
                "acquired_at": now,
                "heartbeat_at": now,
                "lease_timeout_seconds": 60,
            },
        )

        runtime.heartbeat_host_lease(project.config, lease_id, "T-1")
        runtime.release_host_lease(project.config, lease_id, "T-1")
        self.assertFalse((host_root / "leases" / f"{lease_id}.json").exists())

    def test_v1_non_git_umbrella_reports_schema_v2_migration(self):
        root = self.root / "legacy-umbrella"
        root.mkdir()
        context_root = root / "docs" / "context"
        context_root.mkdir(parents=True)
        for name in ("planner", "worker", "tester", "archive"):
            (context_root / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
        config_root = root / ".codex"
        config_root.mkdir()
        (config_root / "m-orchestrator.toml").write_text(
            config_text("legacy-umbrella"), encoding="utf-8"
        )
        with self.assertRaisesRegex(
            runtime.OrchestratorError, "schema_version 2 with explicit"
        ) as raised:
            runtime.load_config(root)
        self.assertNotIn("git init", str(raised.exception))

    def test_v2_does_not_start_while_legacy_v1_runtime_is_active(self):
        project = ProjectFixture(self.root / "project", "project")
        runtime.create_task(project.config, "T-1", str(project.plan_path))
        project.config_path.write_text(
            config_v2_text("project", [("root", ".", "main")]), encoding="utf-8"
        )
        v2_config = runtime.load_config(project.root)
        with self.assertRaisesRegex(runtime.OrchestratorError, "schema_version 1 runtime"):
            runtime.config_result(v2_config)

    def test_v2_invalid_repository_names_the_declared_path(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        original = project.config_path.read_text(encoding="utf-8")
        project.config_path.write_text(
            original.replace('path = "repo/service-a"', 'path = "repo/missing"'),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            runtime.OrchestratorError, r"repositories\[0\]\.path directory does not exist"
        ):
            runtime.load_config(project.root)

    def test_v2_rejects_duplicate_and_traversing_repository_paths(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        project.config_path.write_text(
            config_v2_text(
                "umbrella",
                [
                    ("first", "repo/service-a", "main"),
                    ("alias", "repo/service-a", "main"),
                ],
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "resolves to the same path"):
            runtime.load_config(project.root)

        project.config_path.write_text(
            config_v2_text("umbrella", [("outside", "../outside", "main")]),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "traversal segments"):
            runtime.load_config(project.root)

    def test_v2_task_manifest_persists_repository_set_and_composite_gate(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        manifest = project.create_manifest("T-1")
        task = runtime.create_task(project.config, manifest_path_value=str(manifest))
        self.assertEqual(
            [item["id"] for item in task["repositories"]],
            ["service-a", "service-b"],
        )
        self.assertEqual(task["planner"]["thread_id"], "planner-thread")
        change_id = runtime.compute_task_change_id(project.config, "T-1")
        runtime.transition_task(project.config, "T-1", "PLANNED", "DISPATCHING")
        runtime.bind_worker(project.config, "T-1", "worker-T-1", "local")
        gate = project.evidence(
            "gate-T-1",
            {
                "status": "Passed",
                "change_id": change_id,
                "repositories": [
                    {"id": "service-a", "status": "Passed"},
                    {"id": "service-b", "status": "Passed"},
                ],
            },
        )
        runtime.transition_task(
            project.config,
            "T-1",
            "EXECUTING",
            "WAITING_FOR_TESTER",
            str(gate),
            change_id,
        )
        queued = runtime.enqueue_task(project.config, "tester", "T-1")
        self.assertEqual(queued["status"], "Queued")
        first_worktree = Path(task["repositories"][0]["worktree"])
        (first_worktree / "seed.txt").write_text("changed after gate\n", encoding="utf-8")
        with self.assertRaisesRegex(runtime.OrchestratorError, "changed after the lightweight gate"):
            runtime.try_acquire(project.config, "tester", "T-1")

    def test_v2_task_create_retry_is_idempotent_after_worker_commit(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        manifest_path = project.create_manifest("T-1")
        created = runtime.create_task(project.config, manifest_path_value=str(manifest_path))
        worktree = Path(created["repositories"][0]["worktree"])
        (worktree / "seed.txt").write_text("worker implementation\n", encoding="utf-8")
        run_fixture_git(worktree, "add", "seed.txt")
        subprocess.run(
            [
                "git",
                "-C",
                str(worktree),
                "-c",
                "user.name=Codex Tests",
                "-c",
                "user.email=codex-tests@example.invalid",
                "commit",
                "-q",
                "-m",
                "implementation",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        retried = runtime.create_task(
            project.config, manifest_path_value=str(manifest_path)
        )
        self.assertEqual(retried, created)

        changed_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed_manifest["title"] = "Changed title"
        manifest_path.write_text(json.dumps(changed_manifest), encoding="utf-8")
        with self.assertRaisesRegex(runtime.OrchestratorError, "different manifest"):
            runtime.create_task(project.config, manifest_path_value=str(manifest_path))

    def test_v2_cli_creates_manifest_task_and_computes_change_id(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        manifest = project.create_manifest("T-1")
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        created = subprocess.run(
            [
                sys.executable,
                str(RUNTIME_PATH),
                "task",
                "create",
                "--project-root",
                str(project.root),
                "--manifest",
                str(manifest),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(json.loads(created.stdout)["task_id"], "T-1")
        computed = subprocess.run(
            [
                sys.executable,
                str(RUNTIME_PATH),
                "task",
                "change-id",
                "--project-root",
                str(project.root),
                "--task-id",
                "T-1",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertEqual(computed.returncode, 0, computed.stderr)
        self.assertRegex(json.loads(computed.stdout)["change_id"], r"^[a-f0-9]{64}$")

    def test_v2_task_manifest_rejects_unknown_repository_and_legacy_create(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        with self.assertRaisesRegex(runtime.OrchestratorError, "requires --manifest"):
            runtime.create_task(project.config, "T-legacy", str(project.root / "missing-plan.md"))
        self.assertFalse(project.config.runtime_root.exists())

        manifest_path = project.create_manifest("T-1", selected=("service-a",))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["repositories"][0]["id"] = "unknown"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(runtime.OrchestratorError, "not configured"):
            runtime.create_task(project.config, manifest_path_value=str(manifest_path))

    def test_v2_task_manifest_rejects_worktree_outside_project_worktrees(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        manifest_path = project.create_manifest("T-1", selected=("service-a",))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["repositories"][0]["worktree"] = str(
            project.repository_roots["service-a"]
        )
        manifest["repositories"][0]["plan"] = str(
            project.repository_roots["service-a"] / "plan.md"
        )
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(runtime.OrchestratorError, "project worktree root"):
            runtime.create_task(project.config, manifest_path_value=str(manifest_path))

    def test_v2_gate_requires_every_selected_repository(self):
        project = MultiRepoProjectFixture(self.root / "umbrella")
        manifest = project.create_manifest("T-1")
        runtime.create_task(project.config, manifest_path_value=str(manifest))
        change_id = runtime.compute_task_change_id(project.config, "T-1")
        runtime.transition_task(project.config, "T-1", "PLANNED", "DISPATCHING")
        runtime.bind_worker(project.config, "T-1", "worker-T-1", "local")
        gate = project.evidence(
            "incomplete-gate",
            {
                "status": "Passed",
                "change_id": change_id,
                "repositories": [{"id": "service-a", "status": "Passed"}],
            },
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "repository set does not match"):
            runtime.transition_task(
                project.config,
                "T-1",
                "EXECUTING",
                "WAITING_FOR_TESTER",
                str(gate),
                change_id,
            )

    def test_v2_tester_acquisition_rejects_mutated_gate_evidence(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        manifest = project.create_manifest("T-1")
        runtime.create_task(project.config, manifest_path_value=str(manifest))
        change_id = runtime.compute_task_change_id(project.config, "T-1")
        runtime.transition_task(project.config, "T-1", "PLANNED", "DISPATCHING")
        runtime.bind_worker(project.config, "T-1", "worker-T-1", "local")
        gate = project.evidence(
            "gate",
            {
                "status": "Passed",
                "change_id": change_id,
                "repositories": [{"id": "service-a", "status": "Passed"}],
            },
        )
        runtime.transition_task(
            project.config,
            "T-1",
            "EXECUTING",
            "WAITING_FOR_TESTER",
            str(gate),
            change_id,
        )
        runtime.enqueue_task(project.config, "tester", "T-1")
        gate.write_text('{"status":"Failed"}', encoding="utf-8")
        with self.assertRaisesRegex(runtime.OrchestratorError, "evidence changed"):
            runtime.try_acquire(project.config, "tester", "T-1")

    def test_config_rejects_global_context_and_missing_local_context(self):
        project = ProjectFixture(self.root / "project", "project")
        original = project.config_path.read_text(encoding="utf-8")
        project.config_path.write_text(
            original.replace('"local:tester"', '"global:tester"'), encoding="utf-8"
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "explicit local"):
            runtime.load_config(project.root)

        project.config_path.write_text(
            original.replace('"local:tester"', '"local:missing"'), encoding="utf-8"
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "does not exist"):
            runtime.load_config(project.root)

    def test_tester_queue_requires_passing_current_gate(self):
        project = ProjectFixture(self.root / "project", "project")
        runtime.create_task(project.config, "T-1", str(project.plan_path))
        runtime.transition_task(project.config, "T-1", "PLANNED", "DISPATCHING")
        runtime.bind_worker(project.config, "T-1", "worker-T-1", "local")
        with self.assertRaisesRegex(runtime.OrchestratorError, "must be WAITING_FOR_TESTER"):
            runtime.enqueue_task(project.config, "tester", "T-1")

        failed_gate = project.evidence(
            "failed-gate", {"status": "Failed", "change_id": "change-1"}
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "status must be Passed"):
            runtime.transition_task(
                project.config,
                "T-1",
                "EXECUTING",
                "WAITING_FOR_TESTER",
                str(failed_gate),
                "change-1",
            )

    def test_acquire_release_and_repair_clear_gate(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        acquired = runtime.try_acquire(project.config, "tester", "T-1")
        self.assertEqual(acquired["status"], "Acquired")
        lease_id = acquired["lease"]["lease_id"]
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "TESTING")
        retried = runtime.try_acquire(project.config, "tester", "T-1")
        self.assertTrue(retried["idempotent"])
        self.assertEqual(retried["lease"]["lease_id"], lease_id)

        failure = project.evidence("test-failure", {"status": "Failed"})
        runtime.transition_task(
            project.config,
            "T-1",
            "TESTING",
            "TEST_FAILED",
            str(failure),
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "not consistently TESTING"):
            runtime.try_acquire(project.config, "tester", "T-1")
        released = runtime.release_lease(project.config, "tester", "T-1", lease_id)
        self.assertFalse(released["idempotent"])
        self.assertTrue(
            runtime.release_lease(project.config, "tester", "T-1", lease_id)[
                "idempotent"
            ]
        )
        runtime.transition_task(project.config, "T-1", "TEST_FAILED", "EXECUTING")
        repaired = runtime.load_task(project.config, "T-1")
        self.assertIsNone(repaired["gate"])
        self.assertIsNone(repaired["change_id"])

    def test_wrong_owner_cannot_release_lease(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        lease = runtime.try_acquire(project.config, "tester", "T-1")["lease"]
        with self.assertRaisesRegex(runtime.OrchestratorError, "ownership mismatch"):
            runtime.release_lease(
                project.config, "tester", "T-2", lease["lease_id"]
            )

    def test_release_requires_persisted_result(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        lease = runtime.try_acquire(project.config, "tester", "T-1")["lease"]
        with self.assertRaisesRegex(runtime.OrchestratorError, "is not stale"):
            runtime.reclaim_lease(
                project.config,
                "tester",
                "T-1",
                lease["lease_id"],
                "planner-thread",
                "premature recovery",
            )
        with self.assertRaisesRegex(runtime.OrchestratorError, "Persist the Tester"):
            runtime.release_lease(
                project.config, "tester", "T-1", lease["lease_id"]
            )

    def test_lease_id_path_input_is_rejected(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        with self.assertRaisesRegex(runtime.OrchestratorError, "lease_id contains unsafe"):
            runtime.release_lease(project.config, "tester", "T-1", "../../outside")

    def test_concurrent_acquisition_preserves_fifo_and_capacity(self):
        project = ProjectFixture(self.root / "project", "project", tester_capacity=1)
        project.prepare_waiting_task("T-1")
        project.prepare_waiting_task("T-2")
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    lambda task_id: runtime.try_acquire(
                        project.config, "tester", task_id
                    ),
                    ("T-1", "T-2"),
                )
            )
        self.assertEqual(sum(item["status"] == "Acquired" for item in results), 1)
        leases = list((project.config.runtime_root / "pools" / "tester" / "leases").glob("*.json"))
        self.assertEqual(len(leases), 1)
        acquired = next(item for item in results if item["status"] == "Acquired")
        self.assertEqual(acquired["lease"]["task_id"], "T-1")
        result = project.evidence("capacity-result", {"status": "Passed"})
        runtime.transition_task(
            project.config, "T-1", "TESTING", "TEST_PASSED", str(result)
        )
        runtime.release_lease(
            project.config, "tester", "T-1", acquired["lease"]["lease_id"]
        )
        second = runtime.try_acquire(project.config, "tester", "T-2")
        self.assertEqual(second["status"], "Acquired")

    def test_stale_inspection_does_not_reclaim(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        acquired = runtime.try_acquire(project.config, "tester", "T-1")
        lease_id = acquired["lease"]["lease_id"]
        lease_path = (
            project.config.runtime_root
            / "pools"
            / "tester"
            / "leases"
            / f"{lease_id}.json"
        )
        lease = runtime.read_json(lease_path)
        lease["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, lease)
        result = runtime.stale_leases(project.config, "tester")
        self.assertEqual([item["lease_id"] for item in result["stale"]], [lease_id])
        self.assertTrue(lease_path.exists())
        with self.assertRaisesRegex(runtime.OrchestratorError, "is stale"):
            runtime.try_acquire(project.config, "tester", "T-1")

    def test_stale_host_lease_is_not_silently_reused(self):
        project = ProjectFixture(
            self.root / "project", "project", host_enabled=True, host_capacity=1
        )
        lease = runtime.acquire_host_lease(project.config, "T-1")
        self.assertIsNotNone(lease)
        lease_id = lease["lease_id"]
        host_root = runtime.host_pool_root(project.config)
        self.assertIsNotNone(host_root)
        lease_path = host_root / "leases" / f"{lease_id}.json"
        stale = runtime.read_json(lease_path)
        stale["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, stale)

        with self.assertRaisesRegex(runtime.OrchestratorError, "is stale"):
            runtime.acquire_host_lease(project.config, "T-1")
        self.assertTrue(lease_path.exists())

    def test_stale_reclaim_blocks_task_and_writes_audit(self):
        project = ProjectFixture(
            self.root / "project", "project", host_enabled=True, host_capacity=1
        )
        project.prepare_waiting_task("T-1")
        lease = runtime.try_acquire(project.config, "tester", "T-1")["lease"]
        lease_id = lease["lease_id"]
        lease_path = (
            project.config.runtime_root
            / "pools"
            / "tester"
            / "leases"
            / f"{lease_id}.json"
        )
        stale = runtime.read_json(lease_path)
        stale["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, stale)

        reclaimed = runtime.reclaim_lease(
            project.config,
            "tester",
            "T-1",
            lease_id,
            "planner-thread",
            "Worker task was confirmed closed",
        )
        self.assertFalse(reclaimed["idempotent"])
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "BLOCKED")
        self.assertFalse(lease_path.exists())
        self.assertTrue(
            (
                project.config.runtime_root
                / "events"
                / f"lease-reclaim-{lease_id}.json"
            ).is_file()
        )
        self.assertTrue(
            runtime.reclaim_lease(
                project.config,
                "tester",
                "T-1",
                lease_id,
                "planner-thread",
                "Worker task was confirmed closed",
            )["idempotent"]
        )

    def test_stale_reclaim_resumes_started_audit(self):
        project = ProjectFixture(
            self.root / "project", "project", host_enabled=True, host_capacity=1
        )
        project.prepare_waiting_task("T-1")
        lease = runtime.try_acquire(project.config, "tester", "T-1")["lease"]
        lease_id = lease["lease_id"]
        lease_path = (
            project.config.runtime_root
            / "pools"
            / "tester"
            / "leases"
            / f"{lease_id}.json"
        )
        stale = runtime.read_json(lease_path)
        stale["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, stale)
        reason = "Worker task was confirmed closed"
        resolution = f"Stale lease {lease_id} reclaimed by planner-thread: {reason}"
        event_path = (
            project.config.runtime_root
            / "events"
            / f"lease-reclaim-{lease_id}.json"
        )
        runtime.atomic_write_json(
            event_path,
            {
                "event": "lease-reclaimed",
                "status": "Started",
                "project_id": project.config.project_id,
                "pool": "tester",
                "task_id": "T-1",
                "lease_id": lease_id,
                "actor": "planner-thread",
                "reason": reason,
                "started_at": runtime.utc_now(),
            },
        )
        runtime.transition_task(
            project.config,
            "T-1",
            "TESTING",
            "BLOCKED",
            reason=resolution,
        )

        recovered = runtime.reclaim_lease(
            project.config,
            "tester",
            "T-1",
            lease_id,
            "planner-thread",
            reason,
        )
        self.assertFalse(recovered["idempotent"])
        self.assertFalse(lease_path.exists())
        self.assertEqual(runtime.read_json(event_path)["status"], "Completed")

    def test_stale_host_orphan_is_reported_and_audited(self):
        project = ProjectFixture(
            self.root / "project", "project", host_enabled=True, host_capacity=1
        )
        project.prepare_waiting_task("T-1")
        host_lease = runtime.acquire_host_lease(project.config, "T-1")
        self.assertIsNotNone(host_lease)
        lease_id = host_lease["lease_id"]
        with self.assertRaisesRegex(runtime.OrchestratorError, "is not stale"):
            runtime.reclaim_host_lease(
                project.config,
                "tester",
                "T-1",
                lease_id,
                "planner-thread",
                "premature recovery",
            )
        host_root = runtime.host_pool_root(project.config)
        self.assertIsNotNone(host_root)
        lease_path = host_root / "leases" / f"{lease_id}.json"
        stale = runtime.read_json(lease_path)
        stale["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, stale)

        inspected = runtime.stale_leases(project.config, "tester")
        self.assertEqual(
            [item["lease_id"] for item in inspected["stale_host"]], [lease_id]
        )
        reclaimed = runtime.reclaim_host_lease(
            project.config,
            "tester",
            "T-1",
            lease_id,
            "planner-thread",
            "Worker stopped before project admission",
        )
        self.assertFalse(reclaimed["idempotent"])
        self.assertFalse(lease_path.exists())
        self.assertEqual(
            runtime.load_task(project.config, "T-1")["state"],
            "WAITING_FOR_TESTER",
        )
        self.assertTrue(
            runtime.reclaim_host_lease(
                project.config,
                "tester",
                "T-1",
                lease_id,
                "planner-thread",
                "Worker stopped before project admission",
            )["idempotent"]
        )

    def test_conflicting_host_pool_initialization_is_serialized(self):
        first = ProjectFixture(
            self.root / "first", "project-a", host_enabled=True, host_capacity=1
        )
        second = ProjectFixture(
            self.root / "second", "project-b", host_enabled=True, host_capacity=2
        )
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(runtime.ensure_host_pool, config)
                for config in (first.config, second.config)
            ]
            results = []
            errors = []
            for future in futures:
                try:
                    results.append(future.result())
                except runtime.OrchestratorError as exc:
                    errors.append(str(exc))

        self.assertEqual(len(results), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("Host budget mismatch for capacity", errors[0])
        host_root = runtime.host_pool_root(first.config)
        self.assertIsNotNone(host_root)
        self.assertIn(runtime.read_json(host_root / "pool.json")["capacity"], {1, 2})

    def test_host_budget_limits_separate_projects_and_releases(self):
        first = ProjectFixture(
            self.root / "first", "project-a", host_enabled=True, host_capacity=1
        )
        second = ProjectFixture(
            self.root / "second", "project-b", host_enabled=True, host_capacity=1
        )
        first.prepare_waiting_task("T-A")
        second.prepare_waiting_task("T-B")
        first_lease = runtime.try_acquire(first.config, "tester", "T-A")["lease"]
        waiting = runtime.try_acquire(second.config, "tester", "T-B")
        self.assertEqual(waiting["reason"], "host-capacity")
        result = first.evidence("host-result", {"status": "Passed"})
        runtime.transition_task(
            first.config, "T-A", "TESTING", "TEST_PASSED", str(result)
        )
        runtime.release_lease(
            first.config, "tester", "T-A", first_lease["lease_id"]
        )
        self.assertEqual(
            runtime.try_acquire(second.config, "tester", "T-B")["status"],
            "Acquired",
        )

    def test_process_archive_admission_serializes_and_resumes_same_project(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",), host_enabled=True
        )
        project.prepare_archive_task("T-1")
        project.prepare_archive_task("T-2")

        processes = [
            start_archive_acquire(project.root, task_id) for task_id in ("T-1", "T-2")
        ]
        results = []
        for process in processes:
            stdout, stderr = finish_process(process)
            self.assertEqual(process.returncode, 0, stderr)
            results.append(json.loads(stdout))

        self.assertEqual(sum(item["status"] == "Acquired" for item in results), 1)
        acquired = next(item for item in results if item["status"] == "Acquired")
        waiting = next(item for item in results if item["status"] == "Waiting")
        self.assertEqual(acquired["lease"]["task_id"], "T-1")
        self.assertIsNone(acquired["lease"]["host_lease_id"])
        self.assertIn(waiting["reason"], {"fifo", "project-capacity"})

        archive = project.evidence("archive-T-1", {"status": "Passed"})
        runtime.transition_task(
            project.config, "T-1", "ARCHIVING", "COMPLETED", str(archive)
        )
        released = runtime.release_lease(
            project.config, "merge", "T-1", acquired["lease"]["lease_id"]
        )
        self.assertEqual(released["next_ready"]["task_id"], "T-2")
        self.assertEqual(released["next_ready"]["thread_id"], "worker-T-2")
        status = runtime.project_status(project.config)
        self.assertEqual(status["pools"]["merge"]["next_ready"], released["next_ready"])
        self.assertEqual(
            runtime.try_acquire(project.config, "merge", "T-2")["status"],
            "Acquired",
        )

    def test_process_archives_run_in_parallel_between_projects_without_host_capacity(self):
        first = MultiRepoProjectFixture(
            self.root / "first",
            project_id="first",
            repository_ids=("service-a",),
            host_enabled=True,
            host_capacity=1,
        )
        second = MultiRepoProjectFixture(
            self.root / "second",
            project_id="second",
            repository_ids=("service-a",),
            host_enabled=True,
            host_capacity=1,
        )
        first.prepare_archive_task("T-A")
        second.prepare_archive_task("T-B")
        host_holder = runtime.acquire_host_lease(first.config, "TESTER-HOLDER")
        self.assertIsNotNone(host_holder)

        processes = [
            start_archive_acquire(first.root, "T-A"),
            start_archive_acquire(second.root, "T-B"),
        ]
        results = []
        for process in processes:
            stdout, stderr = finish_process(process)
            self.assertEqual(process.returncode, 0, stderr)
            results.append(json.loads(stdout))

        self.assertEqual([item["status"] for item in results], ["Acquired", "Acquired"])
        self.assertTrue(all(item["lease"]["host_lease_id"] is None for item in results))
        host_root = runtime.host_pool_root(first.config)
        self.assertEqual(len(list((host_root / "leases").glob("*.json"))), 1)
        runtime.release_host_lease(
            first.config, host_holder["lease_id"], "TESTER-HOLDER"
        )

    def test_live_pool_lock_is_not_reclaimed_after_stale_threshold(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        merge_root = runtime.pool_root(project.config, "merge")
        for ticket_path in (merge_root / "queue").glob("*.json"):
            ticket_path.unlink()

        original_issue = runtime.archive_candidate_issue
        original_stale = runtime.LOCK_STALE_SECONDS
        original_timeout = runtime.LOCK_TIMEOUT_SECONDS

        def slow_issue(config, task):
            time.sleep(0.25)
            return original_issue(config, task)

        runtime.archive_candidate_issue = slow_issue
        runtime.LOCK_STALE_SECONDS = 0.05
        runtime.LOCK_TIMEOUT_SECONDS = 2.0
        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [
                    executor.submit(
                        runtime.enqueue_task, project.config, "merge", "T-1"
                    )
                    for _ in range(2)
                ]
                results = [future.result() for future in futures]
        finally:
            runtime.archive_candidate_issue = original_issue
            runtime.LOCK_STALE_SECONDS = original_stale
            runtime.LOCK_TIMEOUT_SECONDS = original_timeout

        self.assertEqual([item["status"] for item in results], ["Queued", "Queued"])
        self.assertEqual(sorted(item["idempotent"] for item in results), [False, True])
        self.assertEqual(len(list((merge_root / "queue").glob("*.json"))), 1)

    def test_blocked_archive_resume_preserves_candidate_and_rejects_drift(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        task = project.prepare_archive_task("T-1")
        lease = runtime.try_acquire(project.config, "merge", "T-1")["lease"]
        runtime.transition_task(
            project.config,
            "T-1",
            "ARCHIVING",
            "BLOCKED",
            reason="archive process stopped before integration",
        )
        runtime.release_lease(
            project.config, "merge", "T-1", lease["lease_id"]
        )
        worktree = Path(task["repositories"][0]["worktree"])
        (worktree / "seed.txt").write_text("drift while blocked\n", encoding="utf-8")

        resumed = runtime.transition_task(
            project.config,
            "T-1",
            "BLOCKED",
            "WAITING_FOR_MERGE",
            reason="resume the interrupted archive owner",
        )
        self.assertEqual(resumed["archive_candidate"], task["archive_candidate"])
        result = runtime.enqueue_task(project.config, "merge", "T-1")

        self.assertEqual(result["status"], "NeedsRevalidation")
        self.assertEqual(result["reason"], "worktree-drift")
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "EXECUTING")
        merge_root = runtime.pool_root(project.config, "merge")
        self.assertEqual(list((merge_root / "queue").glob("*.json")), [])
        self.assertEqual(list((merge_root / "operations").glob("*.json")), [])

    def test_archive_revalidation_operation_recovers_stale_head_ticket(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        project.prepare_archive_task("T-2")
        merge_root = runtime.pool_root(project.config, "merge")
        owned_ticket = runtime.find_owned_record(
            runtime.list_records(merge_root / "queue"), "T-1"
        )
        self.assertIsNotNone(owned_ticket)
        reason = "Archive candidate requires revalidation: worktree-drift"
        runtime.atomic_write_json(
            runtime.archive_operation_path(merge_root, "T-1"),
            {
                "kind": "archive-revalidation",
                "project_id": project.config.project_id,
                "pool": "merge",
                "task_id": "T-1",
                "ticket_id": owned_ticket[1]["ticket_id"],
                "reason": reason,
                "started_at": runtime.utc_now(),
            },
        )
        runtime.transition_task(
            project.config,
            "T-1",
            "WAITING_FOR_MERGE",
            "EXECUTING",
            reason=reason,
        )

        acquired = runtime.try_acquire(project.config, "merge", "T-2")

        self.assertEqual(acquired["status"], "Acquired")
        self.assertEqual(acquired["lease"]["task_id"], "T-2")
        self.assertEqual(list((merge_root / "operations").glob("*.json")), [])
        self.assertIsNone(
            runtime.find_owned_record(runtime.list_records(merge_root / "queue"), "T-1")
        )

    def test_archive_acquire_operation_recovers_partial_lease_write(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        project.prepare_archive_task("T-2")
        merge_root = runtime.pool_root(project.config, "merge")
        owned_ticket = runtime.find_owned_record(
            runtime.list_records(merge_root / "queue"), "T-1"
        )
        self.assertIsNotNone(owned_ticket)
        lease_id = "b" * 32
        now = runtime.utc_now()
        lease = {
            "project_id": project.config.project_id,
            "pool": "merge",
            "task_id": "T-1",
            "lease_id": lease_id,
            "acquired_at": now,
            "heartbeat_at": now,
            "lease_timeout_seconds": 60,
            "host_lease_id": None,
        }
        runtime.atomic_write_json(
            runtime.archive_operation_path(merge_root, "T-1"),
            {
                "kind": "archive-acquire",
                "project_id": project.config.project_id,
                "pool": "merge",
                "task_id": "T-1",
                "ticket_id": owned_ticket[1]["ticket_id"],
                "lease": lease,
                "started_at": now,
            },
        )
        runtime.atomic_write_json(
            merge_root / "leases" / f"{lease_id}.json", lease
        )

        waiting = runtime.try_acquire(project.config, "merge", "T-2")

        self.assertEqual(waiting["status"], "Waiting")
        self.assertEqual(waiting["reason"], "project-capacity")
        task = runtime.load_task(project.config, "T-1")
        self.assertEqual(task["state"], "ARCHIVING")
        self.assertEqual(task["active_lease"], {"pool": "merge", "lease_id": lease_id})
        self.assertEqual(list((merge_root / "operations").glob("*.json")), [])
        self.assertTrue(runtime.try_acquire(project.config, "merge", "T-1")["idempotent"])

    def test_archive_acquire_operation_revalidates_drift_before_recovery(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        task = project.prepare_archive_task("T-1")
        merge_root = runtime.pool_root(project.config, "merge")
        owned_ticket = runtime.find_owned_record(
            runtime.list_records(merge_root / "queue"), "T-1"
        )
        self.assertIsNotNone(owned_ticket)
        lease_id = "e" * 32
        now = runtime.utc_now()
        lease = {
            "project_id": project.config.project_id,
            "pool": "merge",
            "task_id": "T-1",
            "lease_id": lease_id,
            "acquired_at": now,
            "heartbeat_at": now,
            "lease_timeout_seconds": 60,
            "host_lease_id": None,
        }
        runtime.atomic_write_json(
            runtime.archive_operation_path(merge_root, "T-1"),
            {
                "kind": "archive-acquire",
                "project_id": project.config.project_id,
                "pool": "merge",
                "task_id": "T-1",
                "ticket_id": owned_ticket[1]["ticket_id"],
                "lease": lease,
                "started_at": now,
            },
        )
        runtime.atomic_write_json(
            merge_root / "leases" / f"{lease_id}.json", lease
        )
        worktree = Path(task["repositories"][0]["worktree"])
        (worktree / "seed.txt").write_text(
            "drift after partial admission\n", encoding="utf-8"
        )

        result = runtime.try_acquire(project.config, "merge", "T-1")

        self.assertEqual(result["status"], "NeedsRevalidation")
        self.assertEqual(result["reason"], "worktree-drift")
        self.assertTrue(result["reconciled"])
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "EXECUTING")
        self.assertEqual(list((merge_root / "queue").glob("*.json")), [])
        self.assertEqual(list((merge_root / "leases").glob("*.json")), [])
        self.assertEqual(list((merge_root / "operations").glob("*.json")), [])

    def test_stale_partial_archive_lease_reclaims_without_recovery_hold(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        merge_root = runtime.pool_root(project.config, "merge")
        lease_id = "c" * 32
        runtime.atomic_write_json(
            merge_root / "leases" / f"{lease_id}.json",
            {
                "project_id": project.config.project_id,
                "pool": "merge",
                "task_id": "T-1",
                "lease_id": lease_id,
                "acquired_at": runtime.utc_now(),
                "heartbeat_at": (
                    datetime.now(timezone.utc) - timedelta(minutes=5)
                ).isoformat(),
                "lease_timeout_seconds": 60,
                "host_lease_id": None,
            },
        )

        reclaimed = runtime.reclaim_lease(
            project.config,
            "merge",
            "T-1",
            lease_id,
            "planner-thread",
            "recover partial archive admission",
        )
        repeated = runtime.reclaim_lease(
            project.config,
            "merge",
            "T-1",
            lease_id,
            "planner-thread",
            "recover partial archive admission",
        )

        self.assertTrue(reclaimed["orphan_admission"])
        self.assertIsNone(reclaimed["recovery_hold"])
        self.assertTrue(repeated["idempotent"])
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "WAITING_FOR_MERGE")
        self.assertEqual(runtime.try_acquire(project.config, "merge", "T-1")["status"], "Acquired")

    def test_legacy_archive_host_orphan_is_discoverable_and_reclaimable(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella",
            repository_ids=("service-a",),
            host_enabled=True,
        )
        project.prepare_archive_task("T-1")
        host_root = runtime.ensure_host_pool(project.config)
        lease_id = "d" * 32
        runtime.atomic_write_json(
            host_root / "leases" / f"{lease_id}.json",
            {
                "host_id": "local",
                "resource": "testers",
                "owner": runtime.legacy_host_lease_owner(project.config, "T-1"),
                "lease_id": lease_id,
                "acquired_at": runtime.utc_now(),
                "heartbeat_at": (
                    datetime.now(timezone.utc) - timedelta(minutes=5)
                ).isoformat(),
                "lease_timeout_seconds": 60,
            },
        )

        inspected = runtime.stale_leases(project.config, "merge")
        blocked = runtime.try_acquire(project.config, "merge", "T-1")

        self.assertEqual([item["lease_id"] for item in inspected["stale_host"]], [lease_id])
        self.assertEqual(blocked["status"], "Blocked")
        self.assertEqual(blocked["reason"], "legacy-host-orphan")
        reclaimed = runtime.reclaim_host_lease(
            project.config,
            "merge",
            "T-1",
            lease_id,
            "planner-thread",
            "remove pre-upgrade archive host orphan",
        )
        self.assertEqual(reclaimed["status"], "HostReclaimed")
        acquired = runtime.try_acquire(project.config, "merge", "T-1")
        self.assertEqual(acquired["status"], "Acquired")
        self.assertIsNone(acquired["lease"]["host_lease_id"])
        self.assertFalse((host_root / "leases" / f"{lease_id}.json").exists())

    def test_archive_acquire_rejects_worktree_drift_without_a_lease(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        task = project.prepare_archive_task("T-1")
        worktree = Path(task["repositories"][0]["worktree"])
        (worktree / "seed.txt").write_text("changed after test\n", encoding="utf-8")

        result = runtime.try_acquire(project.config, "merge", "T-1")

        self.assertEqual(result["status"], "NeedsRevalidation")
        self.assertEqual(result["reason"], "worktree-drift")
        task = runtime.load_task(project.config, "T-1")
        self.assertEqual(task["state"], "EXECUTING")
        self.assertNotIn("archive_candidate", task)
        merge_root = runtime.pool_root(project.config, "merge")
        self.assertEqual(list((merge_root / "queue").glob("*.json")), [])
        self.assertEqual(list((merge_root / "leases").glob("*.json")), [])

    def test_archive_acquire_rejects_base_drift_without_a_lease(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        repository = project.repository_roots["service-a"]
        (repository / "base.txt").write_text("advanced base\n", encoding="utf-8")
        run_fixture_git(repository, "add", "base.txt")
        run_fixture_git(
            repository,
            "-c",
            "user.name=Codex Tests",
            "-c",
            "user.email=codex-tests@example.invalid",
            "commit",
            "-q",
            "-m",
            "advance base",
        )

        result = runtime.try_acquire(project.config, "merge", "T-1")

        self.assertEqual(result["status"], "NeedsRevalidation")
        self.assertEqual(result["reason"], "base-drift")
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "EXECUTING")
        self.assertEqual(
            list((runtime.pool_root(project.config, "merge") / "leases").glob("*.json")),
            [],
        )

    def test_missing_archive_candidate_returns_upgraded_task_to_execution(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        path = runtime.task_path(project.config, "T-1")
        task = runtime.read_json(path)
        task.pop("archive_candidate")
        runtime.atomic_write_json(path, task)

        result = runtime.try_acquire(project.config, "merge", "T-1")

        self.assertEqual(result["status"], "NeedsRevalidation")
        self.assertEqual(result["reason"], "missing-archive-candidate")
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "EXECUTING")

    def test_stale_archive_recovery_holds_unrelated_queue_until_owner_completes(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella", repository_ids=("service-a",)
        )
        project.prepare_archive_task("T-1")
        project.prepare_archive_task("T-2")
        lease = runtime.try_acquire(project.config, "merge", "T-1")["lease"]
        lease_path = (
            runtime.pool_root(project.config, "merge")
            / "leases"
            / f"{lease['lease_id']}.json"
        )
        stale = runtime.read_json(lease_path)
        stale["heartbeat_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        ).isoformat()
        runtime.atomic_write_json(lease_path, stale)

        reclaimed = runtime.reclaim_lease(
            project.config,
            "merge",
            "T-1",
            lease["lease_id"],
            "planner-thread",
            "archive owner stopped",
        )
        self.assertEqual(reclaimed["recovery_hold"]["task_id"], "T-1")
        blocked = runtime.try_acquire(project.config, "merge", "T-2")
        self.assertEqual(blocked["status"], "Blocked")
        self.assertEqual(blocked["reason"], "archive-recovery")
        self.assertIsNone(runtime.project_status(project.config)["pools"]["merge"]["next_ready"])

        runtime.transition_task(
            project.config,
            "T-1",
            "BLOCKED",
            "WAITING_FOR_MERGE",
            reason="resume the interrupted archive owner",
        )
        runtime.enqueue_task(project.config, "merge", "T-1")
        recovery_lease = runtime.try_acquire(project.config, "merge", "T-1")["lease"]
        archive = project.evidence("archive-recovered-T-1", {"status": "Passed"})
        runtime.transition_task(
            project.config, "T-1", "ARCHIVING", "COMPLETED", str(archive)
        )
        released = runtime.release_lease(
            project.config, "merge", "T-1", recovery_lease["lease_id"]
        )
        self.assertIsNone(released["recovery_hold"])
        self.assertEqual(released["next_ready"]["task_id"], "T-2")

    def test_legacy_archive_host_lease_is_cleaned_on_release(self):
        project = MultiRepoProjectFixture(
            self.root / "umbrella",
            repository_ids=("service-a",),
            host_enabled=True,
        )
        project.prepare_archive_task("T-1")
        merge_lease = runtime.try_acquire(project.config, "merge", "T-1")["lease"]
        self.assertIsNone(merge_lease["host_lease_id"])
        legacy_host_id = "a" * 32
        host_root = runtime.ensure_host_pool(project.config)
        now = runtime.utc_now()
        runtime.atomic_write_json(
            host_root / "leases" / f"{legacy_host_id}.json",
            {
                "host_id": "local",
                "resource": "testers",
                "owner": "umbrella:T-1",
                "lease_id": legacy_host_id,
                "acquired_at": now,
                "heartbeat_at": now,
                "lease_timeout_seconds": 60,
            },
        )
        merge_path = (
            runtime.pool_root(project.config, "merge")
            / "leases"
            / f"{merge_lease['lease_id']}.json"
        )
        stored_merge = runtime.read_json(merge_path)
        stored_merge["host_lease_id"] = legacy_host_id
        runtime.atomic_write_json(merge_path, stored_merge)
        archive = project.evidence("archive-legacy-host", {"status": "Passed"})
        runtime.transition_task(
            project.config, "T-1", "ARCHIVING", "COMPLETED", str(archive)
        )

        runtime.release_lease(
            project.config, "merge", "T-1", merge_lease["lease_id"]
        )

        self.assertFalse((host_root / "leases" / f"{legacy_host_id}.json").exists())

    def test_success_path_reaches_serialized_archive(self):
        project = ProjectFixture(self.root / "project", "project")
        project.prepare_waiting_task("T-1")
        tester_lease = runtime.try_acquire(project.config, "tester", "T-1")[
            "lease"
        ]
        passed = project.evidence("test-passed", {"status": "Passed"})
        runtime.transition_task(
            project.config,
            "T-1",
            "TESTING",
            "TEST_PASSED",
            str(passed),
        )
        runtime.release_lease(
            project.config, "tester", "T-1", tester_lease["lease_id"]
        )
        runtime.transition_task(
            project.config, "T-1", "TEST_PASSED", "WAITING_FOR_MERGE"
        )
        runtime.enqueue_task(project.config, "merge", "T-1")
        merge_lease = runtime.try_acquire(project.config, "merge", "T-1")["lease"]
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "ARCHIVING")
        archive = project.evidence("archive", {"status": "Passed"})
        runtime.transition_task(
            project.config,
            "T-1",
            "ARCHIVING",
            "COMPLETED",
            str(archive),
        )
        runtime.release_lease(
            project.config, "merge", "T-1", merge_lease["lease_id"]
        )
        self.assertEqual(runtime.load_task(project.config, "T-1")["state"], "COMPLETED")

    def test_planner_replacement_requires_reason(self):
        project = ProjectFixture(self.root / "project", "project")
        runtime.register_planner(project.config, "thread-a", "local", False, None)
        with self.assertRaisesRegex(runtime.OrchestratorError, "already registered"):
            runtime.register_planner(project.config, "thread-b", "local", False, None)
        with self.assertRaisesRegex(runtime.OrchestratorError, "requires --reason"):
            runtime.register_planner(project.config, "thread-b", "local", True, None)
        replaced = runtime.register_planner(
            project.config, "thread-b", "local", True, "thread-a was archived"
        )
        self.assertEqual(replaced["thread_id"], "thread-b")

    def test_blocked_resume_requires_recorded_resolution(self):
        project = ProjectFixture(self.root / "project", "project")
        runtime.create_task(project.config, "T-1", str(project.plan_path))
        runtime.transition_task(
            project.config, "T-1", "PLANNED", "BLOCKED", reason="approval missing"
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "recorded resolution"):
            runtime.transition_task(project.config, "T-1", "BLOCKED", "PLANNED")
        resumed = runtime.transition_task(
            project.config,
            "T-1",
            "BLOCKED",
            "PLANNED",
            reason="approval recorded in the plan",
        )
        self.assertEqual(resumed["state"], "PLANNED")

    def test_worker_binding_is_owner_safe_and_idempotent(self):
        project = ProjectFixture(self.root / "project", "project")
        runtime.create_task(project.config, "T-1", str(project.plan_path))
        runtime.transition_task(project.config, "T-1", "PLANNED", "DISPATCHING")
        bound = runtime.bind_worker(
            project.config, "T-1", "worker-a", "local"
        )
        self.assertEqual(bound["state"], "EXECUTING")
        self.assertEqual(bound["worker"]["thread_id"], "worker-a")
        self.assertEqual(
            runtime.bind_worker(project.config, "T-1", "worker-a", "local")[
                "worker"
            ]["thread_id"],
            "worker-a",
        )
        with self.assertRaisesRegex(runtime.OrchestratorError, "already bound"):
            runtime.bind_worker(project.config, "T-1", "worker-b", "local")


if __name__ == "__main__":
    unittest.main()
