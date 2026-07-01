# Idtmod Clock Phase Meter

Implement one behavioral Verilog-A DUT file named `idtmod_clock_phase_meter.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `idtmod()` as a voltage-domain phase accumulator and sample its phase on clock edges.

This is a behavioral continuous-time/event task, not a conservative-current/KCL task. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `freq_q = 1.25e6 + 0.5e6 * V(vin)`
- `phase_q = idtmod((V(rst) > vth) ? 0.0 : freq_q, 0.0, 1.0)`
- on each rising crossing of `V(clk) - vth`, sample `phase_q`
- while `V(rst) > vth`, the sampled phase and `metric` must reset to `0.0`
- otherwise drive `out = 0.9 * sampled_phase`
- otherwise drive `metric = 0.9` when the sampled phase is greater than `V(mode)`, else `0.0`

The hidden testbench drives `vin = 0.4`, `mode = 0.55`, and clock rising edges near `100 ns`, `300 ns`, `500 ns`, and `700 ns`. The evaluator samples just after each edge to verify that the held output reports the clock-sampled phase rather than the continuously changing instantaneous phase.

## Output

Return exactly one source artifact named `idtmod_clock_phase_meter.va`. Do not generate a Spectre testbench for this task.
