# Slew Limited Envelope

## Task Contract

Implement one behavioral Verilog-A DUT file named `slew_limited_envelope.va`. The DUT samples a voltage envelope target and drives both public outputs through the Verilog-A `slew()` operator.

This is a DUT-only Verilog-A modeling task. The supplied testbenches are verification scenarios; do not hard-code their stop times, sample times, or waveform breakpoints into the DUT.

## Public Verilog-A Interface

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

## Public Parameter Contract

- `vth = 0.45` V is the reset, clock, and mode threshold.
- `rise_rate = 8.0e8` V/s is the positive output slew-rate limit.
- `fall_rate = 3.0e8` V/s is the positive magnitude of the falling slew-rate limit. Cadence Verilog-A `slew(expr, SRpos, SRneg)` expects `SRneg` to be negative, so use `-fall_rate` as the third argument.

## Required Behavior

On reset, clear the envelope to zero. On each rising crossing of `clk` through `vth` while reset is low:

- if `mode` is low, update the envelope to `max(previous_envelope, vin)`
- if `mode` is high, release the envelope to the current `vin`
- clamp the envelope to `[0, 0.8]`
- set target `out = envelope`
- set target `metric = envelope / 0.8`

Both `out` and `metric` must preserve the envelope hold behavior while changing with slew-limited rising and falling slopes.

## Modeling Constraints

Use pure voltage-domain behavioral Verilog-A. Do not instantiate devices, do not drive `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive the public outputs with `slew(target, rise_rate, -fall_rate)`, not with an immediate assignment or `transition()`.

## Output Contract

Return exactly one source artifact named `slew_limited_envelope.va`. Do not generate a Spectre testbench for this task.
