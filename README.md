# Robust TDD Skills

Intent: keep closely related TDD, audit, and code-quality monitoring skills together in one umbrella repository while preserving each skill as an independent repository.
Updated: 2026-07-01
Commit: pending local change from c3baf2b

## Overview

This repository groups related skills that are commonly used together:

- `fast-multi-agent-tdd/`: strict Red-Green-Refactor workflow orchestration with monitor discipline
- `review-with-multi-debate/`: structured audit workflow for phase claims and artifacts
- `code-smell-monitor/`: scoped objective code-quality feedback for repositories

The top-level repository exists to make the skill set easier to clone, inspect, and manage as one unit. The child skills remain independent repositories and are tracked here as git submodules.

## Repository Layout

```text
robust-tdd-skills/
  code-smell-monitor/
  fast-multi-agent-tdd/
  review-with-multi-debate/
```

## Git Model

- The umbrella repo tracks only the parent structure and submodule pointers.
- Each child skill keeps its own git history, remote, and release cadence.
- Changes inside a child skill must be committed in that child repo first.
- The umbrella repo should then commit the updated submodule pointer.
- `review-with-multi-debate` tracks upstream `main` through `.gitmodules`.
- `.github/workflows/sync-review-with-multi-debate.yml` runs hourly and on manual dispatch to update and commit the `review-with-multi-debate` pointer when upstream `main` moves.

Submodules are still exact commit pins. The workflow keeps the pin current; git does not make a submodule float automatically inside an already committed parent revision.

## Clone And Update

Clone with submodules:

```bash
git clone --recurse-submodules https://github.com/linmou/robust-tdd-skills.git
```

If already cloned:

```bash
git submodule update --init --recursive
```

To pull the latest child skill changes after they are pushed upstream:

```bash
git submodule update --remote --merge
```

To update only `review-with-multi-debate` locally:

```bash
scripts/sync_review_with_multi_debate_submodule.sh
```

## Skill Locations

- `code-smell-monitor` upstream: `https://github.com/linmou/code-smell-monitor.git`
- `fast-multi-agent-tdd` upstream: `https://github.com/linmou/fast-multi-agent-tdd.git`
- `review-with-multi-debate` upstream: `https://github.com/linmou/review-with-multi-debate.git`

## When To Use This Repo

Use this repository when you want one parent checkout for the full TDD-plus-audit workflow without collapsing the skills into one mixed codebase.
