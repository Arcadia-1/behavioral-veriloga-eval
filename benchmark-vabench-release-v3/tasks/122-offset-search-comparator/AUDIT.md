# Two-Gate SOP Audit: Task 122 Offset Search Comparator

## Scope

Task 122 is a comparator-offset stimulus helper. It updates a differential
stimulus pair on falling clock edges and halves its search step only when the
observed comparator polarity changes.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: human review confirmed that task 122 should not be a
  separate counted benchmark because task `208-offset-bisection-driver` exposes
  the same polarity-change bisection algorithm with a clearer public common-mode
  input and comparator-driver role.
- Function boundary: comparator-offset bisection stimulus generation.
- Rewrite path: keep only if rewritten into a distinct characterization helper,
  such as a bounded search with done/valid output, programmable step schedule,
  or explicit offset-estimate readout not covered by task 208.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself, but not a
  separate counted function under the strict duplicate policy.
- Prompt hygiene: repaired to the current public-prompt format with interface,
  parameters, update rule, common-mode behavior, and modeling constraints.
- Checker coverage: `v3_offset_search_comparator` verifies falling-edge
  updates, decision polarity, step halving on polarity changes, and symmetric
  differential output behavior.

## Human Confirmation

The reviewer confirmed that offset-search helper rows should be deduplicated by
algorithmic behavior, not by legacy import naming or port naming.
