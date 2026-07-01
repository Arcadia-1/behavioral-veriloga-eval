# Rdist Chi Square Energy

Implement one behavioral Verilog-A source file named `rdist_chi_square_energy.va`.

## Interface

Use this exact module interface:

```verilog
module rdist_chi_square_energy (
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

Use `$rdist_chi_square()` for deterministic seeded energy-like variation.

Required behavior:

- initialize `seed_q = 394`, `noise_q = 0.0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, and counters when `rst > vth`;
- otherwise draw `noise_q = $rdist_chi_square(seed_q, 2.0)`;
- set `out_v = V(vin) + 0.01 * noise_q`;
- set `metric_v = noise_q`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `rdist_chi_square_energy.va`.
