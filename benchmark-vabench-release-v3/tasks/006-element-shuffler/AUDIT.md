# Task 006 Audit

Task: `006-element-shuffler`

Status: certified EVAS formal candidate.

## Four-Standard Review

- Useful scenario: pass. A deterministic one-hot element shuffler is a common calibration and DEM control primitive.
- Reasonable task: pass. The public prompt fixes the module name, port order, active-low reset, rising-clock update rule, voltage-domain output levels, and required non-monotonic sequence `out2,out0,out3,out1`.
- Complete tests: candidate. `test_visible/visible.scs` covers the first six active samples. `test_hidden/hidden.scs` covers the same public window plus a mid-run reset and a second post-reset sequence window.
- Fair evaluation: candidate. The hidden checker logic samples only public signals and checks requirements stated in `instruction.md`: one-hot output, exact sequence, and reset restart.

## Checker Contract

Trace signals: `clk`, `rst_n`, `out0`, `out1`, `out2`, `out3`.

At each sample time listed in `test_harness/checks.yaml`, classify an output as high when its voltage is greater than `0.45 V`. A passing waveform has exactly one high output and the active output name must match the expected sequence. Hidden samples additionally verify that asserting `rst_n` low restarts the sequence.

## Negative Coverage

- `neg_001_stuck_initial_state`: no clock advancement.
- `neg_002_skip_every_other_state`: advances by two states per clock.
- `neg_003_monotonic_output_order`: uses monotonic output mapping instead of the required permutation.
- `neg_004_forces_state_three`: forces a single state after every clock.
- `neg_005_out0_stuck_high`: violates the one-hot rotating sequence.

## Evidence

- File-level release-v3 structure prepared in this task directory only.
- Gold EVAS certification PASS under `v3_006_element_shuffler` with active sequence `2,0,3,1,2,0`.
- Concrete negative variants: 5/5 compile and fail with `FAIL_SIM_CORRECTNESS`.

## Remaining Risk

- Paper-facing certification still needs fresh EVAS/Spectre correlation or an explicit EVAS-only label.

Certification status: certified as an EVAS formal candidate on 2026-06-24.
