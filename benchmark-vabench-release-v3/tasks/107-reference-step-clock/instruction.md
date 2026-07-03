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
testbench. The verification harness instantiates this module directly and
checks the generated `CLK` waveform.

- Generate a voltage-coded square-wave clock on `CLK`.
- Use the `VDD` and `VSS` supplies as the high and low output rails.
- Before `t_switch`, use `period_pre` as the full clock period.
- Near the switching time, transition from the pre-step cadence to the
  post-step cadence using `period_post` for subsequent clock periods.
- Keep duty cycle close to 50% before and after the frequency step.
- Preserve the public parameters `period_pre`, `period_post`, `t_switch`, and
  `tedge`.

Public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `period_pre` | `20 ns` | time, `(0:inf)` | Full clock period before the frequency step. |
| `period_post` | `19.5 ns` | time, `(0:inf)` | Full clock period after the frequency step. |
| `t_switch` | `2 us` | time, `[0:inf)` | Time at which subsequent clock periods use `period_post`. |
| `tedge` | `100 ps` | time, `(0:inf)` | Rise/fall smoothing for the voltage-coded clock output. |

A correct implementation should be parameterized by those public parameters
rather than hard-coding a fixed waveform. The observable behavior should remain
consistent when the verification harness instantiates nearby legal parameter
values, and should not rely on a fixed internal variable name or exact
implementation template.

Use voltage-coded logic with a mid-supply decision threshold where applicable,
drive high logic outputs near `VDD` and low outputs near `VSS`, and keep the
model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise
analysis, checker logic, private test hooks, or simulator-private side channels.

Only `ref_step_clk.va` is graded as the candidate implementation.
