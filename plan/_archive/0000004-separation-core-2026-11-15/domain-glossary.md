---
title: "Domain Glossary - Add the two-pass separation core"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the two-pass separation core

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Version:** 0.2.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| pass 1 | The first separation. It splits a mix into vocals and instrumental | none | stem-core |
| pass 2 | The optional second separation. It splits the instrumental into drums, bass, and other | none | stem-core |
| full stems | The `full_stems=True` option that runs pass 2 | none | stem-core |
| model folder | The folder that `STEMS_MODEL_DIR` names. It holds the downloaded model files | none | stem-core |
| separator factory | A callable that builds the object that loads models and separates files. Tests inject a fake | none | stem-core |
