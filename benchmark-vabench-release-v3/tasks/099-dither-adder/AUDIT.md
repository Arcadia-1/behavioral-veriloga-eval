# Honest SOP Audit: Task 099 Dither Adder

## Scope

Task boundary is one standalone Verilog-A DUT artifact, `dither_adder.va`.
It is admitted as an L1 support/component function: a reusable differential
dither injection block that can be used inside measurement flows such as
`287-gain-extraction-flow`, but is evaluated independently from that flow.

## Four Standards

- Useful scenario: accepted. Differential dither injection is a recognizable AMS support function for decorrelation, calibration, and measurement excitation.
- Reasonable task: accepted. The public prompt names only the target module, interface, polarity rule, dither amplitude parameter, and common-mode invariant.
- Complete tests: pending fresh local recertification after the boundary split. Hidden and visible decks are no longer byte-identical and exercise different `DITHER_AMP`/input trajectories.
- Fair evaluation: accepted for EVAS audit shape. The checker is task-specific and checks dither sign plus common-mode preservation, not the enclosing gain-extraction flow.

## Checker And Evidence

- Checker id: `v3_099_dither_adder`
- Hidden bench: `test_hidden/tests/tb_dither_adder_ref.scs`
- Concrete negatives: `neg_001_zero`, `neg_002_wrong_polarity`, `neg_003_common_mode_shift`, `neg_004_fixed_positive_dither`
- Fresh EVAS/Spectre recertification: pending after this manual boundary repair

## Remaining Risk

Do not mark final release certified until the updated gold and negative variants
have fresh EVAS evidence, and Spectre evidence if this task enters a paper-facing
dual-certified slice.
