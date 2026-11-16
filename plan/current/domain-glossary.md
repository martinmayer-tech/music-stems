---
title: "Domain Glossary - Add the HTTP API"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the HTTP API

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Version:** 0.5.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| job | One request to split one mix, stored as a row in `jobs` | none | stem-service |
| upload | The audio file that a caller posts to `POST /jobs` | none | stem-service |
| stem | One separated audio track of a finished job, served as a WAV file | none | stem-service, stem-core |
| stem name | The file name of one entry in a job's outputs. It names a stem in the URL | none | stem-service |
| app | The FastAPI object that `create_app()` returns | none | stem-service |
| upload limit | The largest upload in megabytes, from `STEMS_MAX_UPLOAD_MB` | none | stem-service |
