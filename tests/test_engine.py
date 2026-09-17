from __future__ import annotations

import json
import unittest
from pathlib import Path

from governed_growth_workbench.engine import evaluate


ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = json.loads(
            (ROOT / "examples" / "profiles.synthetic.json").read_text(encoding="utf-8")
        )
        cls.ruleset = json.loads(
            (ROOT / "config" / "rules.synthetic.json").read_text(encoding="utf-8")
        )

    def test_replay_is_deterministic_and_matches_snapshot(self) -> None:
        first = evaluate(self.profiles, self.ruleset, ROOT / "schemas")
        second = evaluate(self.profiles, self.ruleset, ROOT / "schemas")
        self.assertEqual(first, second)
        expected = json.loads(
            (ROOT / "examples" / "opportunities.json").read_text(encoding="utf-8")
        )
        self.assertEqual(first[0], expected)

    def test_blocked_profile_fails_closed(self) -> None:
        opportunities, audit_events = evaluate(self.profiles, self.ruleset, ROOT / "schemas")
        blocked_id = "SYN-ORG-004"
        self.assertNotIn(blocked_id, {item["subject_id"] for item in opportunities})
        self.assertIn(
            (blocked_id, "data_blocked", "DATA_NOT_READY"),
            {(item["target_id"], item["action"], item["reason_code"]) for item in audit_events},
        )

    def test_every_output_is_synthetic_and_reviewable(self) -> None:
        opportunities, _ = evaluate(self.profiles, self.ruleset, ROOT / "schemas")
        self.assertTrue(opportunities)
        statuses = set()
        for opportunity in opportunities:
            self.assertTrue(opportunity["opportunity_id"].startswith("SYN-OPP-"))
            self.assertTrue(opportunity["subject_id"].startswith("SYN-"))
            self.assertTrue(opportunity["synthetic"])
            self.assertIn(opportunity["execution_status"], {"READY", "REVIEW", "HOLD", "CONTROL"})
            statuses.add(opportunity["execution_status"])
        self.assertEqual(statuses, {"READY", "REVIEW", "HOLD", "CONTROL"})


if __name__ == "__main__":
    unittest.main()
