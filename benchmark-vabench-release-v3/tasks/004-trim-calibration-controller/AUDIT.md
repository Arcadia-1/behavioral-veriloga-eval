# Task 004 Audit

Task: `004-trim-calibration-controller`

Status: formal candidate for EVAS-based release-v3 evaluation.

## Four-Standard Review

- Useful scenario: pass. A voltage-domain trim accumulator is a common calibration-control primitive for behavioral data-converter and mixed-signal models.
- Reasonable task: pass. The public prompt fixes module name, scalar port order, voltage logic threshold, reset value, step size, clamp range, rising-edge update rule, and voltage-only Verilog-A implementation constraints.
- Complete tests: candidate pass. The visible testbench checks syntax, reset, and basic increment/decrement behavior. Private validation drives a deterministic PWL clock sequence that covers synchronous reset, repeated increments, repeated decrements through midscale to the lower clamp, and recovery after direction reversal.
- Fair evaluation: pass. Private validation checks stricter stimulus points for requirements stated in `instruction.md`; the visible testbench does not expose the full clamp and recovery sequence.

## Checker Contract

Trace signals: `time`, `clk`, `rst`, `err`, `trim`.

Scoring logic:

- Detect rising `clk` crossings at 0.45 V.
- Sample `rst`, `err`, and settled `trim` after each rising edge.
- On an edge with `rst > 0.45 V`, expected trim is 0.45 V.
- Otherwise update expected trim by +0.06 V when `err > 0.45 V`, by -0.06 V when `err <= 0.45 V`, then clamp to [0.05 V, 0.85 V].
- Require `trim` to match the expected sequence within 15 mV and remain inside the clamp range between samples.

## Evidence

- Public visible SCS: `test_visible/visible.scs`.
- Private validation SCS: validation deck under the task harness.
- Golden reference: `solution/cdac_calibration.va`.
- Concrete negative variants: 5 cases under `negative_variants/neg_*`, described by `negative_variants/manifest.json`.

Negative coverage:

- `neg_001_stuck_midscale`: rejects implementations that reset correctly but never calibrate.
- `neg_002_inverted_error_direction`: rejects reversed feedback polarity.
- `neg_003_wrong_step_size`: rejects plausible accumulators with the wrong 50 mV step.
- `neg_004_wrong_reset_level`: rejects reset to the wrong nominal trim voltage.
- `neg_005_missing_lower_clamp`: rejects missing lower saturation while preserving other behavior.

## Remaining Risk

- EVAS gold PASS under `v3_004_trim_calibration_controller`.
- 5/5 concrete negatives compile and fail with `FAIL_SIM_CORRECTNESS`.
- Paper-facing certification still needs fresh EVAS/Spectre correlation or an explicit EVAS-only label.

Certification status: certified as an EVAS formal candidate on 2026-06-24.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `independent_l1_ready`.
- Rationale: voltage-domain calibration accumulator with reset, signed error update, clamp range, and recovery behavior.
- Counting recommendation: retain as calibration/control L1.
