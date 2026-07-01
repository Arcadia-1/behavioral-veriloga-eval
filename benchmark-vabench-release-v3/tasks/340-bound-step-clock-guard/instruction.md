# Bound Step Clock Guard

Implement one behavioral Verilog-A DUT file named `bound_step_clock_guard.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module bound_step_clock_guard (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `$bound_step(0.5n)` inside the analog block for time-step control.

Use voltage-coded logic with `vth = 0.45` V and high outputs below `vhi = 0.9` V.

On every rising crossing of `clk`:

1. If `rst` is high, drive both `out` and `metric` low.
2. If `rst` is low and `mode` is low, guard the clock update: keep `out` unchanged and drive `metric = 0.2`.
3. If `rst` is low and `mode` is high, sample `vin` into `out`, clipped to `[0.0, vhi]`, and drive `metric = 0.8`.

The evaluator checks the low-mode guard, the high-mode sampled update, reset clearing, and the presence of `$bound_step`.

## Output

Return exactly one source artifact named `bound_step_clock_guard.va`. Do not generate a Spectre testbench for this task.
