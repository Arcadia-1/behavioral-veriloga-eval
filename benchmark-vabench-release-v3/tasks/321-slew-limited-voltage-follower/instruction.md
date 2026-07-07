# Slew Limited Voltage Follower

## Task Contract

Implement one behavioral Verilog-A DUT file named `slew_limited_voltage_follower.va`. The DUT samples a voltage target on clock events and drives both public outputs through the Verilog-A `slew()` operator.

This is a DUT-only Verilog-A modeling task. The supplied testbenches are verification scenarios; do not hard-code their stop times, sample times, or waveform breakpoints into the DUT.

## Public Verilog-A Interface

```verilog
module slew_limited_voltage_follower (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45` V is the voltage-coded logic threshold.
- `vhi = 0.9` V is the full-scale voltage used for inversion, clamping, and metric normalization.
- `rise_rate = 8.0e8` V/s is the positive output slew-rate limit.
- `fall_rate = 3.0e8` V/s is the positive magnitude of the falling slew-rate limit. Cadence Verilog-A `slew(expr, SRpos, SRneg)` expects `SRneg` to be negative, so use `-fall_rate` as the third argument.

## Required Behavior

On a rising `rst` event, clear the internal target values to zero. On every rising crossing of `clk` through `vth` while reset is low:

- when `mode` is low, set the target output to `vin`
- when `mode` is high, set the target output to `vhi - vin`
- clamp the target output to `[0, vhi]`
- set the target metric to `target_out / vhi`

Both `out` and `metric` must follow their targets with slew-limited rising and falling slopes, including intermediate ramp values before final settling.

## Modeling Constraints

Use pure voltage-domain behavioral Verilog-A. Do not instantiate devices, do not drive `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive the public outputs with `slew(target, rise_rate, -fall_rate)`, not with an immediate assignment or `transition()`.

## Output Contract

Return exactly one source artifact named `slew_limited_voltage_follower.va`. Do not generate a Spectre testbench for this task.
