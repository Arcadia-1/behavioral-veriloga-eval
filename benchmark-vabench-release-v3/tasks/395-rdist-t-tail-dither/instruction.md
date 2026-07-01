# Rdist T Tail Dither

Implement one behavioral Verilog-A source file named `rdist_t_tail_dither.va`.

## Interface

Use this exact module interface:

```verilog
module rdist_t_tail_dither (
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

Use `$rdist_t()` for deterministic seeded heavy-tail dither.

Required behavior:

- initialize `seed_q = 395`, `noise_q = 0.0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, and counters when `rst > vth`;
- otherwise draw `noise_q = $rdist_t(seed_q, 4.0)`;
- set `out_v = V(vin) + 0.01 * noise_q`;
- set `metric_v = noise_q`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `rdist_t_tail_dither.va`.
