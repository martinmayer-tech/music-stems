---
title: "Backlog Entry: 0000023 - Add audioread to the Docker image"
summary: "The image cannot separate audio, because audio-separator 0.48.0 imports audioread and librosa 1.0.1 no longer installs it."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000023 - Add audioread to the Docker image

**Source feature:** 0000016-docker-packaging

**Source phase:** P3

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

A job in the CPU image ends `failed` with `No module named 'audioread'`. `audio-separator` 0.48.0 imports `audioread` in `spec_utils.py`, and `librosa` 1.0.1 no longer installs it. The step 8 chart lists no `audioread` row, so the step added no library for it.

## Suggested Action

Approve `audioread` as a dependency. Then add it to the `separation` extra of `pyproject.toml`, so the image and a local install both get it. The agent checked the fix by hand. After `pip install audioread` in the running container, a job ended `done` with `vocals.wav` and `instrumental.wav`, and the models landed in the model volume.

**Observable condition:** a job uploaded to `docker compose up` ends `done` with a fresh image.

## Why Deferred

The chart's dependency rule stops a step that needs an unlisted library. The step kept its scope and reported the finding.
