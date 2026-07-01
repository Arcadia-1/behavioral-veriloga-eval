# Vector Part Select Window

Implement one behavioral Verilog-A source file named `vector_part_select_window.va`.

## Interface

Use this exact module interface:

```verilog
module vector_part_select_window (
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

Use Verilog part-select syntax on integer vector state.

Required behavior:

- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set `code_q = count_q + 9`;
- set `window_q = code_q[3:1]`;
- set `out_v = window_q > 3 ? vhi : 0.0`;
- set `metric_v = window_q`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `vector_part_select_window.va`.
