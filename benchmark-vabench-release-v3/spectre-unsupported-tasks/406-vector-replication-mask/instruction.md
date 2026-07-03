# Vector Replication Mask

Implement one behavioral Verilog-A source file named `vector_replication_mask.va`.

## Interface

Use this exact module interface:

```verilog
module vector_replication_mask (
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

Use replication concatenation to build a repeated mask.

Required behavior:

- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set `mask_q = {2{2'b10}}`;
- set `out_v = ((mask_q & count_q) != 0) ? vhi : 0.0`;
- set `metric_v = mask_q`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `vector_replication_mask.va`.
