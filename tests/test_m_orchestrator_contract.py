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
            "Any implementation or plan edit in any participating repository",
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
            "canonical project root plus `project_id`",
            "Git-common-directory isolation for schema version 1 compatibility",
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

    def test_archive_contract_is_project_scoped_retryable_and_revalidated(self):
        archive_skill = (
            REPO_ROOT / "skills" / "m-archive" / "SKILL.md"
        ).read_text(encoding="utf-8")
        required = (
            (self.skill_text, "Independent projects may archive concurrently"),
            (self.skill_text, "never introduce a machine-wide archive lock"),
            (self.skill_text, "Ordinary contention remains `WAITING_FOR_MERGE`"),
            (self.references["worker.md"], "`NeedsRevalidation` returns the Task to `EXECUTING`"),
            (self.references["testing-pool.md"], "return `next_ready`"),
            (self.references["configuration.md"], "never acquired for the archive/integration pool"),
            (archive_skill, "active project integration lease"),
            (archive_skill, "Standalone `$m-archive` behavior is unchanged"),
        )
        for source, text in required:
            with self.subTest(text=text):
                self.assertIn(text, source)

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
            REPO_ROOT / "docs" / "decisions" / "2026-08-04_orchestrator-multi-repo-runtime.md",
            REPO_ROOT / "docs" / "decisions" / "2026-08-15_project-scoped-archive-resume.md",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_schema_v2_and_multi_repository_dispatch_are_explicit(self):
        configuration = self.references["configuration.md"]
        planner = self.references["planner.md"]
        worker = self.references["worker.md"]
        required = (
            (configuration, "Schema version 2 treats `project_root` as an umbrella directory"),
            (configuration, "explicit repository catalog"),
            (configuration, "never recommend initializing an umbrella root"),
            (planner, "pass the complete absolute worktree map"),
            (worker, "composite change identifier"),
            (worker, "never claim cross-repository atomicity"),
        )
        for source, text in required:
            with self.subTest(text=text):
                self.assertIn(text, source)

        example = (SKILL_ROOT / "assets" / "m-orchestrator.example.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn("schema_version = 2", example)
        self.assertGreaterEqual(example.count("[[repositories]]"), 2)

    def test_phase_references_preserve_multi_repository_worktree_set(self):
        required = {
            "m-execute/references/execution.md": "exact per-repository worktree set",
            "m-test/references/testing.md": "complete persisted worktree set",
            "m-continue/references/continue.md": "every active repository worktree",
            "m-archive/references/archive.md": "do not describe independent Git merges as atomic",
        }
        for relative, text in required.items():
            source = (REPO_ROOT / "skills" / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative):
                self.assertIn(text, source)


if __name__ == "__main__":
    unittest.main()
