---
title: "Backlog Entry: 0000017 - Docker image and compose file"
summary: "Docker image and compose file for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000017 - Docker image and compose file

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

Running the service needs a manual Python and FFmpeg install. A container without a volume downloads every model again.

## Suggested Action

Add a Dockerfile with Python 3.12 and FFmpeg, and a compose file. The compose file mounts one volume for models and one for job data. The image installs the CPU extra by default, and a build argument selects the GPU extra.

**Observable condition:** `docker compose up` serves the page on a local port, and a restart keeps the downloaded models and the finished jobs.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
