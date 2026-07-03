# Two-Gate SOP Audit: Task 124 Comparator Offset Detect

## Scope

Task 124 samples comparator decisions on falling clock edges, updates a signed
offset estimate with a step that halves after every decision, and drives a
differential stimulus pair around a supply-derived common mode.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: human review confirmed that task 124 should not be counted
  separately because task `203-comparator-offset-driver` keeps the same
  every-update halving algorithm with a clearer comparator-offset driver
  boundary.
- Function boundary: binary-search style comparator-offset stimulus generation.
- Rewrite path: keep only if rewritten into a distinct detector role, such as a
  calibration-completion detector, signed offset estimate output, or comparator
  polarity monitor that is not already represented by task 203.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself, but not a
  separate counted function under the strict duplicate policy.
- Prompt hygiene: current public prompt states the falling-clock decision rule,
  detector polarity, per-decision step halving, differential output behavior,
  common-mode behavior, and voltage-only constraints.
- Checker coverage: `v3_comp_os_detect` verifies the public differential
  sequence and common-mode behavior, including polarity and per-decision step
  halving.

## Human Confirmation

The reviewer confirmed that offset-driver rows should be counted by distinct
search algorithm or circuit role, not by source name, default step size, or
port naming.
