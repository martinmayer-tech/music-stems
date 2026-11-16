---
title: "Domain Glossary - Add the Docker image and compose file"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the Docker image and compose file

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Version:** 0.8.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| image | The built container file system that holds Python, FFmpeg, and the service | none | stem-service |
| extra | A set of optional dependencies of `audio-separator`. The image installs `cpu` or `gpu` | none | stem-service |
| named volume | Storage that Docker keeps outside the container, so a restart keeps it | volume | stem-service |
| model volume | The named volume `models`, mounted at `/models`, that holds downloaded models | none | stem-service |
| data volume | The named volume `data`, mounted at `/data`, that holds the job store and job output | none | stem-service |
