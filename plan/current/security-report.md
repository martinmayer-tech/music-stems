---
title: "Security Report - 0000012-web-front-end"
summary: "Findings for the web page, the page route, and the static mount."
---
# Security Report - 0000012-web-front-end

## Findings

| Finding | Location | Severity | Mitigation |
|---------|----------|----------|------------|
| Server text could run as markup | `src/stem-web/stem_web/static/app.js` | Medium | The script writes with `textContent` and `setAttribute` only. A test rejects `innerHTML`, `outerHTML`, `insertAdjacentHTML`, and `document.write` |
| A stem URL could carry markup or a path from a stem name | `stemLinks()` in `app.js` | Low | `encodeURIComponent` encodes the job id and the name. The server still looks the name up in the job's outputs |
| The `/static` mount serves a file outside the page folder | `create_app()` in `src/stem-service/stem_service/api.py` | Low | The mount names `static_dir()`. Starlette refuses `..` paths. A test requests encoded `..` paths and gets 404 |
| The upload form is open to anyone who reaches the port | `GET /` and `POST /jobs` | Medium | Not mitigated by decision. The service binds to `127.0.0.1` by default and ADR-0005 records the trade-off |
| Dependencies | `pyproject.toml` | Low | The step adds none. `pip-audit` reports no known vulnerabilities |
| Credentials, secrets, and logs | whole step | none | The step handles none |

## Risk register cross-check

- R-001 (markup from server text): mitigated by the `textContent` rule and its test.
- R-002 (static path escape): mitigated by the folder mount and its test.
- R-003 (no browser test): open by decision. A browser run in P3 observed the flow.
- R-004 (import path): open. The quirks doc states it. Step 8 packages both components.

## Overall risk rating

Medium, because the service has no login. The page adds no unmitigated critical or high finding.

## Top actions before production

- Keep `STEMS_HOST` on the loopback address, or put a login in front of the service.
- Add a favicon route or a link tag if the 404 matters.
