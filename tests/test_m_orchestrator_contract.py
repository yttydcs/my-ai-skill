import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "m-orchestrator"


class MOrchestratorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.references = {
            path.name: path.read_text(encoding="utf-8")
            for path in (SKILL_ROOT / "references").glob("*.md")
        }
        cls.all_text = cls.skill_text + "\n" + "\n".join(cls.references.values())
        cls.manifest = json.loads(
            (REPO_ROOT / "manifests" / "m-orchestrator.json").read_text(
                encoding="utf-8"
            )
        )

    def test_package_contains_declared_files(self):
        required = (
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "assets" / "m-orchestrator.example.toml",
            SKILL_ROOT / "scripts" / "orchestrator_runtime.py",
            *(SKILL_ROOT / path for path in self.manifest["reference_files"]),
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_manifest_declares_existing_phase_authorities(self):
        self.assertEqual(self.manifest["name"], "m-orchestrator")
        self.assertEqual(
            set(self.manifest["depends_on_skills"]),
            {
                "m-autoflow",
                "m-context",
                "m-discuss",
                "m-plan",
                "m-execute",
                "m-test",
                "m-archive",
            },
        )
        self.assertEqual(
            self.manifest["script_files"], ["scripts/orchestrator_runtime.py"]
        )

    def test_skill_routes_without_replacing_phase_ownership(self):
        required = (
            "does not replace their phase behavior",
            "invoke `$m-execute`",
            "invoke `$m-test`",
            "Invoke `$m-archive`",
            "Keep `$m-go` available",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.all_text)

    def test_worker_gate_precedes_tester_admission(self):
        required = (
            "Do not enqueue, reserve, or create a Tester until every applicable check passes",
            "Any implementation edit after gate creation invalidates that gate",
            "Release project and host permits before repair",
            "rerun the complete gate",
        )
        worker = self.references["worker.md"]
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, worker)

    def test_project_context_and_isolation_are_explicit(self):
        required = (
            "explicit `local:<name>`",
            "cannot silently select unrelated global data",
            "repository common Git directory and `project_id`",
            "contains only numeric capacity",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.all_text)

    def test_pool_contract_preserves_capacity_and_ownership(self):
        required = (
            "Only the head eligible Task may acquire",
            "Wrong-owner operations fail",
            "explicit reclaim",
            "release the host lease",
        )
        pool = self.references["testing-pool.md"]
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, pool)

    def test_autoflow_routes_orchestrator_as_non_phase_companion(self):
        umbrella = (REPO_ROOT / "skills" / "m-autoflow" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        stages = (
            REPO_ROOT / "skills" / "m-autoflow" / "references" / "stages.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`$m-orchestrator`", umbrella)
        self.assertIn("project-level companion above separate task workflows", stages)
        self.assertIn("does not become a stage", stages)

    def test_stable_docs_chain_exists(self):
        required = (
            REPO_ROOT / "docs" / "features" / "m-project-orchestrator.md",
            REPO_ROOT / "docs" / "requirements" / "m-project-orchestrator.md",
            REPO_ROOT / "docs" / "specs" / "m-project-orchestrator.md",
            REPO_ROOT / "docs" / "decisions" / "2026-07-31_project-orchestrator.md",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
