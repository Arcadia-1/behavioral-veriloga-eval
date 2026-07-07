# Parameter Range Real Control

## Task Contract

Implement one behavioral Verilog-A source file named
`parameter_range_real_control.va`. This is a Spectre-compatible Verilog-A
language-semantics support row for ranged real and integer parameter
declarations in a clocked voltage-domain model, not a standalone AMS
circuit-function row.

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module parameter_range_real_control (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`,
`parameter real tr = 200p`, `parameter real gain_limited = 0.8 from [0.0:2.0]`,
and `parameter integer max_count = 8 from [1:32]`. Use `vth` for clock and
reset thresholding, `tr` as the transition rise/fall time, `gain_limited` as
the sampled-input gain, and `max_count` as the counter modulus. Keep `vhi` as a
public compatibility parameter even though this ranged-parameter row does not
otherwise use it. These parameters may be overridden by a testbench within their
declared ranges.

## Required Behavior

Initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`.
On each rising crossing of `clk`, clear these state values when `rst > vth`.
Otherwise increment `count_q` modulo `max_count`, set `out_v` to
`gain_limited` times the sampled `vin`, and set `metric_v` to the updated count.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `parameter_range_real_control.va`.
