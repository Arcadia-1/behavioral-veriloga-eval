# Repository Layout Policy

This repository should read as a public benchmark repository, not as private
Vela infrastructure or a raw experiment workspace.

## Active Public Surface

The active benchmark task root is:

```text
benchmark-vabench-release-v3/tasks/
```

New tasks, task-quality fixes, and current benchmark-facing documentation should
target `benchmark-vabench-release-v3/`.

`benchmark-vabench-release-v1/` is retained only as a legacy release/evidence
surface for older vaBench reports, website exports, and historical paper-facing
artifacts. Do not add new v3 tasks there.

`benchmark-vabench-release-v2/` is retired and should not be recreated. Its
five candidate tasks have been absorbed into v3.

The active benchmarkv4 release package lives at
`benchmark-vabench-release-v4/release/benchmarkv4-r45/`. The frozen r44 package
remains at `benchmark-vabench-release-v4/release/benchmarkv4/` only for
historical reproduction and immutable release verification. An r47 candidate
must remain explicitly selected until its certification artifacts and seal are
complete.

## Stable Top-Level Directories

Use these directories for durable public work:

- `benchmark-vabench-release-v3/` - active benchmark task release.
- `benchmark-vabench-release-v1/` - legacy release/evidence surface.
- `docs/` - stable public documentation, policies, and website data exports.
- `examples/` - runnable non-scored examples.
- `runners/` - reusable public benchmark and simulator harnesses.
- `schemas/` - public task/result schemas.
- `scripts/` - repository maintenance scripts.
- `skills/` - public reusable skill documentation for this repo.
- `tests/` - regression tests and policy checks.

## Private And Transient State

Do not commit:

- Vela submission records, process snippets, private model IDs, private result
  logs, tokens, Harbor image tags, or private cost/accounting reports.
- Raw waveform dumps, transient simulator output directories, ad hoc run logs,
  or scratch/generated workspaces.

Raw local outputs may exist under ignored local directories while debugging,
but public claims should be represented only by compact, intentionally reviewed
reports or task-local audit notes.

## Forbidden Root Patterns

Do not create new top-level directories matching these patterns:

- `benchmark-vabench-release-v2/`
- `generated-*`
- `generated/`
- `results-*`
- `results_*/`
- `runlogs/`
- `experiment-logs/`
- `refine-logs/`
- `scratch/`
- `tmp/`

## Adding Or Updating Tasks

For active v3 work, each task should remain self-contained under
`benchmark-vabench-release-v3/tasks/NNN-name/` and preserve the public/private
boundary:

- agent-visible: `instruction.md`, `starter/`, and `test_visible/`;
- evaluator-side: `solution/`, `test_hidden/`, `test_harness/`, and
  `negative_variants/`;
- tooling index: `task.toml`.

Do not add `meta.json` for v3 tasks unless the repository adopts a new
generator that requires it.

## Checks

Before committing layout or task-surface changes, run a relevant subset of:

```bash
git diff --check
python3 -m py_compile runners/simulate_evas.py
PYTHONPATH=runners python3 -m pytest -q tests/test_evas_output_cleanup.py
python3 -m pytest -q tests/test_task_count_filters.py
```
