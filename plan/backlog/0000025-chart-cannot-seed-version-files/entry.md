---
title: "Backlog Entry: 0000025 - Chart cannot seed the version files"
summary: "Chart cannot seed the version files, found by the retrospective of initiative 0000001."
status: "open"
priority: "medium"
theme: "initiative-tooling"
---
# Backlog Entry: 0000025 - Chart cannot seed the version files

**Source feature:** 0000001-stem-separation-service

**Source phase:** I-E Delivery

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

The merge queue needs `docs/about.md` and `product.yml` on the initiative branch before step 1 merges. It also reads `ravintio-zero/version-files.txt`, which lists `ravintio-zero/component.yml`, the pack's own version file. In a new consumer repo, Chart had to add both product files and cut the list. `gate-write` blocked the coordinator's writes to `product.yml` and `ravintio-zero/version-files.txt`, because no confirmed design exists at Chart. The human had to approve a direct copy.

## Suggested Action

Ship a consumer version file list that names the product files only. Let Activate create `docs/about.md` and `product.yml` at `0.0.0` when they are missing.

**Observable condition:** a new consumer repo activates an initiative and merges step 1 with no manual file copy.

## Why Deferred

The gap sits in the RAVINTIO pack, not in the product. The source is the retrospective `plan/retrospectives/0000001-stem-separation-service-initiative-2026-11-16.md`.
