# Rdist Uniform Seeded Dither

## Task Contract

Implement one behavioral Verilog-A source file named `rdist_uniform_seeded_dither.va`.

Use `$rdist_uniform()` to generate seeded uniform dither for a sampled voltage output. The model should expose the current uniform draw on `metric` and add a small scaled version of that draw to the sampled input voltage.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and drive output transitions with rise/fall time `tr = 200p`. Use a uniform range from `0.0` to `1.0` and a small output dither scale of `0.01` V. These values may be implemented as compatible Verilog-A parameters or internal constants. The `mode` input is a public context input; this task does not require mode-dependent voltage behavior.

## Required Behavior

- Initialize an integer seed state at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- On each non-reset sample, call `$rdist_uniform(seed_q, 0.0, 1.0)`.
- Set `out_v` to `V(vin)` plus the scaled uniform draw.
- Set `metric_v` to the current uniform draw.
- Increment `count_q` after each non-reset sample.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Do not hard-code expected random waveform values; rely on the seeded distribution call semantics.

## Output Contract

Return exactly one source artifact named `rdist_uniform_seeded_dither.va`.
