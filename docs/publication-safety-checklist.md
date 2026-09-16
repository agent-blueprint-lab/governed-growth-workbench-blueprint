# Publication Safety Checklist

Complete this before every public pull request and release.

- [ ] Work was created from approved public abstractions, not copied from a private production repository.
- [ ] Examples use generic names and `SYN-*` identifiers only.
- [ ] No real person, organization, customer, product, contact detail, raw content, screenshot, or private metric is present.
- [ ] No internal database, field, domain, network address, local user path, credential, certificate, or environment value is present.
- [ ] Demo parameters are clearly marked synthetic and are not described as production recommendations.
- [ ] `python -m governed_growth_workbench verify-publication --root .` passes.
- [ ] `make verify` passes from a clean environment.
- [ ] The staged diff and commit metadata use a public maintainer identity.
- [ ] CI is green and the pull-request privacy checklist is complete.
- [ ] Release notes do not claim users, adoption, performance, or deployments without public evidence.

This checklist reduces accidental disclosure risk. It does not replace legal, security, privacy, or open-source review required by a downstream organization.
