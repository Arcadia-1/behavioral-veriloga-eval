# Repository Layout Policy

This repository should stay organized around the paper-facing mainline:
vaBench benchmark material and EVAS/Spectre parity evidence.

## Stable Top-Level Directories

Use these directories for durable work:

- `benchmark-vabench-release-v1/` - release benchmark definition, reports, evidence summaries, and promoted fixtures.
- `speed-optimization/` - EVAS/Spectre speed experiments, compact reports, plans, and speed-specific raw-result pointers.
- `conformance/` - focused EVAS/Spectre conformance regressions.
- `datasets/` - curated input datasets or manifests.
- `docs/` - audit notes, paper-facing summaries, archive manifests, and policies.
- `examples/` - runnable reference examples.
- `experiments/` - promoted experiment specs only; do not place raw run outputs here.
- `runners/` - reusable benchmark and simulator harnesses.
- `schemas/` - task and result schemas.
- `scripts/` - repository maintenance and orchestration scripts.
- `tables/` - compact table inputs or generated table summaries that are intentionally kept.
- `tasks/` - benchmark source tasks.
- `tests/` - regression tests and policy checks.

## Transient Directories

These directories may exist locally but should remain generated or ignored:

- `results/` - fresh local simulator output only.
- `logs/` - local logs.
- `literature/` - local paper-reading material.
- `.pytest_cache/` and `__pycache__/` - test/runtime caches.

Do not treat transient directories as the canonical source for paper claims.
Promote compact evidence into `benchmark-vabench-release-v1/reports/`,
`speed-optimization/reports/`, or `docs/` instead.

## Forbidden Root Patterns

Do not create new top-level directories matching these patterns:

- `generated-*`
- `generated/`
- `results-*`
- `results_*/`
- `runlogs/`
- `experiment-logs/`
- `refine-logs/`
- `scratch/`
- `tmp/`

Raw experiment output belongs under `results/<date-or-run-id>/` while it is
active. If it needs to survive as provenance, compress it outside the repo under
`/Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/`
and add a manifest under `docs/`.

## Speed Work

Speed-related work should stay under `speed-optimization/`:

- plans and claim notes: `speed-optimization/`
- compact analysis reports: `speed-optimization/reports/`
- scripts or reusable harness changes: `runners/` or `scripts/`
- raw simulator output: `results/<run-id>/` while active, then archive plus manifest

## Checks

Run the layout policy check before committing cleanup or experiment-structure
changes:

```text
python3 scripts/check_repo_layout.py
```
