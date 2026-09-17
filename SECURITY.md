# Security Policy

## Supported versions

Security fixes target the latest published release and the `main` branch while the project is in early development.

## Report privately

Use a private [GitHub Security Advisory](https://github.com/agent-blueprint-lab/governed-growth-workbench-blueprint/security/advisories/new) for vulnerabilities or accidental sensitive-data exposure. Do not include real data, credentials, or private logs in a public issue.

## Public repository boundary

This repository must not contain real people, customers, organizations, products, contact details, account or order identifiers, raw content, internal database names, private domains, local user paths, network addresses, credentials, revenue, user counts, conversion metrics, or production thresholds.

All examples must be synthetic. Public sample identifiers must use the `SYN-*` prefix.

## Security model

- The reference engine accepts local JSON only and performs no network requests.
- It has no connector for messaging, CRM, databases, payments, or file export.
- Non-ready data fails closed and generates only an audit event.
- Contact restrictions and experiment controls override priority.
- Inputs and outputs are checked against JSON Schema.
- `make verify` includes a repository publication scan and negative security tests.

The scanner is a defense-in-depth control, not proof that a repository is safe to publish. Maintainers must review the diff and the [publication checklist](docs/publication-safety-checklist.md) before every release.
