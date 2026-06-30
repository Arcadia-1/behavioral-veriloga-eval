# Task 099 Audit

## Scope

Task boundary is one standalone Verilog-A DUT artifact, `dither_adder.va`.
It is admitted as an L1 support/component function: a reusable differential
dither injection block that can be used inside measurement flows such as
`287-gain-extraction-flow`, but is evaluated independently from that flow.

## Four Standards

- Useful scenario: accepted. Differential dither injection is a recognizable AMS support function for decorrelation, calibration, and measurement excitation.
- Reasonable task: accepted. The public prompt names only the target module, interface, polarity rule, dither amplitude parameter, and common-mode invariant.
- Complete tests: pass for the current reviewed slice. Private and visible decks
  are no longer byte-identical and exercise different `DITHER_AMP`/input
  trajectories.
- Fair evaluation: accepted for EVAS audit shape. The checker is task-specific and checks dither sign plus common-mode preservation, not the enclosing gain-extraction flow.

## Checker And Evidence

- Checker id: `v3_099_dither_adder`
- Private bench: `test_hidden/tests/tb_dither_adder_ref.scs`
- Concrete negatives: `neg_001_zero`, `neg_002_wrong_polarity`, `neg_003_common_mode_shift`, `neg_004_fixed_positive_dither`
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: private
  reference PASS and 4/4 private negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

AHDL lint evidence is not attached yet; do not mark `cadence_modeling_ready`
until lint/triage is recorded.
