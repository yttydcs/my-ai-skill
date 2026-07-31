from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
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
            ["git", "init", "-q", str(root)],
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
