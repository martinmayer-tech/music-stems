---
title: "Backlog Entry: 0000015 - Model choice and ensemble options"
summary: "Model choice and ensemble options for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000015 - Model choice and ensemble options

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

Every job uses the two default models. Sections 8 and 9 of the guide list other models and ensembles that trade speed for quality.

## Suggested Action

Let a caller pick the pass 2 model from `htdemucs_ft.yaml`, `htdemucs_6s.yaml`, and `htdemucs.yaml`. Let a caller pick an ensemble preset for pass 1 and a single stem to write. Expose the options in `split()`, the `stems` command, the API, and the page. Reject any model outside the allowlist.

**Observable condition:** a job with `htdemucs_6s.yaml` returns guitar and piano stems, and a job that names an unlisted model fails with a clear error before any model loads.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
