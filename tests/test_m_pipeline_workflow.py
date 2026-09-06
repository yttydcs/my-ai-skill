from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "m-pipeline"))
from support import Fixture, git
from pipeline_lib.config import PipelineError


class WorkflowTests(Fixture):
    def test_project_creation_checks_membership_before_binding_and_preserves_pending(self):
        target = {"type": "project", "projectId": "saved-project", "base_ref": "main"}
        self.config["roles"]["executor"]["create"] = {"target": target}
        self.start(bind=False)
        setup = {"roles": ["executor"], "source_ref": "fixture:user-create-team", "creation_limit": 8}
        creation = self.call("bootstrap", setup)
        self.assertEqual(creation["target"], target)
        self.call("operation_result", {"operation_id": creation["operation_id"], "outcome": "pending",
                                       "client_thread_id": "pending-project", "observation_ref": "fake-host:queued"})
        receipt = {"operation_id": creation["operation_id"], "outcome": "ready", "session": self.worker,
                   "cwd": str(self.repo), "observation_ref": "fake-host:task-metadata"}
        for extra in ({}, {"project_id": "wrong-project"}):
            with self.subTest(extra=extra):
                with self.assertRaises(PipelineError) as failure:
                    self.call("operation_result", {**receipt, **extra})
                self.assertEqual(failure.exception.code, "project_mismatch")
                self.assertFalse(self.call("status")["bindings"])
                self.assertEqual(self.call("bootstrap", setup)["action"], "wait")
                self.assertEqual(self.call("status")["created"], 1)
        receipt["project_id"] = "saved-project"
        self.call("operation_result", receipt)
        self.assertTrue(self.call("operation_result", receipt)["duplicate"])
        self.assertEqual(self.call("bootstrap", setup)["action"], "ready")
        with self.assertRaisesRegex(PipelineError, "Conflicting duplicate"):
            self.call("operation_result", {**receipt, "project_id": "wrong-project"})

    def test_on_demand_local_project_creation_keeps_target_and_assignment_worktree(self):
        target = {"type": "project", "projectId": "saved-umbrella", "environment": "local"}
        self.config["roles"]["executor"]["create"] = {"target": target}
        self.start(bind=False)
        packet = self.packet()
        self.admit([packet])
        creation = self.call("next")
        self.assertEqual(creation["target"], target)
        self.call("operation_result", {"operation_id": creation["operation_id"], "outcome": "ready",
                                       "session": self.worker, "cwd": str(self.root), "project_id": "saved-umbrella",
                                       "observation_ref": "fake-host:project-metadata"})
        self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:ready"})
        dispatch = self.call("next")
        self.assertEqual(dispatch["action"], "dispatch")
        self.assertEqual(dispatch["envelope"]["packet"]["repositories"], packet["repositories"])

    def test_pass_requires_inactive_receiver_exact_tasks_and_evidence(self):
        self.start()
        self.admit([self.packet()])
        dispatch = self.call("next")
        self.delivered(dispatch)
        result = self.result(dispatch)
        self.call("observe", {"session": self.worker, "status": "active", "observation_ref": "fake-host:running"})
        with self.assertRaisesRegex(PipelineError, "receiver stopped"):
            self.call("result", result)
        self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:done"})
        result["task_ids"] = ["OTHER"]
        with self.assertRaisesRegex(PipelineError, "Task IDs"):
            self.call("result", result)
        result["task_ids"] = ["A"]
        self.call("result", result)
        self.assertTrue(self.call("result", result)["duplicate"])
        self.assertEqual(self.call("finish")["status"], "complete")

    def test_result_before_delivery_ack_cannot_be_reversed_by_late_ack(self):
        self.start()
        self.admit([self.packet()])
        dispatch = self.call("next")
        self.call("result", self.result(dispatch))
        self.delivered(dispatch)
        self.assertEqual(self.call("status")["jobs"]["job-a"]["status"], "passed")

    def test_manual_takeover_keeps_worktree_claim_and_resume_does_not_replay(self):
        self.start()
        self.admit([self.packet()])
        dispatch = self.call("next")
        self.delivered(dispatch)
        self.call("pause")
        with self.assertRaises(PipelineError):
            self.call("next")
        with self.assertRaisesRegex(PipelineError, "inactive"):
            self.call("takeover", {"job_id": "job-a", "observation_ref": "fake-host:stale-idle"})
        self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:stopped"})
        self.call("takeover", {"job_id": "job-a", "observation_ref": "fake-host:inactive-manual-handoff"})
        claims = self.call("status")["claims"]
        self.assertTrue(any(c["resource"].startswith("worktree:") for c in claims))
        self.assertFalse(any(c["resource"].startswith("session:") for c in claims))
        with self.assertRaisesRegex(PipelineError, "manual"):
            self.call("resume")
        self.call("result", self.result(dispatch))
        self.call("resume")
        self.assertEqual(self.call("next")["action"], "wait")
        self.call("finish")

    def test_bootstrap_pending_creation_is_not_duplicated_and_needs_real_id(self):
        self.config["roles"]["executor"]["create"] = {"target": {"type": "projectless", "directoryName": "fixture"}}
        self.start(bind=False)
        setup = {"roles": ["executor"], "source_ref": "fixture:user-create-team", "creation_limit": 8}
        creation = self.call("bootstrap", setup)
        self.call("operation_result", {"operation_id": creation["operation_id"], "outcome": "pending",
                                       "client_thread_id": "pending-fixture", "observation_ref": "fake-host:queued"})
        self.assertEqual(self.call("bootstrap", setup)["action"], "wait")
        with self.assertRaisesRegex(PipelineError, "real session"):
            self.call("operation_result", {"operation_id": creation["operation_id"], "outcome": "ready", "observation_ref": "fake-host:ready"})
        fresh = {"host_id": "local", "thread_id": "fresh-fixture"}
        self.call("operation_result", {"operation_id": creation["operation_id"], "outcome": "ready", "session": fresh,
                                       "cwd": str(self.root), "observation_ref": "fake-host:ready"})
        self.assertEqual(self.call("bootstrap", setup)["action"], "ready")
        self.assertEqual(self.call("status")["created"], 1)

    def test_busy_wait_and_bounded_fresh_replacement(self):
        self.config["limits"]["reuse_after"] = 1
        self.config["roles"]["executor"]["create"] = {"target": {"type": "projectless", "directoryName": "fixture"}}
        self.start()
        self.admit([self.packet("a"), self.packet("b", task="B")])
        first = self.call("next")
        second = self.call("next")
        self.assertEqual(second["action"], "create")
        self.assertEqual(self.call("next")["action"], "wait")
        self.call("result", self.result(first))
        fresh = {"host_id": "local", "thread_id": "fresh-worker"}
        self.call("operation_result", {"operation_id": second["operation_id"], "outcome": "ready", "session": fresh,
                                       "cwd": str(self.root), "observation_ref": "fake-host:ready"})
        self.call("observe", {"session": fresh, "status": "idle", "observation_ref": "fake-host:bootstrap-complete"})
        following = self.call("next")
        self.assertEqual(following["envelope"]["receiver"], "local:fresh-worker")
        self.assertEqual(following["envelope"]["packet"]["task_ids"], ["B"])

    def test_fanout_conflicts_and_unsealed_late_work_fail(self):
        self.start()
        first, second = self.packet("a"), self.packet("b", task="B", writes="a.txt")
        with self.assertRaisesRegex(PipelineError, "overlap"):
            self.admit([first, second])
        second["write_set"][0]["path"] = "b.txt"
        self.admit([first, second])
        with self.assertRaisesRegex(PipelineError, "sealed"):
            self.admit([self.packet("late", task="C")])

    def test_distinct_branch_results_need_explicit_integration_before_test(self):
        self.config["roles"]["tester"] = {"skill": "m-test", "contexts": [], "sessions": [], "create": None}
        self.config["stages"].append({"id": "test", "role": "tester", "after": ["execute"], "routing": "join"})
        self.start()
        first, second = self.packet("a"), self.packet("b", task="B")
        self.admit([first, second])
        for packet in (first, second):
            dispatch = self.call("next")
            tree = Path(packet["repositories"]["code"]["worktree"])
            (tree / packet["write_set"][0]["path"]).write_text(packet["id"], encoding="utf-8")
            git(tree, "add", ".")
            git(tree, "commit", "-m", "fixture: separate branch output")
            packet["repositories"]["code"]["commit"] = git(tree, "rev-parse", "HEAD")
            self.call("result", self.result(dispatch, packet=packet))
        self.admit([self.packet("test", stage="test")])
        with self.assertRaisesRegex(PipelineError, "integration"):
            self.call("next")

    def test_one_level_group_waits_for_all_children(self):
        self.start()
        parent = self.packet("group")
        parent.update(kind="group", task_ids=["A", "B"], requires=["a", "b"], write_set=[])
        first, second = self.packet("a"), self.packet("b", task="B")
        first["parent"] = second["parent"] = "group"
        self.admit([parent, first, second])
        self.call("result", self.result(self.call("next")))
        self.assertEqual(self.call("status")["jobs"]["group"]["status"], "pending")
        with self.assertRaisesRegex(PipelineError, "incomplete"):
            self.call("finish")
        self.call("result", self.result(self.call("next")))
        self.call("next")
        self.call("finish")

    def test_nonprogress_bound_and_stale_result_cannot_repeat_work(self):
        self.start()
        packet = self.packet()
        self.admit([packet])
        first_result = None
        for attempt in range(3):
            dispatch = self.call("next")
            failed = self.result(dispatch, "failed")
            first_result = first_result or failed
            self.call("result", failed)
            if attempt < 2:
                self.call("retry", {"job_id": "job-a", "repositories": packet["repositories"], "plans": packet["plans"], "review_ref": "fixture:repair"})
                self.call("result", first_result)
                self.assertEqual(self.call("status")["jobs"]["job-a"]["status"], "pending")
        with self.assertRaisesRegex(PipelineError, "Non-progress"):
            self.call("retry", {"job_id": "job-a", "repositories": packet["repositories"], "plans": packet["plans"], "review_ref": "fixture:repair"})

    def test_known_nondelivery_releases_but_ambiguous_delivery_cannot_retry(self):
        self.start()
        self.admit([self.packet()])
        first = self.call("next")
        self.call("operation_result", {"operation_id": first["operation_id"], "outcome": "not_delivered", "observation_ref": "fake-host:rejected-before-send"})
        self.assertEqual(self.call("next")["action"], "wait")
        self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:rechecked-idle"})
        second = self.call("next")
        self.assertNotEqual(first["operation_id"], second["operation_id"])
        self.call("operation_result", {"operation_id": second["operation_id"], "outcome": "uncertain", "observation_ref": "fake-host:timeout"})
        with self.assertRaisesRegex(PipelineError, "ambiguous"):
            self.call("operation_result", {"operation_id": second["operation_id"], "outcome": "not_delivered", "observation_ref": "fake-host:guess"})
