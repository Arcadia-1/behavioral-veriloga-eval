# Idtmod Wrapped Ramp Source

Implement one behavioral Verilog-A DUT file named `idtmod_wrapped_ramp_source.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `idtmod()` as a voltage-domain wrapped ramp source.

This is a behavioral continuous-time task, not a conservative-current/KCL task. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `freq_q = 0.75e6 + 1.5e6 * V(vin)`
- `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`
- while `V(rst) > vth`, drive both outputs to `0.0`
- otherwise drive `out = 0.9 * phase_q`
- otherwise drive `metric = 0.9` when `phase_q > V(mode)`, else `0.0`

The hidden testbench holds reset high at the beginning, then releases it while driving `vin = 0.5` and `mode = 0.6`. This makes `freq_q = 1.5 MHz`, so the wrapped ramp phase advances by about `0.15` every `100 ns` after reset is released. The evaluator samples both the analog ramp voltage and the thresholded metric output.

## Output

Return exactly one source artifact named `idtmod_wrapped_ramp_source.va`. Do not generate a Spectre testbench for this task.
