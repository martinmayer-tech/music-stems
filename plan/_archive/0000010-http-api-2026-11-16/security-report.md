# Security Report - 0000010-http-api

**Skill:** [validate-and-accept](../../ravintio-zero/skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000010-http-api
**Version:** 0.5.0

> It is advisory - the review makes no code changes. All findings require human review before action.

## Summary

**Overall Risk Assessment:** medium
**Components Reviewed:** stem-service
**Review Scope:** code review, dependency audit, and threat model

The service has no login by decision. It binds to `127.0.0.1` by default, so the exposure stays on the local host. No finding is critical or high.

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | medium | auth | stem-service | `src/stem-service/stem_service/api.py` has no login. An operator who sets `STEMS_HOST` to a public address exposes an open upload route | Keep the loopback default. The docs in `src/stem-service/docs/risk.md` warn about it. Add auth in a later initiative before any public bind | accepted |
| S-002 | low | injection | stem-service | The upload route in `api.py` (`create_job`) builds a path from the client's file name. `_client_file_name` keeps only the last part of the name, and the file lands in a random folder | None. `test_req_001_keeps_only_the_last_part_of_the_client_file_name` covers `..` and backslash input | mitigated |
| S-003 | low | injection | stem-service | The stem route in `api.py` (`get_stem`) takes a name from the URL. It reads no path from the request and serves only a path that the job's stored outputs list | None. `test_req_003_refuses_a_name_the_job_does_not_list` covers encoded `..` and nested names | mitigated |
| S-004 | low | data-exposure | stem-service | A job in JSON could leak a server path. `_job_json` returns file names and no path | None. `test_req_002_reads_a_queued_job_with_no_server_path` checks the body | mitigated |
| S-005 | low | config | stem-service | FastAPI buffers a multipart body before the route runs, so the size limit protects the data folder and not memory | Document it. `src/stem-service/docs/quirks.md` does | accepted |
| S-006 | low | config | stem-service | A job's `error` holds the first line of an exception, which can name a server path | Accept for a service on the local host. Revisit when a public bind is planned | accepted |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| fastapi | 0.163.1 | none | low | none |
| uvicorn | 0.54.0 | none | low | none |
| python-multipart | 0.0.33 | none | low | none |
| httpx | 0.28.1 | none | low | none |

`pip-audit` reported no known vulnerabilities for the environment on 2026-11-16. The root `pyproject.toml` sets no version pin for these four libraries.

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|--------------|-------------------|------------|--------|--------------------|----|
| Another host uploads files | A public `STEMS_HOST` bind | stem-service | low | medium | Loopback default | No login |
| Path traversal through a name | `..` or `\` in an upload name or a stem name | stem-service | medium | high | Name cleaning and a lookup in stored outputs | None |
| Disk fill | Many large uploads | stem-service | low | medium | `STEMS_MAX_UPLOAD_MB` for each upload | No total quota or rate limit |

## Recommendations

1. Add auth before any bind to a non-loopback address.
2. Add a total disk quota and a job cap if the service ever serves more than one trusted user.

## Risk register check

| Risk | Outcome |
|------|---------|
| R-001 path reaches outside the data folder | Mitigated by S-002 and S-003 |
| R-002 public bind | Open, accepted as S-001 |
| R-003 disk fill | Mitigated for one upload, open for the total |
| R-004 worker outlives a test app | Mitigated. `test_req_004_the_app_stops_its_worker_at_shutdown` |
| R-005 real `Separator` ignores `output_dir` | Open. Carried from step 4 |
