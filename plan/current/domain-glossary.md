---
title: "Domain Glossary - Scaffold the Python project and its CI"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Scaffold the Python project and its CI

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Version:** 0.1.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| dev extra | The `dev` optional dependency group in `pyproject.toml` that lists `pytest` and `ruff` | none | stem-core, stem-service, stem-web |
| smoke test | One test per component that imports its package and checks `__version__` | none | stem-core, stem-service, stem-web |
| stem | One audio track that a separation produces, such as vocals | none | stem-core |
