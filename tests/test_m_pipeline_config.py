from pathlib import Path
import json
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "m-pipeline"))
from support import Fixture, proof, save
from pipeline_lib.config import PipelineError, artifact, load_json, plan_ref, snapshot, validate_blueprint


class ConfigurationTests(Fixture):
    def test_project_creation_environments_and_legacy_target(self):
        targets = (
            {"type": "project", "projectId": "saved-project", "base_ref": "main"},
            {"type": "project", "projectId": "saved-project", "environment": "worktree", "base_ref": "main"},
            {"type": "project", "projectId": "saved-umbrella", "environment": "local"},
            {"type": "projectless", "directoryName": "explicit-standalone"},
        )
        for target in targets:
            with self.subTest(target=target):
                self.config["roles"]["executor"]["create"] = {"target": target}
                validated = validate_blueprint(self.config, self.root)
                self.assertEqual(validated["roles"]["executor"]["create"]["target"], target)

    def test_unresolved_project_and_inconsistent_environment_rejected(self):
        targets = (
            {"type": "project", "projectId": "<verified-project-id>", "base_ref": "main"},
            {"type": "project", "projectId": "saved-project"},
            {"type": "project", "projectId": "saved-project", "environment": "local", "base_ref": "main"},
            {"type": "project", "projectId": "saved-project", "environment": "cloud", "base_ref": "main"},
        )
        for target in targets:
            with self.subTest(target=target):
                self.config["roles"]["executor"]["create"] = {"target": target}
                with self.assertRaises(PipelineError):
                    validate_blueprint(self.config, self.root)

    def test_relative_paths_and_unicode_project(self):
        self.config["project_root"] = "project"
        self.config["docs_root"] = "docs"
        actual = validate_blueprint(self.config, self.root)
        self.assertEqual(actual["project_root"], str(self.repo))
        tree = self.tree("unicode-测试")
        self.assertEqual(snapshot(actual, {"code": {"worktree": str(tree), "commit": self.commit}})["code"]["worktree"], str(tree))

    def test_unknown_fields_limits_and_graph_fail_explicitly(self):
        for edit in (lambda c: c.update(unknown=True),
                     lambda c: c["limits"].update(max_depth=2),
                     lambda c: c["stages"][0].update(after=["missing"]),
                     lambda c: c["roles"]["executor"]["contexts"].append({"scope": "auto", "name": "name"})):
            config = json.loads(json.dumps(self.config))
            edit(config)
            with self.assertRaises(PipelineError):
                validate_blueprint(config, self.root)

    def test_duplicate_json_keys_and_context_artifacts_rejected(self):
        path = self.root / "duplicate.json"
        path.write_text('{"value":1,"value":2}', encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Duplicate"):
            load_json(path)
        context = self.docs / "context"
        context.mkdir()
        secret = context / "private.md"
        secret.write_text("fixture value, never persist", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Context bodies"):
            artifact(proof(secret), [self.docs])

    def test_plan_progress_does_not_invalidate_definition(self):
        tree = self.tree("definitions")
        ref = plan_ref({"path": str(tree / "plan.md"), "sections": ["Scope", "Task A"]}, tree)
        path = tree / "plan.md"
        path.write_text(self.plan_text.replace("[ ]", "[x]").replace("Pending.", "Validated."), encoding="utf-8")
        self.assertEqual(plan_ref(ref, tree), ref)
        path.write_text(path.read_text(encoding="utf-8").replace("Write a.txt", "Delete a.txt"), encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Plan definition changed"):
            plan_ref(ref, tree)

    def test_candidate_dirty_wrong_repository_and_symlink_escape(self):
        config = validate_blueprint(self.config, self.root)
        tree = self.tree("candidate")
        (tree / "a.txt").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "checkpoint"):
            snapshot(config, {"code": {"worktree": str(tree), "commit": self.commit}})
        with self.assertRaisesRegex(PipelineError, "dedicated"):
            snapshot(config, {"code": {"worktree": str(self.repo), "commit": self.commit}})
        outside = self.root / "outside"
        outside.mkdir()
        link = self.worktrees / "escape"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc.winerror if hasattr(exc, 'winerror') else exc.errno}")
        with self.assertRaisesRegex(PipelineError, "dedicated"):
            snapshot(config, {"code": {"worktree": str(link), "commit": self.commit}})
