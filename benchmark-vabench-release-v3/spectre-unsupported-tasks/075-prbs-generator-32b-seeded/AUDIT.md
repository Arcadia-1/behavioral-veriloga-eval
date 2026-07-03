# Task 075 Audit

Task: `075-prbs-generator-32b-seeded`

Review: 2026-07 Testbench Utility Straggler Review

## Gate 1

- Admission label: `candidate_evas_only` for the archived package; support
  source candidate if upstream later chooses to restore it.
- Function boundary: a seeded 32-bit PRBS/LFSR voltage-coded source is a
  reusable AMS support generator for converter, link, calibration, and
  measurement stimulus flows.
- Counting policy: current `upstream/main` keeps this row under
  `spectre-unsupported-tasks/` and excludes it from the default `TASKS.json` and
  `CHECKS.yaml` denominator. Do not count it or restore it from this category
  review alone.
- Overlap note: unlike the combinational helpers in 052-057, this row has
  sequential source behavior with reset, seed load, and deterministic
  progression. It is still support/source coverage rather than a full L2 flow.

## Gate 2

- Prompt status: updated to the mandatory vaBench v3 instruction headings and
  made explicit about module name, vector port direction, reset state, seed load
  semantics, all-zero seed fallback, LFSR taps, shift direction, threshold,
  logic levels, transition parameter, and clock event behavior.
- Modeling status: `cadence_sim_pending` and `cadence_lint_pending` for this
  category PR. The archived Verilog-A assets need the separate Spectre legality
  and AHDL evidence chain before any restoration or readiness claim.
- Existing archived checks: reset, seed loading, progression, and concrete
  negative variants target the stated source behavior, but those checks are not
  default release evidence while the row remains archived.

Certification status: archived support/non-counted. Category review is complete;
Cadence modeling readiness is not claimed by this PR.
