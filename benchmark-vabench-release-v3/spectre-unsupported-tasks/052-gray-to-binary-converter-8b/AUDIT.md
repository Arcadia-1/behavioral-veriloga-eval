# Task 052 Audit

Task: `052-gray-to-binary-converter-8b`

Review: 2026-07 Testbench Utility Straggler Review

## Gate 1

- Admission label: `candidate_evas_only` for the archived package; support
  utility candidate if upstream later chooses to restore it.
- Function boundary: an 8-bit Gray-to-binary voltage-coded bus converter is a
  reusable AMS support helper for converter, encoder, and measurement flows.
- Counting policy: current `upstream/main` keeps this row under
  `spectre-unsupported-tasks/` and excludes it from the default `TASKS.json` and
  `CHECKS.yaml` denominator. Do not count it or restore it from this category
  review alone.
- Overlap note: this is distinct from active thermometer-code converter rows,
  but it remains support utility coverage rather than a core analog circuit
  function by itself.

## Gate 2

- Prompt status: updated to the mandatory vaBench v3 instruction headings and
  made explicit about module name, vector port order, bit order, threshold,
  logic levels, transition parameter, and observable Gray-to-binary behavior.
- Modeling status: `cadence_sim_pending` and `cadence_lint_pending` for this
  category PR. The archived Verilog-A assets need the separate Spectre legality
  and AHDL evidence chain before any restoration or readiness claim.
- Existing archived checks: representative code vectors and concrete negative
  variants target the stated conversion behavior, but those checks are not
  default release evidence while the row remains archived.

Certification status: archived support/non-counted. Category review is complete;
Cadence modeling readiness is not claimed by this PR.
