import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "m-continue"


class MContinueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.rules_text = (SKILL_ROOT / "references" / "continue.md").read_text(
            encoding="utf-8"
        )
        cls.manifest = json.loads(
            (REPO_ROOT / "manifests" / "m-continue.json").read_text(
                encoding="utf-8"
            )
        )

    def test_package_contains_required_files(self):
        required = (
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "references" / "continue.md",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_skill_routes_to_existing_phase_authorities(self):
        required_references = (
            "../m-execute/SKILL.md",
            "../m-execute/references/execution.md",
            "../m-test/SKILL.md",
            "../m-test/references/testing.md",
            "../m-autoflow/references/subagents.md",
            "../m-autoflow/references/output-components.md",
        )
        for reference in required_references:
            with self.subTest(reference=reference):
                self.assertIn(f"`{reference}`", self.skill_text)
                self.assertTrue((SKILL_ROOT / reference).resolve().is_file())

    def test_manifest_declares_phase_dependencies_and_reference(self):
        self.assertEqual(self.manifest["name"], "m-continue")
        self.assertEqual(
            set(self.manifest["depends_on_skills"]),
            {"m-autoflow", "m-execute", "m-test"},
        )
        self.assertEqual(
            self.manifest["reference_files"], ["references/continue.md"]
        )

    def test_invocation_authorizes_unattended_in_scope_loop(self):
        required_contracts = (
            "authorizes the whole in-scope convergence loop",
            "not a reason to ask the user whether to continue",
            "silence never requires another confirmation",
            "Do not ask whether to continue between phases",
        )
        combined = self.skill_text + self.rules_text
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, combined)

    def test_non_progress_requires_same_signature_and_no_improvement(self):
        required_contracts = (
            "same normalized failure signature",
            "no measurable Task, diff, validation, or evidence improvement",
            "three consecutive complete cycles",
            "Any measurable improvement resets",
            "Do not impose a separate small total-iteration limit",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, self.rules_text)

    def test_terminal_boundaries_preserve_scope_and_archive_ownership(self):
        required_contracts = (
            "new or changed requirement, architecture decision, Task ID, or write set",
            "Do not label ordinary test failure",
            "Do not invoke archive automatically",
            "Do not create `docs/change`",
        )
        combined = self.skill_text + self.rules_text
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, combined)


if __name__ == "__main__":
    unittest.main()
