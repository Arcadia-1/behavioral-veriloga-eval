# Idtmod Frequency Control

## Task Contract

Implement one behavioral Verilog-A DUT file named `idtmod_frequency_control.va`.

This task focuses on voltage-controlled `idtmod()` phase slope behavior. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a wrapped phase helper whose slope changes with the input voltage and a voltage-coded mode control. The mode must change the gain used in the continuous frequency expression.

## Public Verilog-A Interface

```verilog
module idtmod_frequency_control (
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
- Use `gain_q = 2.0e6` when `V(mode) > vth`, otherwise `1.0e6`.
- Use `freq_q = 0.5e6 + gain_q * V(vin)`.
- Use `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`.

## Required Behavior

- While reset is high, drive both outputs to `0.0`.
- Otherwise drive `out = vhi * phase_q`.
- Otherwise drive `metric = vhi` when `phase_q > 0.75`, else `0.0`.
- A change in `vin` or `mode` must change the subsequent phase slope rather than only changing an output scale factor.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `idtmod_frequency_control.va`. Do not generate a Spectre testbench for this task.
