# Honest SOP Audit: Task 107 Reference Step Clock

## Scope

Task boundary is one primary Verilog-A DUT artifact, `ref_step_clk.va`. This
row was split from the original
`vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb` scenario after
duplicate-counting audit found that the previous v3 row reused the same CPPLL
system checker as task 097.

## Four Standards

- Useful scenario: accepted. A reference clock with a deterministic frequency
  step is a reusable stimulus/support block for PLL and timing-flow tests.
- Reasonable task: accepted. The public prompt names the target artifact,
  interface, public parameters, parameterized pre/post cadence semantics,
  switching behavior, rails, and duty-cycle expectation without exposing the
  hidden numeric scenario.
- Complete tests: accepted for the current reviewed slice. Gold passes and five
  concrete behavior negatives fail by simulation correctness under the Spectre
  evidence runner.
- Fair evaluation: improved. The checker now evaluates the local `CLK`
  waveform rather than downstream CPPLL reacquisition behavior.

## Checker And Evidence

- Checker id: `v3_reference_step_clock`
- EVAS hidden gold smoke: PASS
- Concrete negatives: 5/5 `FAIL_SIM_CORRECTNESS`
- Hidden test parameters intentionally differ from the visible smoke parameters
  to reduce fixed-waveform overfitting risk.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: hidden
  gold PASS and 5/5 hidden negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

AHDL lint evidence is not attached yet; do not mark `cadence_modeling_ready`
until lint/triage is recorded.
