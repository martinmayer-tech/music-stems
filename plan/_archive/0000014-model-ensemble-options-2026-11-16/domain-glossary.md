---
title: "Domain Glossary - Add model choice and ensemble options"
summary: "Definitions of domain terms used within this feature."
status: "active"
version: "0.1.0"
---
# Domain Glossary - Add model choice and ensemble options

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Version:** 0.7.0

## Terms

| Term | Definition | Aliases | Used In |
|------|-----------|---------|---------|
| pass 2 model | The model that splits the instrumental into drums, bass, and other. A caller picks one of three | none | stem-core, stem-service, stem-web |
| ensemble preset | A named set of pass 1 models that `audio-separator` combines. A caller picks one of nine | preset | stem-core, stem-service, stem-web |
| single stem | The one stem that a job keeps. `split()` deletes the others | none | stem-core, stem-service, stem-web |
| allowlist | The fixed list of values that one option accepts | none | stem-core |
| option | A model, a preset, or a single stem that a caller sets | none | all components |
