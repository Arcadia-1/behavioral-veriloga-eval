# Rdist Uniform Seeded Dither

Implement one behavioral Verilog-A/AMS source file named `rdist_uniform_seeded_dither.va`.

## Interface

Use this exact module interface:

```verilog
module rdist_uniform_seeded_dither (
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

Use $rdist_uniform() for seeded uniform dither.

Required behavior:

- initialize `seed_q` to 448 at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise call `$rdist_uniform(seed_q, 0.0, 1.0)`;
- set `out_v = V(vin) + 0.01 * rnd_q`;
- set `metric_v = rnd_q`;
- increment `count_q` after each non-reset sample;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `rdist_uniform_seeded_dither.va`.
