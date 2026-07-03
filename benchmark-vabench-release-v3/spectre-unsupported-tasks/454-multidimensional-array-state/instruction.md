# Multidimensional Array State

Implement one behavioral Verilog-A/AMS source file named `multidimensional_array_state.va`.

## Interface

Use this exact module interface:

```verilog
module multidimensional_array_state (
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

Use a two-dimensional integer array for behavioral state.

Required behavior:

- declare a two-dimensional integer array such as `integer arr[0:1][0:1]`;
- initialize output state and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise assign `arr[0][1] = count_q + 1`;
- set `out_v = vhi` only when `arr[0][1] > 2`, else 0.0;
- set `metric_v = arr[0][1]`;
- increment `count_q` after computing the array state;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `multidimensional_array_state.va`.
