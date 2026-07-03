# Task 057 Audit

Task: `057-signed-magnitude-to-twos-complement-8b`

Review: 2026-07 Testbench Utility Straggler Review

## Gate 1

- Admission label: `candidate_evas_only` for the archived package; support
  utility candidate if upstream later chooses to restore it.
- Function boundary: an 8-bit sign-magnitude to two's-complement converter is a
  voltage-coded code-format helper for AMS readout, measurement, or control
  paths that exchange signed digital words.
- Counting policy: current `upstream/main` keeps this row under
  `spectre-unsupported-tasks/` and excludes it from the default `TASKS.json` and
  `CHECKS.yaml` denominator. Do not count it or restore it from this category
  review alone.
- Overlap note: the row is pure support logic by itself. It should not be used
  as a core AMS circuit-function claim unless a future category explicitly
  counts signed-code interface helpers.

## Gate 2

- Prompt status: updated to the mandatory vaBench v3 instruction headings and
  made explicit about module name, vector port order, magnitude bit order,
  output bit order, negative-zero behavior, threshold, logic levels, transition
  parameter, and signed-code observable behavior.
- Modeling status: `cadence_sim_pending` and `cadence_lint_pending` for this
  category PR. The archived Verilog-A assets need the separate Spectre legality
  and AHDL evidence chain before any restoration or readiness claim.
- Existing archived checks: positive, negative, zero, and concrete negative
  variants target the stated conversion behavior, but those checks are not
  default release evidence while the row remains archived.

Certification status: archived support/non-counted. Category review is complete;
Cadence modeling readiness is not claimed by this PR.
