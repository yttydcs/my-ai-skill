import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
REVIEW_PATH = SKILLS_ROOT / "m-autoflow/references/review.md"


class AcceptanceReviewPackageTests(unittest.TestCase):
    def test_shared_review_is_packaged_and_reachable_by_consumers(self):
        manifest = json.loads(
            (REPO_ROOT / "manifests/m-autoflow.json").read_text(encoding="utf-8")
        )
        reference = "references/review.md"
        self.assertIn(reference, manifest["reference_files"])
        self.assertTrue(REVIEW_PATH.is_file())
        for name in ("m-execute", "m-test", "m-archive", "m-go", "m-continue"):
            with self.subTest(skill=name):
                package = SKILLS_ROOT / name
                target = "../m-autoflow/references/review.md"
                self.assertIn(target, (package / "SKILL.md").read_text(encoding="utf-8"))
                self.assertEqual((package / target).resolve(), REVIEW_PATH.resolve())
                consumer = json.loads(
                    (REPO_ROOT / f"manifests/{name}.json").read_text(encoding="utf-8")
                )
                self.assertIn("m-autoflow", consumer["depends_on_skills"])


@unittest.skipUnless(shutil.which("git"), "Git is required for documented review commands")
class ReviewGitRecipeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="acceptance-review-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "--quiet")
        self.git("config", "core.autocrlf", "false")
        for name in ("committed.txt", "staged.txt", "unstaged.txt", "overlap.txt", "deleted.txt"):
            (self.repo / name).write_text("baseline\n", encoding="utf-8")
        self.git("add", "--all")
        self.commit("baseline")
        self.base = self.git("rev-parse", "HEAD").decode().strip()
        (self.repo / "committed.txt").write_text("committed behavior\n", encoding="utf-8")
        self.git("add", "--", "committed.txt")
        self.commit("committed change")
        for name in ("staged.txt", "overlap.txt"):
            (self.repo / name).write_text("staged behavior\n", encoding="utf-8")
        self.git("add", "--", "staged.txt", "overlap.txt")
        (self.repo / "unstaged.txt").write_text("unstaged behavior\n", encoding="utf-8")
        # The final worktree can hide an index-only change; both views matter.
        (self.repo / "overlap.txt").write_text("baseline\n", encoding="utf-8")
        (self.repo / "deleted.txt").unlink()
        (self.repo / "new file 中文.txt").write_text("new behavior\n", encoding="utf-8")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], check=True, capture_output=True
        ).stdout

    def commit(self, message):
        self.git(
            "-c", "user.name=Review fixture", "-c", "user.email=review@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", message,
        )

    def recipe(self):
        text = REVIEW_PATH.read_text(encoding="utf-8")
        block = re.search(r"```sh\n(.*?)\n\s*```", text, re.DOTALL)
        self.assertIsNotNone(block, "The shared review must provide executable Git views")
        commands = [shlex.split(line.strip()) for line in block[1].splitlines() if line.strip()]
        outputs = []
        for command in commands:
            self.assertEqual(command[0], "git")
            self.assertIn(command[1], ("status", "diff", "ls-files"))
            args = [self.base if arg == "<review-base-sha>" else arg for arg in command[1:]]
            outputs.append((command, self.git(*args)))
        return outputs

    def test_documented_recipe_sees_all_candidate_surfaces(self):
        views = self.recipe()
        patches = b"\n".join(output for command, output in views if command[1] == "diff")
        for name, expected in (
            (b"committed.txt", b"committed behavior"),
            (b"staged.txt", b"staged behavior"),
            (b"unstaged.txt", b"unstaged behavior"),
            (b"overlap.txt", b"staged behavior"),
            (b"deleted.txt", b"deleted file mode"),
        ):
            with self.subTest(path=name):
                self.assertIn(name, patches)
                self.assertIn(expected, patches)
        untracked = [output for command, output in views if command[1] == "ls-files"]
        self.assertEqual(len(untracked), 1)
        self.assertEqual(untracked[0].split(b"\0")[:-1], ["new file 中文.txt".encode()])

    def test_review_views_leave_head_index_and_worktree_unchanged(self):
        def state():
            return (
                self.git("rev-parse", "HEAD"),
                self.git("ls-files", "--stage", "-z"),
                self.git("status", "--porcelain=v1", "-z"),
                {p.name: p.read_bytes() for p in self.repo.iterdir() if p.is_file()},
            )
        before = state()
        self.recipe()
        self.assertEqual(state(), before)


if __name__ == "__main__":
    unittest.main()
