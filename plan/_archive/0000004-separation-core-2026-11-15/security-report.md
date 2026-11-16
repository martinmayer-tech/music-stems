# Security Report - Add the two-pass separation core

**Skill:** [validate-and-accept](../../ravintio-zero/skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000004-separation-core
**Version:** 0.2.0

> The review is advisory. It makes no code changes.

## Summary

**Overall Risk Assessment:** low
**Components Reviewed:** stem-core
**Review Scope:** code review and dependency review

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | low | injection | stem-core | `split()` in `src/stem-core/stem_core/separation.py` passes the caller's mix path to the separator and writes to the caller's output folder. The function builds no shell command. | Step 5 must validate upload names before it calls `split()`. | accepted |
| S-002 | low | data-exposure | stem-core | `split()` deletes `residual_vocals.wav` in the output folder. The name is fixed, and the function only deletes a path that the separator reported. | None. | accepted |
| S-003 | low | dependency | stem-core | `audio-separator[cpu]==0.48.0` pulls large machine learning packages and downloads model files on first use. | Pin stays exact. Review it on each upgrade. | accepted |
| S-004 | informational | config | stem-core | The workflow job keeps `permissions: contents: read`. | None. | mitigated |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| audio-separator | 0.48.0 | none checked, no audit tool in the approved set | low | accept-risk |

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|---------------|--------------------|------------|--------|---------------------|-----|
| Path traversal through the mix path | A caller passes a crafted path | stem-core | low | low | The function opens only the path it gets and trusts the caller | Step 5 validates uploads |

## Credentials

The change holds no credential, token, or secret.

## Top actions before production

- Validate upload names in step 5.
