# Bound Step Clock Guard

## Task Contract

Implement one behavioral Verilog-A DUT file named `bound_step_clock_guard.va`.

This task focuses on `$bound_step` time-step guarding in a clocked voltage helper. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a clocked guard helper that requests a bounded simulator time step while updating a sampled output only when mode enables the update.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level limit `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Call `$bound_step(0.5n)` inside the analog block.

## Required Behavior

- On each rising crossing of `V(clk) - vth`, update the guard state.
- If reset is high, clear both outputs to `0.0`.
- If reset is low and mode is low, keep `out` unchanged and drive `metric = 0.2`.
- If reset is low and mode is high, sample `V(vin)` into `out`, clipped to `0.0 ... vhi`, and drive `metric = 0.8`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `bound_step_clock_guard.va`. Do not generate a Spectre testbench for this task.
