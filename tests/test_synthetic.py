from __future__ import annotations

import unittest

from governed_growth_workbench.synthetic import generate_profiles


class SyntheticGeneratorTests(unittest.TestCase):
    def test_generation_is_seeded_and_identifiers_are_synthetic(self) -> None:
        first = generate_profiles(8, 7, "2026-01-15")
        second = generate_profiles(8, 7, "2026-01-15")
        self.assertEqual(first, second)
        self.assertTrue(all(item["subject_id"].startswith("SYN-") for item in first))

    def test_count_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 1"):
            generate_profiles(0, 7, "2026-01-15")


if __name__ == "__main__":
    unittest.main()
