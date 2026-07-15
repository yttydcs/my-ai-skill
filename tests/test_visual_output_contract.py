from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"

WORKFLOW_SKILLS = {
    "m-autoflow": "references/output-components.md",
    "m-context": "../m-autoflow/references/output-components.md",
    "m-discuss": "../m-autoflow/references/output-components.md",
    "m-plan": "../m-autoflow/references/output-components.md",
    "m-execute": "../m-autoflow/references/output-components.md",
    "m-go": "../m-autoflow/references/output-components.md",
    "m-quick": "../m-autoflow/references/output-components.md",
    "m-test": "../m-autoflow/references/output-components.md",
    "m-archive": "../m-autoflow/references/output-components.md",
    "m-docs": "../m-autoflow/references/output-components.md",
    "m-gitpush": "../m-autoflow/references/output-components.md",
}


class VisualOutputContractTests(unittest.TestCase):
    def test_every_workflow_skill_routes_to_shared_output_reference(self):
        for skill_name, reference in WORKFLOW_SKILLS.items():
            with self.subTest(skill=skill_name):
                skill_dir = SKILLS_ROOT / skill_name
                skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"`{reference}`", skill_text)
                self.assertTrue((skill_dir / reference).resolve().is_file())

    def test_shared_reference_covers_supported_components_and_safety(self):
        reference = (
            SKILLS_ROOT / "m-autoflow" / "references" / "output-components.md"
        ).read_text(encoding="utf-8")

        required_contracts = (
            "Markdown table",
            "Mermaid flowchart",
            "Clickable file links",
            "Embedded image or video",
            "::code-comment",
            "::git-create-branch",
            "::git-stage",
            "::git-commit",
            "::git-push",
            "::git-create-pr",
            "Never emit a directive for an attempted, skipped, failed",
            "absolute paths",
        )

        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, reference)

    def test_shared_reference_has_recipe_for_every_workflow_skill(self):
        reference = (
            SKILLS_ROOT / "m-autoflow" / "references" / "output-components.md"
        ).read_text(encoding="utf-8")

        for skill_name in WORKFLOW_SKILLS:
            with self.subTest(skill=skill_name):
                self.assertIn(f"`${skill_name}`", reference)

    def test_thesis_skill_keeps_a_standalone_visual_output_contract(self):
        skill_text = (
            SKILLS_ROOT / "m-thesis-aigc-revision" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Output", skill_text)
        self.assertIn("absolute clickable paths", skill_text)
        self.assertIn("compact table", skill_text)
        self.assertIn("Do not add a decorative visualization", skill_text)


if __name__ == "__main__":
    unittest.main()
