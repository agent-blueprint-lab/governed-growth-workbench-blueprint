# Architecture

## Trust boundary

The public package is intentionally local and read-only with respect to external systems. It accepts JSON files, validates them, computes deterministic opportunities, and writes JSON files. There are no network clients or connectors.

```text
synthetic profiles ─┐
                    ├─ schema validation ─ rule evaluation ─ execution gate ─ opportunity JSON
synthetic rules ────┘                          │
                                              └────────────────── audit JSON
```

## Components

| Component | Responsibility | Safety control |
| --- | --- | --- |
| CLI | Parse explicit local file paths and commands | No network or implicit discovery |
| Validation | Enforce profile, rule, output, and audit contracts | Reject unknown fields and non-synthetic IDs |
| Rule engine | Evaluate documented conditions deterministically | No model-generated facts or side effects |
| Execution gate | Resolve `READY`, `REVIEW`, `HOLD`, or `CONTROL` | Restrictions override value and priority |
| Audit writer | Record generation or block reason | Stable synthetic identifiers and reason codes |
| Publication scan | Catch common secrets and identifying patterns | Fails CI and local verification |

## Determinism

Opportunity IDs and control assignment use SHA-256 over synthetic subject, snapshot, rule, and rule-set identifiers. Audit timestamps are anchored to the synthetic snapshot date. The same valid input and rule-set version therefore produce byte-stable semantic output.

## Data failure behavior

Profiles marked `late` or `blocked` never reach rule evaluation. The engine emits only a `data_blocked` audit event. It does not reuse an old profile or silently treat missing values as zero.

## Extension boundary

Adapters for real systems are deliberately excluded. A downstream project should place approved read-only extraction outside this package, map only necessary fields into the public profile contract, and retain human approval after evaluation. Any external write or automatic action requires a new threat model.
