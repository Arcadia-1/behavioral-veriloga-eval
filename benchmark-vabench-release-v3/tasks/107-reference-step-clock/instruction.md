# Reference Step Clock

Implement `ref_step_clk.va` in Verilog-A.

## Interface

```verilog
module ref_step_clk (
    inout  electrical VDD,
    inout  electrical VSS,
    output electrical CLK
);
```

## Required Behavior

This task asks for the `ref_step_clk` behavioral module, not a Spectre
testbench. The evaluator instantiates this module directly and checks the
generated `CLK` waveform.

- Generate a voltage-coded square-wave clock on `CLK`.
- Use the `VDD` and `VSS` supplies as the high and low output rails.
- Before `t_switch`, use `period_pre` as the full clock period.
- Near the switching time, transition from the pre-step cadence to the
  post-step cadence using `period_post` for subsequent clock periods.
- Keep duty cycle close to 50% before and after the frequency step.
- Preserve the public parameters `period_pre`, `period_post`, `t_switch`, and
  `tedge`.

A correct implementation should be parameterized by those public parameters
rather than hard-coding a fixed waveform. The observable behavior should remain
consistent when the evaluator instantiates nearby legal parameter values, and
should not rely on a fixed internal variable name or exact implementation
template.

Use voltage-coded logic with a mid-supply decision threshold where applicable,
drive high logic outputs near `VDD` and low outputs near `VSS`, and keep the
model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise
analysis, hidden checker logic, or simulator-private side channels.

Only `ref_step_clk.va` is graded as the candidate implementation.
