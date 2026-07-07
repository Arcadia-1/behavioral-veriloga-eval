# Macro Ifdef Gain Select

## Task Contract

Implement one behavioral Verilog-A source file named `macro_ifdef_gain_select.va`.
This is a Spectre-compatible Verilog-A language-semantics support row for
conditional preprocessor selection inside a clocked voltage-domain model, not a
standalone AMS circuit-function row.

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module macro_ifdef_gain_select (
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
`parameter real tr = 200p`. Use `vth` for clock and reset thresholding and `tr`
as the transition rise/fall time. Keep `vhi` as a public compatibility
parameter even though this row's gain-selection behavior does not otherwise use
it. These parameters may be overridden by a testbench.

## Required Behavior

Define `V3_HIGH_GAIN` before the module declaration. Use
`` `ifdef V3_HIGH_GAIN`` / `` `else`` / `` `endif`` to select a real-valued
`selected_gain`: `1.25` when `V3_HIGH_GAIN` is defined and `0.75` otherwise.

Initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`.
On each rising crossing of `clk`, clear these state values when `rst > vth`.
Otherwise set `out_v` to the selected gain times the sampled `vin`, set
`metric_v` to the selected gain, and increment `count_q` after computing the
outputs.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `macro_ifdef_gain_select.va`.
