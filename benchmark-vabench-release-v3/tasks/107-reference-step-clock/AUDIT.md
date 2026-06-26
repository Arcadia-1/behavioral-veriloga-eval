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
- Complete tests: accepted for EVAS smoke. Gold passes and five concrete
  behavior negatives fail by simulation correctness; Spectre rerun is still
  pending.
- Fair evaluation: improved. The checker now evaluates the local `CLK`
  waveform rather than downstream CPPLL reacquisition behavior.

## Checker And Evidence

- Checker id: `v3_reference_step_clock`
- EVAS hidden gold smoke: PASS
- Spectre hidden gold smoke: not rerun in this audit by request
- Concrete negatives: 5/5 `FAIL_SIM_CORRECTNESS`
- Hidden test parameters intentionally differ from the visible smoke parameters
  to reduce fixed-waveform overfitting risk.

## Remaining Risk

Do not count this task in a final release surface until the standalone checker
also has fresh Spectre certification.
