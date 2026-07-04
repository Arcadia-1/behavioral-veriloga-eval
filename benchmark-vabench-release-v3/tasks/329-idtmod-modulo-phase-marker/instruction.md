# Idtmod Modulo Phase Marker

## Task Contract

Implement one behavioral Verilog-A DUT file named `idtmod_modulo_phase_marker.va`.

This task focuses on explicit-modulo `idtmod()` phase wrapping and marker generation. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a wrapped phase marker using a modulo value of `0.25`. The marker output must be derived from the wrapped phase interval after each modulo reset.

## Public Verilog-A Interface

```verilog
module idtmod_modulo_phase_marker (
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
- Use `freq_q = 0.5e6 + 0.5e6 * V(vin)`.
- Use `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 0.25)`.
- Use `marker_width_q = 0.05` when `V(mode) > vth`, otherwise `0.025`.

## Required Behavior

- While reset is high, drive both outputs to `0.0`.
- Otherwise drive `out = vhi * phase_q / 0.25`.
- Otherwise drive `metric = vhi` when `phase_q < marker_width_q`, else `0.0`.
- The marker must follow the modulo-wrapped phase, not elapsed absolute time.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `idtmod_modulo_phase_marker.va`. Do not generate a Spectre testbench for this task.
