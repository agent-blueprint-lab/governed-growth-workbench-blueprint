# Maintainer Workflow

## Triage

- Use public issues for reproducible bugs and generic rule proposals.
- Redirect vulnerabilities or accidental sensitive-data exposure to a private Security Advisory.
- Close requests that require publishing real data or adding automatic outreach without a new threat-model review.

## Pull requests

1. Confirm the issue and intended compatibility impact.
2. Review the privacy/governance checklist first.
3. Inspect code, schemas, examples, tests, and docs together.
4. Require `make verify` and passing CI.
5. Prefer a focused squash merge that links the issue.

## Releases

1. Move completed entries from `Unreleased` into a versioned changelog section.
2. Run the publication checklist and `make verify` on a clean checkout.
3. Merge through a reviewed pull request.
4. Create and push an annotated semantic-version tag.
5. Confirm the tag workflow builds source and wheel artifacts and creates the GitHub release.
6. Verify the public release page, commit identity, artifacts, and adoption claims.

## Incident handling

If sensitive data is exposed, stop normal release work, make the affected public surface unavailable when possible, preserve a private investigation record, rotate any affected credentials outside this repository, and publish only a sanitized remediation note.
