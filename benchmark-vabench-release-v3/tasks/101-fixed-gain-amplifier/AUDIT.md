# Task 101 Audit

## Scope

Task boundary is one standalone Verilog-A DUT artifact, `gain_amp_fixed.va`.
It is admitted as an L1 baseband signal-conditioning component: a fixed-gain
differential amplifier that can support composed measurement flows such as
`287-gain-extraction-flow`, but is evaluated independently from that flow.

## Four Standards

- Useful scenario: accepted. Fixed-gain differential amplification is a recognizable reusable AMS behavioral block.
- Reasonable task: accepted. The public prompt names only the target module, interface, gain parameter, positive polarity, and output common-mode invariant.
- Complete tests: pass for the current reviewed slice. Private and visible decks
  are no longer byte-identical and use different `ACTUAL_GAIN` values.
- Fair evaluation: accepted for EVAS audit shape. The checker is task-specific and checks requested gain, polarity, and common-mode rather than the enclosing gain-extraction flow.

## Checker And Evidence

- Checker id: `v3_101_fixed_gain_amplifier`
- Private bench: `test_hidden/tests/tb_gain_amp_fixed_ref.scs`
- Concrete negatives: `neg_001_zero`, `neg_002_unity_gain`, `neg_003_inverted_polarity`, `neg_004_ignores_gain_parameter`
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: private
  reference PASS and 4/4 private negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

AHDL lint evidence is not attached yet; do not mark `cadence_modeling_ready`
until lint/triage is recorded.
