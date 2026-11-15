---
title: "Story Map - 0000002-python-scaffold"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000002-python-scaffold

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Set up the project | Install the dev tools from `pyproject.toml` | US-001 | REQ-001 |
| Set up the project | Run `ruff check .` and `pytest` from the repo root | US-001 | REQ-001 |
| Check a pull request | See a red or green Python check | US-002 | REQ-002 |
| Record the version | List the three components in `product.yml` | US-003 | REQ-003 |

## Gaps

- Publish the project as a package: gap: out of scope. Nothing in the brief asks for a published package.
