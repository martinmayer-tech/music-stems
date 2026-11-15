---
title: "Backlog Entry: 0000007 - Command-line interface"
summary: "Command-line interface for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000007 - Command-line interface

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

A user can reach the separation core only from Python code. The guide calls for a scriptable tool.

## Suggested Action

Add a `stems` command to `stem-core`. `stems split {file}` runs pass 1, and `--full-stems` adds pass 2. `stems env` reports the Python version, FFmpeg, and the device. `stems models` lists the supported models.

**Observable condition:** `stems split mix.wav --output-dir out` exits 0 and prints one output path per line. A missing input file exits non-zero with one error line.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
