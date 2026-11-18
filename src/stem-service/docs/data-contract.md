---
title: "Data Contract: stem-service"
summary: "Defines the schema of the jobs table that stem-service owns."
status: "active"
version: "0.1.0"
---
# Data Contract - stem-service

**Skill:** [implement](../../../ravintio-zero/skills/ravintio-implement/SKILL.md) (updated via migration proposals)
**Component:** stem-service
**Feature:** 0000010-http-api
**Owner:** stem-service
**Schema Version:** 1.0.0

> This is the authoritative schema definition for this component's data.

## Tables

### jobs

| Column | Type | Nullable | Default | Constraints |
|--------|------|----------|---------|------------|
| id | TEXT | no | none | PK. A UUID4 hex string |
| status | TEXT | no | `queued` | check: `queued`, `running`, `done`, or `failed` |
| input_path | TEXT | no | none | none |
| full_stems | INTEGER | no | 0 | check: 0 or 1 |
| options | TEXT | no | `{}` | A JSON object. Empty until step 7 |
| outputs | TEXT | yes | none | A JSON list of absolute paths. Set when the job is `done` |
| error | TEXT | yes | none | One line. Set when the job is `failed` |
| created_at | TEXT | no | none | UTC, ISO 8601 |
| started_at | TEXT | yes | none | UTC, ISO 8601. Set when the job is claimed |
| finished_at | TEXT | yes | none | UTC, ISO 8601. Set when the job ends |

**Indexes:**
- `jobs_status_created` on `(status, created_at)`, which `claim_next()` uses.

**Relationships:**
- None.

## Files

The API writes each upload to `{data_dir}/uploads/{random id}/{file name}`. `stem-service` owns the `uploads` folder. The worker writes stems to `{data_dir}/jobs/{job id}`. No schema change comes with this step.

## Invariants

- Only `JobStore` writes the table.
- A job is `queued`, `running`, `done`, or `failed`. `done` and `failed` are final.
- `claim_next()` returns the oldest `queued` job and sets it `running` in one transaction.
- `recover()` is the only call that moves a job from `running` back to `queued`.

## Migration History

| ID | Version | Description | Status | Destructive |
|----|---------|------------|--------|------------|
| M-001 | 1.0.0 | Create `jobs` and its index. The initiative chart approves this additive change | applied | no |
