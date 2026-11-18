---
title: "Requirement: REQ-004 - Options on the page"
summary: "The upload form gains three selects, and the script sends the chosen values with the file."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-004 - Options on the page

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Source:** US-004
**Priority:** must-have

## User Story

As a user, I choose the options on the upload form, so that I need no `curl`.

## Functional Requirements
- `index.html` holds three selects named `model`, `ensemble_preset`, and `single_stem`. Each first option has the empty value and the label `Default`.
- Each select lists exactly the values of its allowlist in `stem_core.separation`.
- `app.js` appends a field to the upload data only when the select holds a non-empty value. A pure function, `optionFields()`, returns those pairs.
- The page shows the API's `detail` text when it answers 422, as it does for any error.

## Acceptance Criteria
- [ ] AC-1: Show the selects
  - Given the served page
  - When a test reads `GET /`
  - Then the page holds the three selects, each with a `Default` option with the empty value
- [ ] AC-2: Match the allowlists
  - Given the served page and `stem_core`
  - When a test compares the select values
  - Then each select lists exactly the values of its allowlist
- [ ] AC-3: Send only chosen values
  - Given the served script
  - When `optionFields()` runs under `node` with one empty value and one set value
  - Then it returns the pair for the set value only

## Dependencies
- REQ-001 holds the allowlists. REQ-003 accepts the fields.
