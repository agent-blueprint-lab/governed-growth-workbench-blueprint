# Threat Model

## Assets

- The integrity of synthetic profile, rule, opportunity, and audit contracts.
- The privacy of any real data held by a downstream adopter.
- The separation between decision support and external execution.
- The reproducibility of rule evaluation and experiment assignment.

## Threats and controls

| Threat | Control in this repository | Residual risk |
| --- | --- | --- |
| Real data is committed publicly | SYN-only schemas, publication scan, PR checklist, private security reporting | Pattern scans cannot recognize every identifying combination |
| Missing data is treated as zero | Nullable facts plus fail-closed data status | Downstream mappings can still be incorrect |
| A high priority bypasses restrictions | Central execution-gate precedence | A downstream fork could remove the gate |
| A rule changes without traceability | Rule and rule-set versions, deterministic snapshot tests | Governance depends on reviewer discipline |
| A control subject receives an action | Stable `CONTROL` status and deferred review | External integrations are outside this repository |
| A model invents facts or takes action | No model client; policy separates facts, judgment, advice, and unknowns | Downstream model adapters need independent evaluation |
| CI or release publishes unverified code | Required local verification and tag-triggered build checks | Branch protection must be configured by repository admins |

## Out-of-scope systems

Authentication, authorization, production storage, real contact permissions, data retention, model-provider contracts, network security, and incident response are deployment responsibilities. This repository supplies reference contracts and tests, not a production compliance claim.
