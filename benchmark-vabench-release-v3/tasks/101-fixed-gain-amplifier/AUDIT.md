# Honest SOP Audit: Task 101 Fixed Gain Amplifier

## Scope

Task boundary is one standalone Verilog-A DUT artifact, `gain_amp_fixed.va`.
It is admitted as an L1 baseband signal-conditioning component: a fixed-gain
differential amplifier that can support composed measurement flows such as
`287-gain-extraction-flow`, but is evaluated independently from that flow.

## Four Standards

- Useful scenario: accepted. Fixed-gain differential amplification is a recognizable reusable AMS behavioral block.
- Reasonable task: accepted. The public prompt names only the target module, interface, gain parameter, positive polarity, and output common-mode invariant.
- Complete tests: pending fresh local recertification after the boundary split. Hidden and visible decks are no longer byte-identical and use different `ACTUAL_GAIN` values.
- Fair evaluation: accepted for EVAS audit shape. The checker is task-specific and checks requested gain, polarity, and common-mode rather than the enclosing gain-extraction flow.

## Checker And Evidence

- Checker id: `v3_101_fixed_gain_amplifier`
- Hidden bench: `test_hidden/tests/tb_gain_amp_fixed_ref.scs`
- Concrete negatives: `neg_001_zero`, `neg_002_unity_gain`, `neg_003_inverted_polarity`, `neg_004_ignores_gain_parameter`
- Fresh EVAS/Spectre recertification: pending after this manual boundary repair

## Remaining Risk

Do not mark final release certified until the updated gold and negative variants
have fresh EVAS evidence, and Spectre evidence if this task enters a paper-facing
dual-certified slice.
