---
title: "Backlog Entry: 0000027 - Resume detection ignores the Applies when line"
summary: "Resume detection ignores the Applies when line, found by the retrospective of initiative 0000001."
status: "open"
priority: "medium"
theme: "initiative-tooling"
---
# Backlog Entry: 0000027 - Resume detection ignores the Applies when line

**Source feature:** 0000001-stem-separation-service

**Source phase:** I-E Delivery

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

Resume detection listed migrations 0007 and 0009 in every step. It reads the `Detect:` line only, so a folder that exists raises a finding. The `Applies when:` condition of both migrations is false in this repo. Each step logged `Migration pending:` lines that needed no answer, as line 38 of each archived build log shows.

## Suggested Action

Record a `not applicable` row in `plan/state/migrations.md` when a coordinator or a step finds the condition false. Resume detection then skips the migration.

**Observable condition:** a step in this repo logs no `Migration pending:` line for migration 0007 or 0009.

## Why Deferred

The gap sits in the RAVINTIO pack, not in the product. The source is the retrospective `plan/retrospectives/0000001-stem-separation-service-initiative-2026-11-16.md`.
