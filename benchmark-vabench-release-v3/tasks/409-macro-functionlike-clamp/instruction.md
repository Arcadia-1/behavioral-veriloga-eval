# Macro Functionlike Clamp

## Task Contract

Implement one behavioral Verilog-A source file named `macro_functionlike_clamp.va`.
This is a Spectre-compatible Verilog-A language-semantics support row for
function-like preprocessor macros inside a clocked voltage-domain model, not a
standalone AMS circuit-function row.

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module macro_functionlike_clamp (
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
as the metric normalization level, and `tr` as the transition rise/fall time.
These parameters may be overridden by a testbench.

## Required Behavior

Define and use a function-like preprocessor macro named `V3_CLAMP(x)`. The macro
must clamp its input below `0.0` to `0.0`, above `0.9` to `0.9`, and otherwise
pass the input through.

Initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`.
On each rising crossing of `clk`, clear these state values when `rst > vth`.
Otherwise sample `vin`, set `out_v` to the clamped sample, set `metric_v` to
the normalized clamped value, and increment `count_q` after computing the
outputs.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `macro_functionlike_clamp.va`.
