# Two-Gate SOP Audit: Task 203 Comparator Offset Binary Driver

## Scope

Task 203 is a comparator-offset stimulus driver. On falling clock edges, it
updates a differential input pair around a fixed common-mode center according
to the previous comparator decision and halves the search step each update.

This is a reusable support component for comparator offset characterization,
not a comparator decision core.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready` as a support-style L1 component.
- Counting decision: human review confirmed that task 203 and task 208 should
  both be retained because they implement different comparator-offset search
  algorithms. Task 203 halves the search step after every update, while task
  208 halves only when comparator polarity changes.
- Function boundary: binary-search style differential stimulus generation for
  comparator-offset search.
- Checker alignment: the checker verifies falling-edge updates, step halving,
  decision polarity, and symmetric differential outputs.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself after
  prompt/schema repair and current comparator-batch EVAS/Spectre validation.
- Prompt hygiene: the prompt now states the public module, ports, parameters,
  update rule, and constraints without source-import or hidden-evaluator
  wording.
- Metadata repair: release-level `CHECKS.yaml` now includes a current
  `sim_correct:` block, so default verification exercises the row.
- Counting risk: task 124 is the duplicate/rewrite candidate for this
  every-update halving algorithm; task 203 is the clearer retained
  representative.

## Evidence

- EVAS hidden gold: PASS; the behavior-derived checker reports six checked
  update edges with zero differential and common-mode error.
- EVAS negatives: 4/4 behavioral rejections covering zero output, missing step
  halving, inverted update direction, and full-differential scaling.
- Spectre hidden gold: PASS with no task-level warnings or errors in the
  result JSON.
- Spectre negatives: 4/4 `NEGATIVE_REJECTED` on the hidden deck.

## Human Confirmation

The reviewer confirmed the general rule that support components can be valid
benchmarks when their reusable circuit role is explicit, but duplicate counting
should be strict and based on function rather than parameter/name differences.
