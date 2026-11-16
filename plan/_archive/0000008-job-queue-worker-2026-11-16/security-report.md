# Security Report - Add the job queue and worker

**Skill:** [validate-and-accept](../../ravintio-zero/skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Version:** 0.4.0

> The review is advisory. It makes no code changes.

## Summary

**Overall Risk Assessment:** low
**Components Reviewed:** stem-service
**Review Scope:** code review and dependency review

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | low | injection | stem-service | `JobStore` in `src/stem-service/stem_service/jobs.py` builds each SQL statement with `?` parameters. The only interpolated text is the fixed `COLUMNS` constant. | None. | mitigated |
| S-002 | low | path-traversal | stem-service | `Worker` passes `job.input_path` to `split()` as given, and `job_output_dir` joins the job id to `STEMS_DATA_DIR`. The id is a UUID that the store makes. A caller of the Python API chooses the input path. | Step 5 must validate upload names and store uploads inside the data folder before it calls `add()`. | accepted |
| S-003 | low | data-exposure | stem-service | `mark_failed` stores the first line of the exception text, which can hold a file path. The row stays in the local SQLite file. | Step 5 must decide whether the API returns the error line. | accepted |
| S-004 | low | availability | stem-service | The database file and the job folders grow with no limit and no cleanup. | File a retention entry before the service runs for long. | accepted |
| S-005 | informational | dependency | stem-service | The step adds no dependency. `sqlite3` and `threading` come from the standard library. | None. | mitigated |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| none added | not applicable | not applicable | not applicable | none |

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|---------------|--------------------|------------|--------|---------------------|-----|
| Two workers run one job | A race on `claim_next()` | stem-service | low | medium | `BEGIN IMMEDIATE` makes the claim one transaction. A test runs two workers over six jobs | None |
| SQL injection through the input path | A crafted path in `add()` | stem-service | low | high | Parameterised statements | None |

## Credentials

The change holds no credential, token, or secret.

## Top actions before production

- Validate upload names and keep uploads inside the data folder in step 5.
- Add a retention rule for old jobs and outputs.
