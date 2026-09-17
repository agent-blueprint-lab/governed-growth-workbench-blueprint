# Governance

Agent Blueprint Lab currently serves as the primary maintainer and release owner.

## Decision process

- Bugs and rule proposals begin with a public issue unless they involve security or sensitive data.
- Functional changes use pull requests, executable tests, and a passing CI run.
- Schema, privacy boundary, or automatic-action changes require an explicit maintainer review.
- Security reports stay private until a safe disclosure decision is made.

## Versioning

The project follows semantic versioning. Breaking CLI or schema changes increment the major version after `1.0.0`; during `0.x`, they increment the minor version and are called out in the changelog.

## Releases

A release requires a clean `main` branch, passing `make verify`, updated changelog, an annotated version tag, and generated GitHub release notes. Release artifacts are source and wheel packages; no package registry publication is implied.

## Maintainer changes

New maintainers must demonstrate sustained, security-conscious contributions. Role changes will be documented publicly rather than implied from commit activity alone.
