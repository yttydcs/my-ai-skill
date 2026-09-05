from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "m-pipeline"))
from support import Fixture, REPO_ROOT, SCRIPTS, git, proof, save
from pipeline_lib.config import PipelineError, plan_ref, validate_blueprint


class ContractTests(Fixture):
    def test_cli_reports_invalid_input_without_mutating_a_run(self):
        request = save(self.root / "bad.json", {"action": "unknown", "secret": "fixture-value"})
        result = subprocess.run([sys.executable, str(SCRIPTS / "pipeline_runtime.py"), "apply", "--input", request,
                                 "--state-root", str(self.root / "cli-state")], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["ok"])
        self.assertNotIn("fixture-value", result.stdout)

    def test_manifest_entries_and_example_validate_without_old_package_changes(self):
        manifest = json.loads((REPO_ROOT / "manifests/m-pipeline.json").read_text(encoding="utf-8"))
        package = REPO_ROOT / manifest["source_dir"]
        for relative in manifest["reference_files"] + manifest["script_files"]:
            self.assertTrue((package / relative).is_file(), relative)
        for name in manifest["depends_on_skills"]:
            self.assertTrue((REPO_ROOT / "skills" / name / "SKILL.md").is_file())
        example = json.loads((package / "assets/pipeline.example.json").read_text(encoding="utf-8"))
        example.update(project_root=str(self.repo), docs_root=str(self.docs), repositories=self.config["repositories"])
        validate_blueprint(example, self.root)

    def test_missing_required_context_blocks_phase_and_no_body_is_persisted(self):
        self.config["roles"]["executor"]["contexts"] = [{"scope": "local", "name": "missing"}]
        self.start()
        self.admit([self.packet()])
        dispatch = self.call("next")
        loader = REPO_ROOT / "skills/m-context/scripts/context_loader.py"
        response = subprocess.run([sys.executable, str(loader), "load", "missing", "--scope", "local", "--docs-root", str(self.docs)],
                                  capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(response.returncode, 2)
        self.call("result", self.result(dispatch, "blocked"))
        self.assertEqual(self.call("status")["status"], "needs_input")
        with self.assertRaises(PipelineError):
            self.call("next")
        data, _ = self.store.read(self.run_id)
        self.assertEqual(data["config"]["roles"]["executor"]["contexts"], [{"scope": "local", "name": "missing"}])

    def test_expanded_write_scope_is_rejected(self):
        self.start()
        with self.store.transaction() as db:
            data, revision = self.store.read(self.run_id)
            data["authority"]["write_scope"] = {"code": ["src"]}
            db.execute("UPDATE runs SET data=? WHERE id=?", (json.dumps(data), self.run_id))
        with self.assertRaisesRegex(PipelineError, "Write scope"):
            self.admit([self.packet()])

    def test_unauthorized_release_environment_is_rejected(self):
        procedure = self.docs / "release.md"
        procedure.write_text("Write a local fixture marker only.", encoding="utf-8")
        self.config["roles"]["release"] = {"skill": "release", "contexts": [], "sessions": [], "create": None,
                                            "environment": "production", "procedure_ref": proof(procedure)}
        self.config["stages"].append({"id": "release", "role": "release", "after": ["execute"], "routing": "any"})
        self.start()
        with self.assertRaisesRegex(PipelineError, "environment"):
            self.admit([self.packet("release", stage="release")])

    def test_composite_cannot_get_duplicate_outer_test_loop(self):
        self.config["roles"]["executor"]["skill"] = "m-go"
        self.config["roles"]["tester"] = {"skill": "m-test", "contexts": [], "sessions": [], "create": None}
        self.config["stages"].append({"id": "test", "role": "tester", "after": ["execute"], "routing": "join"})
        with self.assertRaisesRegex(PipelineError, "Composite owns"):
            validate_blueprint(self.config, self.root)

    def test_non_git_umbrella_retains_two_repository_identities(self):
        second = self.root / "second"
        git(self.root, "clone", str(self.repo), str(second))
        self.config["project_root"] = str(self.root / "umbrella")
        Path(self.config["project_root"]).mkdir()
        self.config["repositories"]["second"] = {"path": str(second), "base_ref": "main", "worktree_root": str(self.worktrees / "second")}
        self.start()
        packet = self.packet()
        second_tree = self.worktrees / "second" / "task"
        git(second, "worktree", "add", "-b", "fixture-second", str(second_tree), "main")
        packet["repositories"]["second"] = {"worktree": str(second_tree), "commit": git(second_tree, "rev-parse", "HEAD")}
        packet["plans"]["second"] = plan_ref({"path": str(second_tree / "plan.md"), "sections": ["Scope", "Task B"]}, second_tree)
        self.admit([packet])
        dispatch = self.call("next")
        self.assertEqual(set(dispatch["envelope"]["packet"]["repositories"]), {"code", "second"})
        incomplete = self.result(dispatch)
        del incomplete["repositories"]["second"]
        with self.assertRaisesRegex(PipelineError, "omits"):
            self.call("result", incomplete)
