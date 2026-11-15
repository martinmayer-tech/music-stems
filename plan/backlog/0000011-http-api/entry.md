---
title: "Backlog Entry: 0000011 - HTTP API"
summary: "HTTP API for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000011 - HTTP API

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

No process outside Python can submit a job or fetch stems. A front end needs an API to call.

## Suggested Action

Add an HTTP API to `stem-service` with FastAPI. It accepts an upload and creates a job. It reports job status, lists jobs, and serves each stem file. It binds to `127.0.0.1` by default and has no login.

**Observable condition:** a client uploads a file, polls the job until `done`, and downloads each stem as a WAV file.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
