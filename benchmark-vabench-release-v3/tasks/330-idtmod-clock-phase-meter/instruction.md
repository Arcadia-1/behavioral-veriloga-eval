# Idtmod Clock Phase Meter

## Task Contract

Implement one behavioral Verilog-A DUT file named `idtmod_clock_phase_meter.va`.

This task focuses on clock-sampled `idtmod()` phase measurement. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a mixed continuous-time/event helper. The phase must accumulate continuously with `idtmod()`, and a held sampled phase must update only on rising clock crossings.

## Public Verilog-A Interface

```verilog
module idtmod_clock_phase_meter (
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
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Use `freq_q = 1.25e6 + 0.5e6 * V(vin)`.
- Use `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`.

## Required Behavior

- On each rising crossing of `V(clk) - vth`, sample the current `phase_q`.
- If reset is high at the clock crossing, clear the sampled phase and `metric` to `0.0`.
- Otherwise drive `out = vhi * sampled_phase`.
- Otherwise drive `metric = vhi` when the sampled phase is greater than `V(mode)`, else `0.0`.
- The held output must report the most recent clock-sampled phase, not the continuously changing instantaneous phase.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `idtmod_clock_phase_meter.va`. Do not generate a Spectre testbench for this task.
