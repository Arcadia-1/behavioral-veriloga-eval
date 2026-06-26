# v3 Task Quality Audit

This file records durable public audit status for the v3 task set. It is not a
private Vela run log.

## Source-Series Audit

As of 2026-06-26, v3 contains 185 `source-*` tasks. The initial source-series
audit found that most imported source tasks had only one concrete negative
variant, usually `neg_001_zero`. That is not strong enough for the final
benchmark standard because it proves little beyond "not all outputs are zero."

The source-series repair is being done in batches. Each repaired batch should
meet these minimum conditions:

- public task contract and implementation boundary are clear;
- gold solution passes the EVAS checker through the normal task id path;
- each task has multiple concrete behavior negatives, not only all-zero;
- every new negative compiles and fails behavioral correctness rather than
  failing by syntax or missing files.

## Completed Pilot: 288-300

Tasks `288-source-absolute-value` through
`300-source-pfd-active-low-reset` were used as the first source-series repair
pilot.

Changes made:

- each task now has four negative variants: the original `neg_001_zero` plus
  three targeted behavior mutations;
- `runners/simulate_evas.py` registers checker aliases for the task ids
  `v3_288_source_*` through `v3_300_source_*`, so the normal `task.toml` id path
  reaches the checker without requiring a manual `--checker-task-id` override.

EVAS 0.4.5 local verification:

- 13/13 gold solutions PASS;
- 52/52 concrete negative variants fail behavioral correctness;
- no negative variant passed unexpectedly.
