# While Loop Array Sum

Implement one behavioral Verilog-A source file named `while_loop_array_sum.va`.

## Interface

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

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use a while loop over small behavioral state.

Required behavior:

- initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and `state_q` when `rst > vth`;
- otherwise set `i = 0` and `acc_q = 0`;
- while `i < 3`, update `acc_q = acc_q + i + count_q` and increment `i`;
- after the loop, set `out_v = (acc_q > 3) ? vhi : 0.0`;
- set `metric_v = acc_q`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `while_loop_array_sum.va`.
