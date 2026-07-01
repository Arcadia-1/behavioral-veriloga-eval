# behavioral-veriloga-eval

This repository holds the public vaBench / behavioral Verilog-A benchmark
source, EVAS/Spectre validation runners, schemas, examples, and compact public
evidence.

## Current Benchmark Entrypoint

The active task release is:

```text
benchmark-vabench-release-v3/
```

Use `benchmark-vabench-release-v3/tasks/` as the authoritative public task
root for new evaluation work. Tasks `001`-`300` are the original certified
full-300 surface; tasks `301`-`340` are Verilog-A language-semantics extension
candidates and tasks `341`-`360` are Verilog-AMS mixed-signal extension
candidates, and tasks `361` and above are noise/analysis extension candidates that must be certified separately before being included in full-suite
claims. The release-level indexes are:

- `benchmark-vabench-release-v3/TASKS.json`: canonical task metadata and target
  artifacts.
- `benchmark-vabench-release-v3/CHECKS.yaml`: canonical checker configuration.

Each v3 task is self-contained under `tasks/NNN-name/` with:

- `instruction.md`: agent-facing problem statement.
- `starter/`: files the agent edits.
- `test_visible/`: public smoke material.
- `test_hidden/`, `test_harness/`, `solution/`, `negative_variants/`:
  evaluator-side material.

Do not use old release roots as current evaluation inputs.

## Historical Surfaces

`benchmark-vabench-release-v1/` remains in the repository as the legacy
paper/evidence surface for the earlier vaBench release and website exports.
It is not the active task-authoring root for new v3 work.

`benchmark-vabench-release-v2/` has been retired. Its five candidate tasks were
absorbed into v3 as tasks `283` through `287`, and the v2 tree was removed from
the public repository so it cannot be mistaken for an active release.

## Public/Private Boundary

This public repository may contain benchmark tasks, prompts, gold/reference
artifacts, public runners, schemas, examples, documentation, and compact public
evidence.

Private execution state belongs outside this repository, including Vela
submission JSONL, process snippets, internal model IDs, Harbor image tags,
tokens, raw run logs, and cost/accounting reports.

## Repository Map

- `benchmark-vabench-release-v3/`: active v3 benchmark task release.
- `benchmark-vabench-release-v1/`: legacy vaBench release/evidence surface.
- `runners/`: reusable public evaluator and report-generation code.
- `schemas/`: public schemas.
- `examples/`: non-scored examples.
- `docs/`: stable public documentation and website data exports.
- `scripts/`: repository maintenance scripts.
- `tests/`: regression and policy checks.

Generated raw results, logs, scratch outputs, and private Vela state should not
be committed.

## Validation

Use EVAS as the fast local evaluator and debugger. Use Spectre as the final
judge for gold promotion and paper-facing parity claims.

For benchmark changes, prefer:

1. static/source integrity checks;
2. EVAS gold validation for changed tasks;
3. Spectre or dual EVAS/Spectre validation for promoted/paper-facing evidence.

For a quick repository sanity check:

```bash
python3 -m py_compile runners/simulate_evas.py
PYTHONPATH=runners python3 -m pytest -q tests/test_evas_output_cleanup.py
python3 -m pytest -q tests/test_task_count_filters.py
```
