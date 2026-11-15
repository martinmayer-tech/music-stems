# RAVINTIO - Repository Structure

> The canonical layout for a RAVINTIO-managed repository. Three top-level folders, three concerns.

---

## The Three Folders

```
repo/
- ravintio-zero/        - Â The pack (skills, templates, schemas, standards)
-                                 Drop this in. Don't modify it per-project.
-
- plan/                       - Â The specifications (organized by feature)
-                                 Plans, briefs, specs, ADRs, risk, scope, glossary.
-                                 Everything that describes WHAT to build and WHY.
-
- src/                        - Â The code (organized by component)
                                  Implementation, tests, config, manifests.
                                  Everything that IS the built thing.
```

---

## `ravintio-zero/` - The pack

This folder is RAVINTIO Zero itself. It is the same across every project. You do not modify it per-feature - you update it when RAVINTIO Zero evolves.

```
ravintio-zero/
- skills/           - Â Agent instructions (orchestrator + phase skills)
- templates/        - Â File format templates for every artifact
- schemas/          - Â JSON Schema validation definitions
- standards/        - Â Code quality standards
- spec/             - Â This file - the canonical structure definition
```

---

## `plan/` - The Plan/Specifications

Organized by feature. Each feature gets a subfolder. This is where humans write briefs and agents write specs. No code lives here.

```
plan/
- {feature-id}/
    - feature-brief.md          - Â Human input (start here)
    - design.md                 - Â Validated plan (orchestrator output)
    - pipeline-run.md              - Â Audit trail (per run)
    - pipeline-run-phase-2.md      - Â Phase 2 audit (if phased)
    -
    - design-requirements.md               - Â Functional & non-functional requirements
    - design-spec-phase-2.md       - Â Phase 2 spec (if phased)
    - openapi-spec.yaml            - Â API contract
    - scope.md                     - Â In / Out / Deferred
    - risk-register.md             - Â Risk items with likelihood & impact
    - domain-glossary.md           - Â Ubiquitous language
    - security-report.md           - Â Security review findings
    - quirks.md                    - Â Quirks and workarounds
    - recommendations.md           - Â Improvement suggestions
    -
    - adr/
        - ADR-001-{title}.md       - Â Architecture decision records
        - ADR-002-{title}.md
        - ...
```

### Path Rules - plan/

1. **Feature ID** follows the format `{0000000}-{kebab-case-name}` - a 7-digit zero-padded number prefix for chronological ordering, followed by a human-chosen kebab-case name.
2. **No nesting** - specs, ADRs, and supporting docs are flat within the feature folder. One level of subfolders only (adr/).
3. **No code** - nothing executable lives in `plan/`. If it runs, it belongs in `src/`.
4. **Phased features** append the phase number: `design-spec-phase-2.md`, `pipeline-run-phase-2.md`. Each phase updates the one `design.md` and never duplicates it.
5. **ADRs** take sequential numbers. Never renumber. Superseded ADRs stay with `status: superseded`.

---

## `src/` - The Code

Organized by component. Each component is a subfolder at the top level of `src/`. The component manifest lives with the code, not with the plan.

```
src/
- {component-id}/
    - component.yml               - Â Component manifest (from template)
    - package.json                  - Â (or equivalent for the stack)
    -
    - src/                          - Â Implementation (structure varies by stack)
    -   - ...
    -
    - tests/                        - Â Tests
    -   - ...
    -
    - docs/
        - data-contract.md          - Â Schema ownership & invariants
        - migrations/
            - proposed-{desc}.md    - Â Migration proposals
```

### Path Rules - src/

1. **Component ID** is kebab-case, matches the `id` in `component.yml`.
2. **component.yml is mandatory** - every component has one. Read it before any work. Update it after every build.
3. **Component-specific docs** live with the component at `src/{component-id}/docs/`. These describe the component's data contract, migrations, and technical specifics.
4. **Feature-level docs** live in `plan/`. The component's `component.yml` references the feature via the `feature` field.
5. **Existing components** that predate RAVINTIO need a `component.yml` at their root.

---

## How the Three Folders Connect

```
plan/current/design.md
    - lists component IDs - â€™ src/{component-id}/component.yml
                                    - references feature - â€™ plan/

plan/current/design-requirements.md
    - functional requirements - â€™ implemented in - â€™ src/{component-id}/src/

plan/current/adr/ADR-001-*.md
    - decisions - â€™ followed by - â€™ src/{component-id}/src/

plan/current/openapi-spec.yaml
    - API contract - â€™ implemented in - â€™ src/{component-id}/src/
```

The relationship is bidirectional:
- `design.md` lists all component IDs
- Each `component.yml` references its feature ID
- The plan describes WHAT. The code IS the WHAT

---

## Retrofit - Adding RAVINTIO to an Existing Repo

If the repo already has code:

1. Drop `ravintio-zero/` into the repo root
2. Create `plan/` for the first feature
3. Move existing components under `src/` (or leave them if they're already there)
4. Add a `component.yml` to each existing component
5. The orchestrator's retrofit mode will read the codebase and infer the existing architecture

---

*Templates for each file are in [ravintio-zero/templates/](../ravintio-zero/templates/). Skills reference these paths.*
