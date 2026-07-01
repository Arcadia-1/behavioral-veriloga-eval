# Idtmod Phase Accumulator

Implement one behavioral Verilog-A DUT file named `idtmod_phase_accumulator.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `idtmod()` as a voltage-domain wrapped phase accumulator.

This is a behavioral continuous-time task, not a conservative-current/KCL task. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

Use:

- `freq_q = 1.0e6 + 2.0e6 * V(vin)`
- `phase_q = idtmod(freq_q, 0.0, 1.0)`
- `out = 0.9 * phase_q`
- `metric = 0.9` when `phase_q > V(mode)`, otherwise `0.0`

The hidden testbench drives `vin = 0.5`, so `freq_q = 2 MHz` and the phase wraps every `0.5 us`. It drives `mode = 0.5`, so `metric` is high only for the upper half of each phase cycle.

## Output

Return exactly one source artifact named `idtmod_phase_accumulator.va`. Do not generate a Spectre testbench for this task.
