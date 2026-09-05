from pathlib import Path
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "m-pipeline"))
from support import Fixture, SCRIPTS, save
from pipeline_lib.config import PipelineError
from pipeline_lib.store import Store
from pipeline_lib.workflow import Engine


class StoreTests(Fixture):
    def test_independent_processes_cannot_claim_shared_receiver(self):
        self.start()
        self.start("run-two")
        self.admit([self.packet("one")])
        self.admit([self.packet("two")], "run-two")
        processes = []
        for run in (self.run_id, "run-two"):
            path = save(self.root / (run + "-next.json"), self.request("next", run_id=run))
            processes.append(subprocess.Popen([sys.executable, str(SCRIPTS / "pipeline_runtime.py"), "apply", "--input", path,
                                               "--state-root", str(self.root / "state")], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        outputs = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, stderr.decode())
            outputs.append(json.loads(stdout.decode("utf-8"))["result"]["action"])
        self.assertCountEqual(outputs, ["dispatch", "wait"])

    def test_all_resource_claims_rollback_when_one_is_busy(self):
        with self.store.transaction() as db:
            self.assertTrue(Store.claim(db, ["busy"], "other", "job"))
            self.assertFalse(Store.claim(db, ["available", "busy"], "mine", "job"))
            self.assertIsNone(db.execute("SELECT 1 FROM claims WHERE resource='available'").fetchone())
        with self.assertRaises(RuntimeError):
            with self.store.transaction() as db:
                self.assertTrue(Store.claim(db, ["temporary"], "mine", "job"))
                raise RuntimeError("simulated process boundary failure")
        with self.store.transaction() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM claims WHERE resource='temporary'").fetchone())

    def test_restart_and_idle_observation_do_not_release_uncertain_claim(self):
        self.start()
        self.admit([self.packet()])
        dispatch = self.call("next")
        self.call("operation_result", {"operation_id": dispatch["operation_id"], "outcome": "uncertain", "observation_ref": "fake-host:timeout"})
        self.engine = Engine(Store(self.root / "state"))
        self.call("observe", {"session": self.worker, "status": "idle", "observation_ref": "fake-host:turn-ended"})
        status = self.call("status")
        self.assertTrue(status["claims"])
        self.assertEqual(self.call("next")["action"], "wait")
        with self.assertRaisesRegex(PipelineError, "Reconcile"):
            self.call("resume")

    def test_schema_version_and_wrong_coordinator_fail(self):
        self.start()
        request = self.request("pause")
        request["actor"] = self.worker
        with self.assertRaisesRegex(PipelineError, "coordinator"):
            self.engine.apply(request)
        with self.store.transaction() as db:
            db.execute("PRAGMA user_version=999")
        with self.assertRaisesRegex(PipelineError, "version"):
            Store(self.root / "state")
