from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from .validation import validate_instance, validate_many


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256("|".join(parts).encode("utf-8")).hexdigest()[:12].upper()
    return f"SYN-{prefix}-{digest}"


def _in_control_group(subject_id: str, ruleset_version: str, percentage: int) -> bool:
    bucket = int(sha256(f"{subject_id}|{ruleset_version}".encode("utf-8")).hexdigest()[:8], 16) % 100
    return bucket < percentage


def _matches(facts: dict[str, Any], conditions: dict[str, Any]) -> bool:
    checks = {
        "has_prior_purchase": lambda expected: facts["has_prior_purchase"] is expected,
        "available_units_band_in": lambda expected: facts["available_units_band"] in expected,
        "recent_usage_count_min": lambda expected: facts["recent_usage_count"] is not None
        and facts["recent_usage_count"] >= expected,
        "days_since_activity_min": lambda expected: facts["days_since_activity"] is not None
        and facts["days_since_activity"] >= expected,
        "organization_signal_in": lambda expected: facts["organization_signal"] in expected,
    }
    return all(checks[name](expected) for name, expected in conditions.items())


def _lifecycle(facts: dict[str, Any], lifecycle_days: dict[str, int]) -> str:
    days = facts["days_since_activity"]
    if days is None:
        return "unknown"
    if days < lifecycle_days["at_risk"]:
        return "active"
    if days < lifecycle_days["dormant"]:
        return "at_risk"
    if days < lifecycle_days["lost"]:
        return "dormant"
    return "lost"


def _execution_status(facts: dict[str, Any], control: bool) -> str:
    if facts["contact_status"] == "hold":
        return "HOLD"
    if facts["contact_status"] == "unknown" or facts["organization_signal"] == "unverified":
        return "REVIEW"
    if control:
        return "CONTROL"
    return "READY"


def _audit_event(
    snapshot_date: str,
    target_id: str,
    action: str,
    reason_code: str,
    rule_version: str | None,
) -> dict[str, Any]:
    return {
        "event_id": _stable_id("AUD", snapshot_date, target_id, action, reason_code, rule_version or "none"),
        "occurred_at": f"{snapshot_date}T00:00:00Z",
        "actor_type": "system",
        "action": action,
        "target_id": target_id,
        "reason_code": reason_code,
        "rule_version": rule_version,
        "model_version": None,
        "synthetic": True,
    }


def evaluate(
    profiles: list[dict[str, Any]],
    ruleset: dict[str, Any],
    schema_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    validate_many(profiles, schema_dir / "profile-snapshot.schema.json", "profiles")
    validate_instance(ruleset, schema_dir / "ruleset.schema.json", "ruleset")
    lifecycle_days = ruleset["lifecycle_days"]
    if not lifecycle_days["at_risk"] < lifecycle_days["dormant"] < lifecycle_days["lost"]:
        raise ValueError("lifecycle_days must increase from at_risk to dormant to lost")

    opportunities: list[dict[str, Any]] = []
    audit_events: list[dict[str, Any]] = []
    ruleset_version = ruleset["ruleset_version"]

    for profile in sorted(profiles, key=lambda item: item["subject_id"]):
        subject_id = profile["subject_id"]
        snapshot_date = profile["snapshot_date"]
        if profile["data_status"] != "ready":
            audit_events.append(
                _audit_event(snapshot_date, subject_id, "data_blocked", "DATA_NOT_READY", None)
            )
            continue

        facts = profile["facts"]
        for rule in ruleset["rules"]:
            if not _matches(facts, rule["when"]):
                continue

            control = _in_control_group(subject_id, ruleset_version, ruleset["control_percentage"])
            status = _execution_status(facts, control)
            opportunity_id = _stable_id(
                "OPP", subject_id, snapshot_date, rule["rule_id"], ruleset_version
            )
            opportunities.append(
                {
                    "opportunity_id": opportunity_id,
                    "subject_id": subject_id,
                    "snapshot_date": snapshot_date,
                    "scenario": rule["scenario"],
                    "rule_version": rule["rule_id"],
                    "ruleset_version": ruleset_version,
                    "value_tier": rule["value_tier"],
                    "lifecycle": _lifecycle(facts, lifecycle_days),
                    "priority": rule["priority"],
                    "evidence": [f"{field}={str(facts[field]).lower()}" for field in rule["evidence_fields"]],
                    "experiment_group": "control" if control else "treatment",
                    "execution_status": status,
                    "review_status": "deferred" if status in {"HOLD", "CONTROL"} else "pending",
                    "synthetic": True,
                }
            )
            action = {
                "READY": "generated",
                "REVIEW": "review_required",
                "HOLD": "held",
                "CONTROL": "control_assigned",
            }[status]
            audit_events.append(
                _audit_event(snapshot_date, opportunity_id, action, f"STATUS_{status}", rule["rule_id"])
            )

    opportunities.sort(key=lambda item: (item["subject_id"], item["scenario"], item["rule_version"]))
    audit_events.sort(key=lambda item: (item["target_id"], item["action"], item["event_id"]))
    validate_many(opportunities, schema_dir / "opportunity.schema.json", "opportunities")
    validate_many(audit_events, schema_dir / "audit-event.schema.json", "audit_events")
    return opportunities, audit_events
