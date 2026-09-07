"""結構測試：Claude Code 與 Codex 兩套封裝共用同一份 skill，安裝文件覆蓋三條路徑。"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "research-report-kit"
SKILLS = PLUGIN / "skills"
SKILL_NAMES = (
    "research-report-output",
    "equity-valuation-discipline",
    "product-cycle-rotation",
    "price-routing",
)
GITHUB = "https://github.com/Benjamin-Teng/industrials-research-skill"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestPluginManifests(unittest.TestCase):
    def test_both_hosts_publish_same_name_and_semver(self) -> None:
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        self.assertEqual(claude["name"], "research-report-kit")
        self.assertEqual(codex["name"], "research-report-kit")
        self.assertEqual(claude["version"], codex["version"])
        self.assertRegex(claude["version"], r"^\d+\.\d+\.\d+$")

    def test_codex_manifest_points_to_shared_skills_only(self) -> None:
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        self.assertEqual(codex["skills"], "./skills/")
        for absent in ("hooks", "mcpServers", "apps"):
            self.assertNotIn(absent, codex)
        interface = codex["interface"]
        for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            self.assertTrue(interface.get(key), key)
        self.assertLessEqual(len(interface["defaultPrompt"]), 3)

    def test_claude_marketplace_entry_matches_plugin(self) -> None:
        marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
        plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        self.assertEqual(marketplace["name"], "research-tools")
        [entry] = marketplace["plugins"]
        self.assertEqual(entry["name"], "research-report-kit")
        self.assertEqual(entry["source"], "./plugins/research-report-kit")
        self.assertEqual(entry["version"], plugin["version"])

    def test_codex_marketplace_points_to_existing_local_plugin(self) -> None:
        marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(marketplace["name"], "research-tools")
        self.assertTrue(marketplace["interface"]["displayName"])
        [entry] = marketplace["plugins"]
        self.assertEqual(entry["name"], "research-report-kit")
        self.assertEqual(entry["source"]["source"], "local")
        target = ROOT / entry["source"]["path"]
        self.assertTrue((target / ".codex-plugin" / "plugin.json").is_file())
        self.assertEqual(target.name, entry["name"])
        self.assertIn(entry["policy"]["installation"], {"AVAILABLE", "INSTALLED_BY_DEFAULT"})
        self.assertIn(entry["policy"]["authentication"], {"ON_INSTALL", "ON_USE"})
        self.assertTrue(entry["category"])

    def test_no_stray_root_manifest(self) -> None:
        self.assertFalse((ROOT / "manifest.json").exists())


class TestSkillMetadata(unittest.TestCase):
    def test_every_skill_has_openai_yaml_with_implicit_invocation(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                text = read(SKILLS / name / "agents" / "openai.yaml")
                self.assertIn("display_name:", text)
                self.assertIn("short_description:", text)
                self.assertIn("default_prompt:", text)
                self.assertRegex(text, r"allow_implicit_invocation:\s*true")

    def test_skill_frontmatter_name_matches_directory(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                match = re.search(r"^name:\s*(\S+)", read(SKILLS / name / "SKILL.md"), re.MULTILINE)
                assert match is not None, name
                self.assertEqual(match.group(1), name)


class TestInstallationDocs(unittest.TestCase):
    def setUp(self) -> None:
        self.readme = read(ROOT / "README.md")

    def test_claude_code_install_path(self) -> None:
        for line in (
            "/plugin marketplace add Benjamin-Teng/industrials-research-skill",
            "/plugin install research-report-kit@research-tools",
            "/reload-plugins",
        ):
            self.assertIn(line, self.readme)

    def test_codex_ide_install_path_lists_every_skill(self) -> None:
        self.assertIn("$skill-installer", self.readme)
        for name in SKILL_NAMES:
            self.assertIn(f"{GITHUB}/tree/main/plugins/research-report-kit/skills/{name}", self.readme)

    def test_codex_cli_install_paths(self) -> None:
        self.assertIn("codex plugin marketplace add Benjamin-Teng/industrials-research-skill", self.readme)
        self.assertIn("codex plugin add research-report-kit@research-tools", self.readme)
        self.assertIn("/plugins", self.readme)

    def test_codex_update_refreshes_marketplace_snapshot_before_reinstall(self) -> None:
        upgrade = self.readme.index("codex plugin marketplace upgrade research-tools")
        reinstall = self.readme.index("codex plugin add research-report-kit@research-tools", upgrade)
        self.assertLess(upgrade, reinstall)

    def test_readme_drops_symlink_and_manifest_instructions(self) -> None:
        for obsolete in ("ln -s", "xcopy", "manifest.json", ".agents/skills"):
            self.assertNotIn(obsolete, self.readme)


if __name__ == "__main__":
    unittest.main()
