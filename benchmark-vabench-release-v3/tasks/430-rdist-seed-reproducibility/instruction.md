# Rdist Seed Reproducibility

## Task Contract

Implement one behavioral Verilog-A source file named `rdist_seed_reproducibility.va`.

Use two repeated seeded random distribution calls to make reproducibility explicit. The model should call `$rdist_poisson()` twice with equal deterministic seed state for a given sample and assert the metric output after the paired calls complete.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and drive output transitions with rise/fall time `tr = 200p`. Use a Poisson mean of `2.0` and a small output dither scale of `0.01` V per random count. These values may be implemented as compatible Verilog-A parameters or internal constants. The `mode` input is a public context input; this task does not require mode-dependent voltage behavior.

## Required Behavior

- Declare two integer seeds and initialize both to the same deterministic value at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- On each non-reset sample, set both seeds to the same deterministic per-sample value derived from `count_q`.
- Call `$rdist_poisson(seed_a, 2.0)` and `$rdist_poisson(seed_b, 2.0)` once each after setting the matched seeds.
- Drive `out_v` from `V(vin)` plus the scaled first random draw.
- Drive `metric_v` high after the paired seeded calls complete.
- Increment `count_q` after each non-reset sample.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Do not hard-code expected random waveform values; rely on the seeded distribution call semantics.

## Output Contract

Return exactly one source artifact named `rdist_seed_reproducibility.va`.
