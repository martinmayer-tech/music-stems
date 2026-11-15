---
title: "Backlog Entry: 0000013 - Web front end"
summary: "Web front end for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000013 - Web front end

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

The API has no user interface. The goal is a self-hosted replacement for a hosted web tool.

## Suggested Action

Add a `stem-web` component of plain HTML, CSS, and JavaScript that the API serves. The page uploads a file, offers the full stems option, and shows job progress. It plays each stem and offers a download link for each.

**Observable condition:** the API root returns the page, and the page shows one player and one download link per stem for a finished job.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
