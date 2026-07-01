# Limexp Soft Exponential

Implement one behavioral Verilog-A/AMS source file named `limexp_soft_exponential.va`.

## Interface

Use this exact module interface:

```verilog
module limexp_soft_exponential (
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

Use limexp() for a limited exponential behavioral transform.

Required behavior:

- initialize output state and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise compute `out_v = limexp(V(vin))`;
- set `metric_v = out_v`;
- increment `count_q` after each non-reset sample;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `limexp_soft_exponential.va`.
