---
title: "Backlog Entry: 0000026 - Pack suite cost in a consumer repo"
summary: "Pack suite cost in a consumer repo, found by the retrospective of initiative 0000001."
status: "open"
priority: "medium"
theme: "initiative-tooling"
---
# Backlog Entry: 0000026 - Pack suite cost in a consumer repo

**Source feature:** 0000001-stem-separation-service

**Source phase:** I-E Delivery

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

Each step ran the full pack suite in a clean clone two or three times. Each run took 20 to 30 minutes and showed 57 to 59 inherited failures. The suite tests the pack, not this product, so the wait bought no product signal. See the `## Inherited failures` section of each step build report in `plan/_archive/`.

## Suggested Action

Give a consumer repo a suite that runs the product tests and the plan format checks only. Keep the pack's own tests in the pack repo.

**Observable condition:** a step in this repo finishes its full suite run in under 5 minutes with 0 inherited failures.

## Why Deferred

The gap sits in the RAVINTIO pack, not in the product. The source is the retrospective `plan/retrospectives/0000001-stem-separation-service-initiative-2026-11-16.md`.
