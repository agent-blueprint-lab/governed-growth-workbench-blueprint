from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from governed_growth_workbench.engine import evaluate
from governed_growth_workbench.validation import ValidationError, validate_instance


ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_profile_requires_synthetic_identifier(self) -> None:
        profile = json.loads(
            (ROOT / "examples" / "profiles.synthetic.json").read_text(encoding="utf-8")
        )[0]
        unsafe = deepcopy(profile)
        unsafe["subject_id"] = "ORG-001"
        with self.assertRaises(ValidationError):
            validate_instance(
                unsafe, ROOT / "schemas" / "profile-snapshot.schema.json", "profile"
            )

    def test_ruleset_must_be_marked_synthetic(self) -> None:
        ruleset = json.loads(
            (ROOT / "config" / "rules.synthetic.json").read_text(encoding="utf-8")
        )
        unsafe = deepcopy(ruleset)
        unsafe["synthetic_demo_only"] = False
        with self.assertRaises(ValidationError):
            validate_instance(unsafe, ROOT / "schemas" / "ruleset.schema.json", "ruleset")

    def test_lifecycle_thresholds_must_increase(self) -> None:
        profiles = json.loads(
            (ROOT / "examples" / "profiles.synthetic.json").read_text(encoding="utf-8")
        )
        ruleset = json.loads(
            (ROOT / "config" / "rules.synthetic.json").read_text(encoding="utf-8")
        )
        ruleset["lifecycle_days"] = {"at_risk": 20, "dormant": 10, "lost": 40}
        with self.assertRaisesRegex(ValueError, "must increase"):
            evaluate(profiles, ruleset, ROOT / "schemas")


if __name__ == "__main__":
    unittest.main()
