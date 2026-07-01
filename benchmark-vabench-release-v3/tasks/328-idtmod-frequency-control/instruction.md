# Idtmod Frequency Control

Implement one behavioral Verilog-A DUT file named `idtmod_frequency_control.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `idtmod()` as a voltage-domain phase accumulator whose frequency is controlled by `vin` and `mode`.

This is a behavioral continuous-time task, not a conservative-current/KCL task. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `gain_q = 2.0e6` when `V(mode) > vth`, otherwise `1.0e6`
- `freq_q = 0.5e6 + gain_q * V(vin)`
- `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`
- while `V(rst) > vth`, drive both outputs to `0.0`
- otherwise drive `out = 0.9 * phase_q`
- otherwise drive `metric = 0.9` when `phase_q > 0.75`, else `0.0`

The hidden testbench keeps `mode` high and steps `vin` from `0.1 V` to `0.6 V` around `400 ns`. The evaluator samples the ramp before and after the step to verify that `vin` changes the idtmod phase slope.

## Output

Return exactly one source artifact named `idtmod_frequency_control.va`. Do not generate a Spectre testbench for this task.
