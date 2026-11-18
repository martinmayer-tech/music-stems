---
title: "Backlog Entry: 0000020 - Add a URL normalisation note to the testing standards"
summary: "A path traversal test that sends a plain dot segment never reaches the route, because the HTTP client rewrites the URL first."
status: "open"
priority: "medium"
theme: "pipeline"
---
# Backlog Entry: 0000020 - Add a URL normalisation note to the testing standards

**Source feature:** 0000010-http-api

**Source phase:** P2

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

A test for path traversal that sends `..` in a URL does not test the route. The HTTP client removes the dot segment before it sends the request, so the test hits a different route. The RED run could not show the fault, because a missing route also answers with an error. `ravintio-zero/standards/testing-standards.md` has no note on either point.

## Suggested Action

Add a short note to `ravintio-zero/standards/testing-standards.md`. A traversal test sends the name in encoded form, such as `%2e%2e`. A negative test also needs a check that it fails for the stated reason in the RED run.

## Why Deferred

The change edits a pack standard, which lies outside the scope of the HTTP API step.

## Source retrospective

`plan/retrospectives/0000010-http-api-2026-11-16.md`. The postmortem is `plan/postmortems/2026-11-16-url-dot-segment-in-traversal-test.md`.
