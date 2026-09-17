# Workflow

## Reference run

1. Load a list of synthetic profile snapshots.
2. Validate every profile and the synthetic rule set.
3. Stop each non-ready profile and record a data-quality audit event.
4. Evaluate matching rules for ready profiles.
5. Create stable opportunity identifiers and evidence strings.
6. Assign a deterministic experiment group.
7. Apply contact and relationship gates.
8. Validate opportunity and audit output before writing files.
9. Route `READY` and `REVIEW` results to people; never execute an external action automatically.

## Gate precedence

```text
data_status != ready
  → no opportunity

contact_status == hold
  → HOLD

contact_status == unknown or relationship unverified
  → REVIEW

stable control assignment
  → CONTROL

otherwise
  → READY
```

`HOLD`, `REVIEW`, and `CONTROL` cannot be overridden by a high value tier or priority.

## Replay and change control

Changing a rule requires a new rule or rule-set version, updated tests, and an updated expected snapshot. Existing output remains attributable to the version that created it. Observation windows and numeric parameters belong in the demo rule file; they must not be hidden in prompts or UI code.

## Optional explanation layer

`prompts/system-policy.md` is a provider-neutral policy example for a downstream explanation layer. This repository includes no model client. If a downstream project adds one, it should receive only validated opportunity evidence and must preserve the same execution gate and human-review boundary.
