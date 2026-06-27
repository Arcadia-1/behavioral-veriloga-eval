# Task 006 Audit

Task: `006-element-shuffler`

Status: Gate 1 accepted formal candidate with reset-restart checker coverage.
Gate 2 Cadence status: `cadence_lint_pending`.

## Four-Standard Review

- Useful scenario: pass. A deterministic one-hot element shuffler is a common calibration and DEM control primitive.
- Reasonable task: pass. The public prompt fixes the module name, port order, active-low reset, rising-clock update rule, voltage-domain output levels, and required non-monotonic sequence `out2,out0,out3,out1`.
- Complete tests: candidate. `test_visible/visible.scs` covers the first six active samples. `test_hidden/hidden.scs` covers the same public window plus a mid-run reset and a second post-reset sequence window.
- Fair evaluation: candidate. The checker samples only public signals and checks requirements stated in `instruction.md`: one-hot output, exact sequence, released reset at sample points, and reset restart after the hidden mid-run reset.

## Checker Contract

Trace signals: `clk`, `rst_n`, `out0`, `out1`, `out2`, `out3`.

At each sample time listed in `test_harness/checks.yaml`, classify an output as high when its voltage is greater than `0.45 V`. A passing waveform has exactly one high output and the active output name must match the expected sequence. Hidden samples additionally verify that `rst_n` is released at sample points and that asserting `rst_n` low between the two windows restarts the sequence.

## Negative Coverage

- `neg_001_stuck_initial_state`: no clock advancement.
- `neg_002_skip_every_other_state`: advances by two states per clock.
- `neg_003_monotonic_output_order`: uses monotonic output mapping instead of the required permutation.
- `neg_004_forces_state_three`: forces a single state after every clock.
- `neg_005_out0_stuck_high`: violates the one-hot rotating sequence.
- `neg_006_ignore_midrun_reset`: passes the first six-sample window but ignores the hidden mid-run reset restart.

## Evidence

- File-level release-v3 structure prepared in this task directory only.
- Gold EVAS certification PASS under `v3_006_element_shuffler` with active sequence `2,0,3,1,2,0,2,0,3,1`.
- Concrete negative variants: 6/6 compile and fail with `FAIL_SIM_CORRECTNESS`.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: hidden
  gold PASS and 6/6 hidden negative variants `NEGATIVE_REJECTED`.

## Remaining Risk

- AHDL lint evidence is not attached yet; do not mark
  `cadence_modeling_ready` until lint/triage is recorded.

Certification status: certified as an EVAS formal candidate on 2026-06-26.
