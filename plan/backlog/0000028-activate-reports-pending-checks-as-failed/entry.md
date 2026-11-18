---
title: "Backlog Entry: 0000028 - Activate reports pending checks as failed"
summary: "Activate reports pending checks as failed, found by the retrospective of initiative 0000001."
status: "open"
priority: "medium"
theme: "initiative-tooling"
---
# Backlog Entry: 0000028 - Activate reports pending checks as failed

**Source feature:** 0000001-stem-separation-service

**Source phase:** I-E Delivery

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

`initiative-activate.mjs --yes` printed `Blocked: checks failed on PR #4` a few seconds after it raised the PR. The checks had not started, and both passed a minute later. A rerun resumed at the PR step and merged.

## Suggested Action

Make the script wait until `gh pr checks` lists a check before it watches, as the merge queue does.

**Observable condition:** activation in a repo with slow CI start merges its PR in one run.

## Why Deferred

The gap sits in the RAVINTIO pack, not in the product. The source is the retrospective `plan/retrospectives/0000001-stem-separation-service-initiative-2026-11-16.md`.
