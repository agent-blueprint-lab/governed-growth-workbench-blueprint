from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from governed_growth_workbench.safety import scan


ROOT = Path(__file__).resolve().parents[1]


class PublicationSafetyTests(unittest.TestCase):
    def test_repository_passes_publication_scan(self) -> None:
        self.assertEqual(scan(ROOT), [])

    def test_scanner_detects_contact_and_local_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = "owner" + "@" + "private.example\n" + "/" + "Users/person/private.txt\n"
            (root / "unsafe.txt").write_text(content, encoding="utf-8")
            rules = {finding.rule for finding in scan(root)}
            self.assertEqual(rules, {"email", "local-user-path"})

    def test_denylist_is_applied_without_scanning_itself(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config" / "publication-denylist.txt").write_text(
                "private-brand\n", encoding="utf-8"
            )
            (root / "README.md").write_text("private-brand\n", encoding="utf-8")
            findings = scan(root)
            self.assertEqual([(item.path.as_posix(), item.rule) for item in findings], [("README.md", "denylist-term")])


if __name__ == "__main__":
    unittest.main()
