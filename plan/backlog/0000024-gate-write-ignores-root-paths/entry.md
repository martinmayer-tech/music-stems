---
title: "Backlog Entry: 0000024 - Make gate-write accept a root file in the component paths"
summary: "The gate-write hook skips a component path with no slash, so a root file such as Dockerfile is never covered."
status: "open"
priority: "low"
theme: "pipeline"
---
# Backlog Entry: 0000024 - Make gate-write accept a root file in the component paths

**Source feature:** 0000016-docker-packaging

**Source phase:** P2

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

`extractComponentPaths` in `gate-write.mjs` keeps only entries that hold a `/`. A design that lists `Dockerfile` or `compose.yaml` under `## Component Paths` never covers those files, and the hook blocks the write. Step 8 listed `./Dockerfile` as a workaround.

## Suggested Action

Accept an entry with no slash when it names a file at the repo root. Add a test in `ravintio-zero/tests/`.

**Observable condition:** a design that lists `Dockerfile` lets the hook allow a write to `Dockerfile`.

## Why Deferred

The change edits a pack hook, which lies outside the scope of the Docker step.
