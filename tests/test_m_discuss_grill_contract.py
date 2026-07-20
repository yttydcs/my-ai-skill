import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "m-discuss"


class MDiscussGrillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.discussion_text = (
            SKILL_ROOT / "references" / "discussion.md"
        ).read_text(encoding="utf-8")
        cls.grilling_text = (
            SKILL_ROOT / "references" / "grilling.md"
        ).read_text(encoding="utf-8")
        cls.manifest = json.loads(
            (REPO_ROOT / "manifests" / "m-discuss.json").read_text(
                encoding="utf-8"
            )
        )
        cls.feature_text = (
            REPO_ROOT / "docs" / "features" / "m-autoflow-workflow.md"
        ).read_text(encoding="utf-8")
        cls.requirements_text = (
            REPO_ROOT / "docs" / "requirements" / "m-autoflow-skill.md"
        ).read_text(encoding="utf-8")
        cls.spec_text = (
            REPO_ROOT / "docs" / "specs" / "m-autoflow-skill.md"
        ).read_text(encoding="utf-8")

    def test_package_contains_grilling_reference(self):
        required = (
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "references" / "discussion.md",
            SKILL_ROOT / "references" / "grilling.md",
            SKILL_ROOT / "references" / "research.md",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_manifest_packages_grilling_without_external_dependency(self):
        self.assertEqual(self.manifest["name"], "m-discuss")
        self.assertEqual(self.manifest["version"], "0.2.0")
        self.assertEqual(
            self.manifest["depends_on_skills"], ["m-autoflow", "m-docs"]
        )
        self.assertEqual(
            self.manifest["reference_files"],
            [
                "references/discussion.md",
                "references/grilling.md",
                "references/research.md",
            ],
        )

    def test_grill_mode_is_explicit_and_conditional(self):
        required_contracts = (
            "Read `references/grilling.md` only when the user explicitly asks",
            "Do not enter Grill Mode merely because a request is vague",
            "Otherwise keep the standard discussion flow",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, self.skill_text)

    def test_decision_snapshot_separates_facts_and_judgment(self):
        required_contracts = (
            "confirmed decisions",
            "rejected alternatives",
            "deferred decisions and their consequences",
            "open decisions",
            "Look up discoverable facts",
            "Ask the user only for judgment calls",
            "Never turn a recommendation, silence, ambiguity, or an inferred preference into a confirmed decision",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, self.grilling_text)

    def test_interview_is_depth_first_and_one_question_per_turn(self):
        required_contracts = (
            "Resolve parent decisions before dependent child branches",
            "Ask exactly one judgment question per turn",
            "Include one recommended answer and a concise rationale",
            "Wait for the user's answer before asking another question",
            "Do not bundle related questions, alternatives, or follow-ups",
            "Continue depth-first",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, self.grilling_text)

    def test_wrap_up_and_completion_preserve_phase_gates(self):
        required_contracts = (
            "Do not impose a fixed numeric question limit",
            "confirm explicitly that shared understanding has been reached",
            "Do not treat the absence of more questions as confirmation",
            "If the user asks to stop or wrap up early",
            "do not claim the workflow is ready for `$m-plan`",
            "Do not enter `$m-plan`, implement code",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, self.grilling_text)

    def test_standard_discussion_brief_remains_authoritative(self):
        required_contracts = (
            "The interview feeds this reference's required discussion brief rather than replacing it",
            "Blocking open decisions prevent the `$m-plan` handoff",
            "Grill Mode does not replace this exit gate",
        )
        combined = self.skill_text + self.discussion_text
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, combined)

    def test_stable_docs_describe_the_conditional_mode(self):
        self.assertIn("### Explicit Grill Mode", self.feature_text)
        self.assertIn("explicit Grill Mode", self.requirements_text)
        self.assertIn("`references/grilling.md`", self.spec_text)
        for text in (
            self.feature_text,
            self.requirements_text,
            self.spec_text,
        ):
            with self.subTest(document=text[:40]):
                self.assertIn("2026-07-20_m-discuss-grill-mode.md", text)


if __name__ == "__main__":
    unittest.main()
