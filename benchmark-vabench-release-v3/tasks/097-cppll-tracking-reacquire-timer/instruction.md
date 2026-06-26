# CPPLL Tracking Reacquire Timer

Implement `cppll_timer_ref.va` in Verilog-A.

## Interface

```verilog
module cppll_timer_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical ref_clk,
    output electrical fb_clk,
    output electrical dco_clk,
    output electrical vctrl_mon,
    output electrical lock
);
```

## Required Behavior

This task asks for the `cppll_timer_ref` behavioral module, not a Spectre
testbench. The evaluator supplies a reference-step clock source and
instantiates your module in a CPPLL frequency-step reacquire scenario.

Support these public parameters:

- `div_ratio`
- `f_center`
- `kvco_hz_per_v`
- `f_min`
- `f_max`
- `kp`
- `ki`
- `integ_min`
- `integ_max`
- `vctrl_init`
- `tedge`
- `lock_tol`
- `lock_count_target`

Required observable behavior:

- Use `ref_clk` as the reference timing input.
- Generate a behavioral DCO clock on `dco_clk`.
- Generate `fb_clk` by dividing the DCO activity according to `div_ratio`.
- Update a bounded control-voltage monitor on `vctrl_mon`.
- Drive `lock` high after stable tracking, low or unstable during the
  reference-frequency disturbance, and high again after reacquisition.
- The late-window relation should show `fb_clk` tracking the new `ref_clk`
  cadence while `vctrl_mon` remains within the supply rails.

Use voltage-coded logic with a mid-supply decision threshold where applicable,
drive high logic outputs near `VDD` and low outputs near `VSS`, and keep the
model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise
analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion
support files are supplied by the harness for this task.
