# Roadmap

This roadmap describes intended open-source work, not delivery commitments.

## Completed for v0.1

- Runnable Python CLI and deterministic rule engine.
- JSON Schema validation for inputs, rules, opportunities, and audit events.
- Synthetic dataset generator and replay snapshot.
- Fail-closed data behavior and execution gates.
- Publication safety scan, executable tests, CI, and release automation.
- Issue, pull-request, contribution, security, and governance workflows.

## Next

- Add compatibility fixtures for schema evolution.
- Add property-based tests for rule conflicts without introducing production data.
- Improve the offline demo so it can load generated synthetic output.
- Publish maintainer guidance for safe adapters that remain read-only by default.

## Explicitly out of scope

- Production data connectors.
- Automatic messaging, CRM writes, payments, or identity inference.
- Claims about conversion lift, model accuracy, or recommended business thresholds.
