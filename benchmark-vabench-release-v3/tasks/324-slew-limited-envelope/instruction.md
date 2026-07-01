# Slew Limited Envelope

Implement one behavioral Verilog-A DUT file named `slew_limited_envelope.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module slew_limited_envelope (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `slew()` to limit a sampled voltage envelope output.

Use voltage-coded logic with `vth = 0.45` V, `rise_rate = 8.0e8` V/s, and `fall_rate = 3.0e8` V/s.

On reset, clear the envelope to zero. On each rising crossing of `clk` while reset is low:

- if `mode` is low, update the envelope to `max(previous_envelope, vin)`
- if `mode` is high, release the envelope to the current `vin`
- clamp the envelope to `[0, 0.8]`
- set target `out = envelope`
- set target `metric = envelope / 0.8`

Drive both outputs using `slew(target, rise_rate, fall_rate)`. The hidden evaluator checks the rising ramp, held envelope plateau, and slew-limited release. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `slew_limited_envelope.va`. Do not generate a Spectre testbench for this task.
