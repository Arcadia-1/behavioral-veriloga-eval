# Task 056 Audit

Task: `056-decimal-digit-to-bcd-encoder`

Review: 2026-07 Testbench Utility Straggler Review

## Gate 1

- Admission label: `valid_variant_needs_counting_policy` for any future
  restoration; archived/non-counted in the current release package.
- Function boundary: a decimal one-hot digit to BCD encoder is a recognizable
  support helper for display/readout or constrained stimulus paths.
- Counting policy: current `upstream/main` keeps this row under
  `spectre-unsupported-tasks/` and excludes it from the default `TASKS.json` and
  `CHECKS.yaml` denominator. Do not count it or restore it from this category
  review alone.
- Overlap note: this is a narrower ten-line specialization of task 054's
  one-hot-to-binary encoding pattern. Keep it non-counted unless upstream wants
  a BCD-specific support row for a future display/readout subcategory.

## Gate 2

- Prompt status: updated to the mandatory vaBench v3 instruction headings and
  made explicit about module name, vector port order, decimal digit mapping,
  BCD bit order, exact-one validity rule, threshold, logic levels, transition
  parameter, and invalid-input behavior.
- Modeling status: `cadence_sim_pending` and `cadence_lint_pending` for this
  category PR. The archived Verilog-A assets need the separate Spectre legality
  and AHDL evidence chain before any restoration or readiness claim.
- Existing archived checks: digit cases, invalid cases, and concrete negative
  variants target the stated encoder behavior, but those checks are not default
  release evidence while the row remains archived.

Certification status: archived support/non-counted. Category review is complete;
Cadence modeling readiness is not claimed by this PR.
