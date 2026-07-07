# Initial Final Step Lifecycle

## Task Contract

Implement one behavioral Verilog-A source file named
`initial_final_step_lifecycle.va`. This is a Spectre-compatible Verilog-A
language-semantics support row for `initial_step` and `final_step` lifecycle
events in a clocked voltage-domain model, not a standalone AMS circuit-function
row.

Return the DUT source artifact only. The model is sampled on the rising crossing
of `clk`, reset by `rst`, and drives voltage outputs `out` and `metric`; it must
not introduce current contributions.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module initial_final_step_lifecycle (
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
parameter even though this lifecycle row does not otherwise use it. These
parameters may be overridden by a testbench.

## Required Behavior

Use `@(initial_step)` to initialize `out_v = 0.0`, `metric_v = 0.0`,
`count_q = 0`, and `state_q = 0`.

On each rising crossing of `clk`, clear these state values when `rst > vth`.
Otherwise sample `vin` into `out_v`, report the current count value on
`metric_v`, and increment `count_q` after computing the outputs. Use
`@(final_step)` to assign `state_q = count_q`.

## Modeling Constraints

Use `cross()` for the sampling event and `transition(...)` to drive `out` and
`metric`. Keep the behavior voltage-domain and behavioral; do not use `I(...)`,
devices, or testbench stop-time constants.

## Output Contract

Return exactly one source artifact named `initial_final_step_lifecycle.va`.
