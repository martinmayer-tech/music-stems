# Security Report - Add the command-line interface

**Skill:** [validate-and-accept](../../ravintio-zero/skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000006-command-line-interface
**Version:** 0.3.0

> The review is advisory. It makes no code changes.

## Summary

**Overall Risk Assessment:** low
**Components Reviewed:** stem-core
**Review Scope:** code review and dependency review

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | low | injection | stem-core | `probe_ffmpeg()` in `src/stem-core/stem_core/cli.py` runs the path that `shutil.which` finds with the fixed argument `-version`. It uses an argument list, no shell, and a 10-second timeout. | None. | mitigated |
| S-002 | low | path-traversal | stem-core | `stems split` passes the caller's file and folder to `split()` and trusts them. A local user chooses both. | The service in step 5 must validate upload names before it calls `split()`. | accepted |
| S-003 | low | data-exposure | stem-core | The error line prints the exception text, which can hold a file path. The command runs locally and prints to the caller's terminal. | None. | accepted |
| S-004 | informational | dependency | stem-core | The step adds no dependency. `argparse` comes from the standard library. | None. | mitigated |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| none added | not applicable | not applicable | not applicable | none |

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|---------------|--------------------|------------|--------|---------------------|-----|
| Command injection through the FFmpeg probe | A crafted `PATH` entry named `ffmpeg` | stem-core | low | low | The probe runs a fixed argument list with no shell. A local user who controls `PATH` already runs code | None |

## Credentials

The change holds no credential, token, or secret.

## Top actions before production

- Validate upload names in step 5.
