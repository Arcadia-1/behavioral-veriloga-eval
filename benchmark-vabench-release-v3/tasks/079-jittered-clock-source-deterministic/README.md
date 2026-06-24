# Deterministic Jittered Clock Source

Implement `deterministic_jittered_clock.va` in Verilog-A.

## Interface

```verilog
module deterministic_jittered_clock(jitter_en, seed0, seed1, seed2, seed3, seed4, seed5, seed6, seed7, clk_out);
```

Inputs: `jitter_en, seed0, seed1, seed2, seed3, seed4, seed5, seed6, seed7`.
Outputs: `clk_out`.

## Required Behavior

Generate `clk_out` as a deterministic clock source. With `jitter_en` low, use a constant 20 ns period. With `jitter_en` high, apply a repeatable seed-dependent cycle-to-cycle period modulation while keeping periods bounded.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
