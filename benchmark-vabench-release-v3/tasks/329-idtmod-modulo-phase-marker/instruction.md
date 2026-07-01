# Idtmod Modulo Phase Marker

Implement one behavioral Verilog-A DUT file named `idtmod_modulo_phase_marker.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `idtmod()` with an explicit modulo value to build a wrapped phase marker.

This is a behavioral continuous-time task, not a conservative-current/KCL task. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `freq_q = 0.5e6 + 0.5e6 * V(vin)`
- `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 0.25)`
- `marker_width_q = 0.05` when `V(mode) > vth`, otherwise `0.025`
- while `V(rst) > vth`, drive both outputs to `0.0`
- otherwise drive `out = 0.9 * phase_q / 0.25`
- otherwise drive `metric = 0.9` when `phase_q < marker_width_q`, else `0.0`

The hidden testbench drives `vin = 0.5` and `mode = 0.9`, so the 0.25-modulo phase wraps about every `333 ns`. The evaluator samples the scaled sawtooth and checks that `metric` marks only the short post-wrap phase interval.

## Output

Return exactly one source artifact named `idtmod_modulo_phase_marker.va`. Do not generate a Spectre testbench for this task.
