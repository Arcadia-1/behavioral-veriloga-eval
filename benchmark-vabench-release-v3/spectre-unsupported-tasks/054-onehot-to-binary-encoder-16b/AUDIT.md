# Task 054 Audit

Task: `054-onehot-to-binary-encoder-16b`

Review: 2026-07 Testbench Utility Straggler Review

## Gate 1

- Admission label: `candidate_evas_only` for the archived package; support
  utility candidate if upstream later chooses to restore it.
- Function boundary: a 16-line one-hot to binary encoder with explicit valid
  output is a reusable AMS support helper for selection, readout, and encoded
  stimulus flows.
- Counting policy: current `upstream/main` keeps this row under
  `spectre-unsupported-tasks/` and excludes it from the default `TASKS.json` and
  `CHECKS.yaml` denominator. Do not count it or restore it from this category
  review alone.
- Overlap note: it is broader than task 056's decimal-only encoder shape, so if
  a future restore is considered, this row is the stronger representative
  one-hot encoder candidate.

## Gate 2

- Prompt status: updated to the mandatory vaBench v3 instruction headings and
  made explicit about module name, vector port order, one-hot validity rule,
  bit order, threshold, logic levels, transition parameter, and invalid-input
  behavior.
- Modeling status: `cadence_sim_pending` and `cadence_lint_pending` for this
  category PR. The archived Verilog-A assets need the separate Spectre legality
  and AHDL evidence chain before any restoration or readiness claim.
- Existing archived checks: representative one-hot and invalid cases plus
  concrete negative variants target the stated encoder behavior, but those
  checks are not default release evidence while the row remains archived.

Certification status: archived support/non-counted. Category review is complete;
Cadence modeling readiness is not claimed by this PR.
