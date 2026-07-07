# Idtmod Phase Accumulator

## Task Contract

Implement one behavioral Verilog-A DUT file named `idtmod_phase_accumulator.va`.

This task focuses on a Cadence `idtmod()` wrapped phase accumulator. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a continuous-time wrapped phase helper. The phase must be produced by `idtmod()`, not by a manually updated discrete counter or an unwrapped `idt()` state.

## Public Verilog-A Interface

```verilog
module idtmod_phase_accumulator (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- Use `vth = 0.45` V for voltage-coded decisions if needed.
- Use high output level `vhi = 0.9` V.
- Use `freq_q = 1.0e6 + 2.0e6 * V(vin)`.
- Use `phase_q = idtmod(freq_q, 0.0, 1.0)`.

## Required Behavior

- Continuously drive `out = vhi * phase_q`.
- Continuously drive `metric = vhi` when `phase_q > V(mode)`, otherwise `0.0`.
- The output phase must wrap smoothly from the modulo limit back to zero according to `idtmod()` semantics.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `idtmod_phase_accumulator.va`. Do not generate a Spectre testbench for this task.
