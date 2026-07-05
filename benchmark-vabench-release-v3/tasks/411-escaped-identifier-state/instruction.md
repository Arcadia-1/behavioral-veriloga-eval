# Escaped Identifier State

## Task Contract

Implement one behavioral Verilog-A source file named `escaped_identifier_state.va`.
This is a Spectre-compatible Verilog-A language-semantics support row for an
escaped internal identifier used as sampled behavioral state, not a standalone
AMS circuit-function row.

## Form-Specific Requirements

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module escaped_identifier_state (
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
`parameter real tr = 200p`. Use `vth` for clock, reset, and mode thresholding
and `tr` as the transition rise/fall time. Keep `vhi` as a public compatibility
parameter even though this row's trim-state behavior does not otherwise use it.
These parameters may be overridden by a testbench.

## Required Behavior

Declare a real escaped identifier named `\trim.state`. Initialize
`\trim.state = 0.1`, `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and
`state_q = 0`.

On each rising crossing of `clk`, clear the output and count state when
`rst > vth`. Otherwise set `\trim.state` to `0.2` when `mode > vth` and `0.1`
when `mode <= vth`, set `out_v` to the sampled `vin` plus the trim state, set
`metric_v` to the trim state, and increment `count_q` after computing the
outputs.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `escaped_identifier_state.va`.
