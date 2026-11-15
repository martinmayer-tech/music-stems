---
title: "Backlog Entry: 0000005 - Two-pass separation core"
summary: "Two-pass separation core for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000005 - Two-pass separation core

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

No code wraps `audio-separator`. Sections 3 and 7 of `open-source-stem-separation-guide.md` describe a two-pass pipeline that exists only as a sketch.

## Suggested Action

Build a `stem-core` component with a `split()` function. Pass 1 runs `model_bs_roformer_ep_317_sdr_12.9755.ckpt` and writes vocals and instrumental. Pass 2 is optional and runs `htdemucs_ft.yaml` on the instrumental. Pin `audio-separator` to one exact version, set WAV output, and read the model folder from `STEMS_MODEL_DIR`. Return absolute paths.

**Observable condition:** `split(mix, out)` returns 2 existing WAV paths, and `split(mix, out, full_stems=True)` returns 5.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
