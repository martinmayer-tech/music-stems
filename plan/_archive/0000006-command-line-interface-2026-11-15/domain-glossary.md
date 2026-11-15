---
title: "Domain Glossary - Add the command-line interface"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the command-line interface

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Version:** 0.3.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| stems | The command that splits a mix from a shell | none | stem-core |
| subcommand | One of `split`, `env`, or `models` | none | stem-core |
| device | The compute target that the separation runs on: `cuda`, `mps`, or `cpu` | none | stem-core |
| probe | A small function that reads one fact about the machine. Tests inject a fake | none | stem-core |
| full stems | The `--full-stems` option that runs pass 2 | none | stem-core |
