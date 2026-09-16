# Contributing

Thank you for helping improve this reference implementation. Contributions must remain generic, reproducible, privacy-preserving, and human-reviewed.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
make verify
```

The project intentionally uses the Python standard library for the engine and test runner. `jsonschema` is the only runtime dependency.

## Workflow

1. Open a bug or rule-proposal issue using a template.
2. Create a focused branch linked to the issue.
3. Add or update executable tests for behavior changes.
4. Synchronize schemas, examples, documentation, and changelog where relevant.
5. Run `make verify`.
6. Open a pull request and complete every privacy/governance checkbox.

## Public-data rules

- Use only synthetic examples and `SYN-*` identifiers.
- Do not submit real names, organizations, products, contact details, internal paths, credentials, database names, private metrics, screenshots, or raw logs.
- Mark every numeric rule parameter as synthetic demo data; do not present it as a recommended production threshold.
- Do not add network calls, messaging, database writes, or automatic execution paths without a separate threat-model review.
- Report sensitive-data exposure privately through a GitHub Security Advisory.

## Rule changes

A rule proposal must state its generic purpose, required facts, exclusions, evidence fields, execution gate, rollback behavior, and deterministic test case. Rules may create review candidates; they may not trigger external action.

## Compatibility

Schema changes are compatibility-sensitive. Note whether a change is additive or breaking, update all example snapshots, and follow the versioning policy in `GOVERNANCE.md`.
