# Repeat Loop Accumulator

Implement one behavioral Verilog-A source file named `repeat_loop_accumulator.va`.

## Interface

Use this exact module interface:

```verilog
module repeat_loop_accumulator (
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

Use repeat-loop syntax to accumulate bounded behavioral state.

Required behavior:

- declare integer state for `count_q` and `acc_q`;
- initialize output state and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise set `acc_q = 0`, execute `repeat (4)`, and add `count_q + 1` on each repeat iteration;
- set `out_v = vhi` only when `acc_q > 4`, else 0.0;
- set `metric_v = acc_q`;
- increment `count_q` after computing the accumulator;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `repeat_loop_accumulator.va`.
