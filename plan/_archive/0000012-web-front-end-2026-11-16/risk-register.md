---
title: "Risk Register - Add the web front end"
summary: "Technical, operational, and security risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the web front end

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Version:** 0.6.0
**Overall Risk Level:** medium

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | security | A file name or an error line from the server runs as markup in the page | medium | high | The script uses `textContent` and `setAttribute` only. A test rejects `innerHTML` in `app.js` | open |
| R-002 | security | The `/static` mount serves a file outside the page folder | low | high | The mount names the folder from `static_dir()`. A test requests `..` paths | open |
| R-003 | technical | The page logic breaks and no browser test catches it | medium | medium | The stem link logic is a pure function. A `node` test runs it. The step adds no browser automation by decision | open |
| R-004 | operational | `stem_service` cannot import `stem_web` when an operator runs the service outside the repo layout | medium | medium | The component docs state the Python path. Step 8 packages both | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | The user reaches the page on the loopback address or through a trusted tunnel | An exposed service gives anyone the upload form | open |
| A-002 | A `done` job lists WAV stem names in `stems` | A player cannot decode a stem | open |
