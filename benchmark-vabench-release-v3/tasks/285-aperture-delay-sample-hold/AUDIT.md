# Two-Gate SOP Audit: Task 285 Aperture Delay Sample Hold

## Scope

Task 285 is a v3 absorption of the same aperture-delay sample/track-and-hold
function covered by task 081. It preserves a package boundary for the imported
v2 row, but its target artifact, gold behavior, checker, and hidden stimulus
overlap with 081.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: keep 285 only as a non-counted duplicate/migration
  artifact unless it is rewritten into a distinct function or artifact role.
- Duplicate evidence: 081 and 285 are both DUT rows, target
  `sample_hold_aperture_ref.va`, share the same gold implementation, and use
  the same aperture-delay behavior checker.
- Independent value: current 285 assets are useful as a regression/migration
  fixture, but not as a second independent L1 circuit-function benchmark.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_lint_pending` for the artifact itself;
  non-counted for benchmark coverage.
- Prompt hygiene: prompt uses the current task title and public parameter
  contract rather than hidden evaluator or migration-path wording.
- Gold quality: gold is Spectre-compatible and passes the hidden aperture
  behavior check.
- Negative fixture repair: `neg_001_no_aperture_delay` was rewritten from a
  Spectre-illegal one-line port-declaration style into Spectre-compatible
  ANSI-style Verilog-A. The negative now compiles and fails behavioral
  correctness instead of failing AHDL read-in.

## Evidence

- EVAS hidden gold smoke: PASS.
- EVAS hidden negative `neg_001_no_aperture_delay`: FAIL_SIM_CORRECTNESS.
- Spectre hidden gold: PASS.
- Spectre hidden negative `neg_001_no_aperture_delay`: NEGATIVE_REJECTED.
- Negative failure is behavioral, not syntax/setup.
