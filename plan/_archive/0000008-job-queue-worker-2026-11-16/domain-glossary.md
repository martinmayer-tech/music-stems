---
title: "Domain Glossary - Add the job queue and worker"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the job queue and worker

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Version:** 0.4.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| job | One request to split one mix, stored as a row in `jobs` | none | stem-service |
| job store | The class that reads and writes the `jobs` table | none | stem-service |
| worker | A thread that claims queued jobs and runs them one at a time | none | stem-service |
| device | A compute target that has one worker. The name is a label for the pool | none | stem-service |
| claim | The step that moves the oldest `queued` job to `running` | none | stem-service |
| recover | The step that returns each `running` job to `queued` after a restart | none | stem-service |
| pooled separator | The object that gives `split()` a separator and reuses each loaded model | none | stem-service |
