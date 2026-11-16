---
title: "Domain Glossary - Add the web front end"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add the web front end

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Version:** 0.6.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| page | The one HTML document that the API serves at `/` | none | stem-web, stem-service |
| page folder | The folder `stem_web/static`, which `static_dir()` returns | none | stem-web |
| job list | The part of the page that shows each job with its status | none | stem-web |
| stem link | The URL and the name of one stem, from `stemLinks()` | none | stem-web |
| polling | The page re-reads `GET /jobs` every two seconds while a job is unfinished | none | stem-web |
