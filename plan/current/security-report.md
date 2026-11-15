# Security Report - Scaffold the Python project and its CI

**Skill:** [validate-and-accept](../../ravintio-zero/skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000002-python-scaffold
**Version:** 0.1.0

> It is advisory. The review makes no code changes.

## Summary

**Overall Risk Assessment:** low
**Components Reviewed:** stem-core, stem-service, stem-web
**Review Scope:** code review, dependency audit, CI workflow review

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | low | dependency | stem-core | `pyproject.toml:14` lists `pytest` and `ruff` with no version pin, so CI installs the newest release on each run | Pin versions when a lock file arrives in a later step | open |
| S-002 | informational | config | stem-core | `.github/workflows/ravintio.yml` job `python` sets `permissions: contents: read` and `persist-credentials: false`, and pins both actions to a commit SHA | None | mitigated |
| S-003 | informational | injection | stem-core | The `python` job reads no pull request text, so it has no script injection path | None | mitigated |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| pytest | newest at install | none known to the review | low | accept-risk |
| ruff | newest at install | none known to the review | low | accept-risk |

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|--------------|-------------------|------------|--------|--------------------|----|
| A compromised PyPI release runs in CI | `pip install` of an unpinned dev tool | stem-core | low | medium | Read-only job token, no secrets in the job | No version pin |

## Recommendations

1. Pin `pytest` and `ruff` when a later step adds a lock file.
