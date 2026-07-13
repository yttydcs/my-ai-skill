from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "m-context"
    / "scripts"
    / "context_loader.py"
)
SPEC = importlib.util.spec_from_file_location("m_context_loader", SCRIPT_PATH)
assert SPEC and SPEC.loader
loader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(loader)


class ContextLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_context(self, name: str, content: str) -> Path:
        path = self.root / f"{name}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_root_resolution_precedence(self) -> None:
        explicit = self.root / "explicit"
        codex_home = self.root / "codex"
        actual = loader.resolve_context_root(
            {"M_CONTEXT_HOME": str(explicit), "CODEX_HOME": str(codex_home)},
            home=self.root / "home",
        )
        self.assertEqual(actual, explicit.resolve())

        actual = loader.resolve_context_root(
            {"M_CONTEXT_HOME": "", "CODEX_HOME": str(codex_home)},
            home=self.root / "home",
        )
        self.assertEqual(actual, (codex_home / "m-contexts").resolve())

        actual = loader.resolve_context_root({}, home=self.root / "home")
        self.assertEqual(actual, (self.root / "home" / ".codex" / "m-contexts").resolve())

    def test_lists_and_finds_unicode_names_without_reading_bodies(self) -> None:
        (self.root / "nas配置.md").write_bytes(b"\xff")
        self.write_context("Test Account", "content")
        (self.root / "ignored.txt").write_text("ignored", encoding="utf-8")

        self.assertEqual(loader.list_contexts(self.root), ["nas配置", "Test Account"])
        self.assertEqual(loader.find_contexts(self.root, "NAS"), ["nas配置"])

    def test_loads_complete_unicode_context(self) -> None:
        expected = "# NAS\n\n密码：example\n"
        self.write_context("nas配置", expected)
        self.assertEqual(loader.load_context(self.root, "nas配置"), expected)

    def test_extracts_section_with_nested_headings(self) -> None:
        content = (
            "# NAS\n\n"
            "## 连接\nvalue\n\n"
            "## 测试方式\ncommand\n\n"
            "### 清理\ncleanup\n\n"
            "## 部署\ndeploy\n"
        )
        self.write_context("nas配置", content)
        self.assertEqual(
            loader.load_context(self.root, "nas配置", "测试方式"),
            "## 测试方式\ncommand\n\n### 清理\ncleanup\n\n",
        )

    def test_rejects_missing_and_duplicate_sections(self) -> None:
        self.write_context("duplicate", "## Same\none\n## Same\ntwo\n")
        with self.assertRaisesRegex(loader.ContextError, "ambiguous"):
            loader.load_context(self.root, "duplicate", "Same")
        with self.assertRaisesRegex(loader.ContextError, "Available headings"):
            loader.load_context(self.root, "duplicate", "Missing")

    def test_rejects_invalid_utf8(self) -> None:
        (self.root / "invalid.md").write_bytes(b"\xff\xfe")
        with self.assertRaisesRegex(loader.ContextError, "not valid UTF-8"):
            loader.load_context(self.root, "invalid")

    def test_rejects_unsafe_names_and_extensions(self) -> None:
        for name in (
            "",
            "..",
            "../secret",
            "folder/context",
            "folder\\context",
            "name.md",
            "name:stream",
            "name.",
            "CON",
        ):
            with self.subTest(name=name):
                with self.assertRaises(loader.ContextError):
                    loader.validate_context_name(name)

    def test_ignores_heading_like_text_inside_fenced_code(self) -> None:
        content = (
            "## 私钥\n"
            "```text\n"
            "## Not a section\n"
            "```\n"
            "## 测试\n"
            "command\n"
        )
        self.write_context("fenced", content)
        self.assertEqual(loader.load_context(self.root, "fenced", "私钥"), content.split("## 测试", 1)[0])
        with self.assertRaisesRegex(loader.ContextError, "Section not found"):
            loader.load_context(self.root, "fenced", "Not a section")

    def test_missing_context_reports_actionable_error(self) -> None:
        self.write_context("nas配置", "content")
        with self.assertRaisesRegex(loader.ContextError, "Context not found"):
            loader.load_context(self.root, "nas")

    def test_rejects_symlink_escape_when_supported(self) -> None:
        outside_dir = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: outside_dir.rmdir())
        outside_file = outside_dir / "outside.md"
        outside_file.write_text("secret", encoding="utf-8")
        self.addCleanup(outside_file.unlink)
        link = self.root / "escape.md"
        try:
            link.symlink_to(outside_file)
        except OSError as exc:
            self.skipTest(f"Symlink creation is unavailable: {exc}")

        with self.assertRaisesRegex(loader.ContextError, "outside the configured root"):
            loader.load_context(self.root, "escape")

    def test_cli_loads_selected_section_and_reports_failures(self) -> None:
        self.write_context("nas配置", "## 连接\nhost\n## 测试\ncommand\n")
        env = os.environ.copy()
        env["M_CONTEXT_HOME"] = str(self.root)

        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "load", "nas配置", "--section", "测试"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "## 测试\ncommand\n")
        self.assertEqual(completed.stderr, "")

        missing = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "load", "missing"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("Context not found", missing.stderr)


if __name__ == "__main__":
    unittest.main()
