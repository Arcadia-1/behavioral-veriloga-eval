# Initial Final Step Lifecycle

Implement one behavioral Verilog-A source file named `initial_final_step_lifecycle.va`.

## Interface

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

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use initial_step and final_step in one behavioral model.

Required behavior:

- use `@(initial_step)` to initialize `out_v = 0.0`, `metric_v = 0.0`, `count_q = 0`, and `state_q = 0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and `state_q` when `rst > vth`;
- otherwise set `out_v = V(vin)`;
- set `metric_v = count_q`;
- increment `count_q` after computing the outputs;
- use `@(final_step)` and set `state_q = count_q`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `initial_final_step_lifecycle.va`.
