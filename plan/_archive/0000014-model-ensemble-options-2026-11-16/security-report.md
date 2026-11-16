---
title: "Security Report - 0000014-model-ensemble-options"
summary: "Findings for the model options on the command, the upload route, the worker, and the page."
---
# Security Report - 0000014-model-ensemble-options

## Findings

| Finding | Location | Severity | Mitigation |
|---------|----------|----------|------------|
| A caller supplies a model name that makes the engine fetch an unexpected file | `validate_options()` in `src/stem-core/stem_core/separation.py` | Medium | Each option checks a fixed allowlist at the command, the upload route, and `split()`. A test rejects other values and counts zero model loads |
| A stored job holds a bad option | `jobs.options`, read in `src/stem-service/stem_service/worker.py` | Low | `split()` validates before it builds a separator, so the job ends `failed` and loads no model. A test covers it |
| The 422 detail echoes the bad value | `create_job` in `src/stem-service/stem_service/api.py` | Low | The value appears in JSON and the page writes it with `textContent`. The browser run showed it as text |
| The page adds three selects | `src/stem-web/stem_web/static/index.html`, `app.js` | Low | The script appends only non-empty values and writes server text with `textContent`. The existing test that rejects `innerHTML` still passes |
| The upload form is open to anyone who reaches the port | `POST /jobs` | Medium | Not mitigated by decision. The service binds to `127.0.0.1` by default, and ADR-0005 records it |
| Dependencies | `pyproject.toml` | Low | The step adds none. `pip-audit` reports no known vulnerabilities |
| Credentials, secrets, and logs | whole step | none | The step handles none |

## Risk register cross-check

- R-001 (unexpected model fetch): mitigated by the allowlists and their tests.
- R-002 (single stem deletes wanted stems): open by design. The docs and the flag help text say so.
- R-003 (pool memory): open. The allowlists cap the pool at 30 separators.
- R-004 (preset changes stem names): open. `split()` raises the error that names the missing file.

## Overall risk rating

Medium, because the service has no login. The step adds no unmitigated critical or high finding.

## Top actions before production

- Keep `STEMS_HOST` on the loopback address, or put a login in front of the service.
- Run one real job for each preset that you plan to offer.
