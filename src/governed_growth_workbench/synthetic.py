from __future__ import annotations

import random
from typing import Any


def generate_profiles(count: int, seed: int, snapshot_date: str) -> list[dict[str, Any]]:
    if count < 1:
        raise ValueError("count must be at least 1")

    randomizer = random.Random(seed)
    subject_types = ("individual", "professional", "organization", "partner_candidate")
    profiles = []
    for index in range(1, count + 1):
        subject_type = subject_types[(index - 1) % len(subject_types)]
        prefix = {
            "individual": "IND",
            "professional": "PRO",
            "organization": "ORG",
            "partner_candidate": "PARTNER",
        }[subject_type]
        profiles.append(
            {
                "subject_id": f"SYN-{prefix}-{index:04d}",
                "snapshot_date": snapshot_date,
                "subject_type": subject_type,
                "data_status": randomizer.choices(
                    ("ready", "late", "blocked"), weights=(8, 1, 1), k=1
                )[0],
                "facts": {
                    "days_since_activity": randomizer.choice((1, 4, 9, 16, 24, 41, None)),
                    "recent_usage_count": randomizer.choice((0, 1, 3, 8, None)),
                    "available_units_band": randomizer.choice(
                        ("unknown", "none", "low", "medium", "high")
                    ),
                    "has_prior_purchase": randomizer.choice((True, False)),
                    "organization_signal": randomizer.choice(
                        ("none", "unverified", "verified", "unknown")
                    ),
                    "contact_status": randomizer.choice(("clear", "hold", "unknown")),
                },
            }
        )
    return profiles
