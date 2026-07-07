# While Loop Array Sum

## Task Contract

Implement one behavioral Verilog-A source file named `while_loop_array_sum.va`.
This is a Spectre-compatible Verilog-A language-semantics support row for a
bounded `while` loop in a clocked voltage-domain model, not a standalone AMS
circuit-function row.

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module while_loop_array_sum (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and
`parameter real tr = 200p`. Use `vth` for clock and reset thresholding, `vhi`
as the high output level, and `tr` as the transition rise/fall time. These
parameters may be overridden by a testbench.

## Required Behavior

Initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`.
On each rising crossing of `clk`, clear these state values when `rst > vth`.

Otherwise set a local loop index to zero and a local accumulator to zero, then
use a bounded `while` loop with three iterations. Each iteration adds the loop
index and the current `count_q` to the accumulator, then increments the loop
index. After the loop, drive `out_v` high only when the accumulator is greater
than `3`, set `metric_v` to the accumulator value, and increment `count_q`
after computing the outputs.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `while_loop_array_sum.va`.
