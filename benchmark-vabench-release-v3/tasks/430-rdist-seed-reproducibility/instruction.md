# Rdist Seed Reproducibility

Implement one behavioral Verilog-A source file named `rdist_seed_reproducibility.va`.

## Interface

Use this exact module interface:

```verilog
module rdist_seed_reproducibility (
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

Use repeated seeded random distribution calls to make reproducibility explicit.

Required behavior:

- declare two integer seeds and initialize both to the same value at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise set `seed_a` and `seed_b` to the same deterministic value for that sample, such as `430 + count_q`;
- call `$rdist_poisson(seed_a, 2.0)` and `$rdist_poisson(seed_b, 2.0)` once each;
- drive `out_v = V(vin) + 0.01 * rand_a`;
- drive `metric_v = 1.0` after the paired seeded calls complete;
- increment `count_q` after each non-reset sample;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `rdist_seed_reproducibility.va`.
