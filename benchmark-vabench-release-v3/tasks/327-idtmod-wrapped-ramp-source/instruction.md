# Idtmod Wrapped Ramp Source

## Task Contract

Implement one behavioral Verilog-A DUT file named `idtmod_wrapped_ramp_source.va`.

This task focuses on a resettable Cadence `idtmod()` wrapped ramp source. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a continuous-time wrapped ramp helper with voltage-coded reset. The reset must suppress phase accumulation through the `idtmod()` input rather than through a separate output-only mask.

## Public Verilog-A Interface

```verilog
module idtmod_wrapped_ramp_source (
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
- Use `freq_q = 0.75e6 + 1.5e6 * V(vin)`.
- Use `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`.

## Required Behavior

- While reset is high, drive both `out` and `metric` to `0.0`.
- Otherwise drive `out = vhi * phase_q`.
- Otherwise drive `metric = vhi` when `phase_q > V(mode)`, else `0.0`.
- After reset release, the ramp must resume from the `idtmod()` state implied by the reset-gated integrand.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `idtmod_wrapped_ramp_source.va`. Do not generate a Spectre testbench for this task.
