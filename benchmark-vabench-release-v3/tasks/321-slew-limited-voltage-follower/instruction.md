# Slew Limited Voltage Follower

Implement one behavioral Verilog-A DUT file named `slew_limited_voltage_follower.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `slew()` to limit voltage-domain output slope.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V. Use `rise_rate = 8.0e8` V/s and `fall_rate = 3.0e8` V/s.

On a rising `rst` event, clear the internal target values to zero. On every rising crossing of `clk` through `vth` while reset is low:

- when `mode` is low, set the target output to `vin`
- when `mode` is high, set the target output to `vhi - vin`
- clamp the target output to `[0, vhi]`
- set the target metric to `target_out / vhi`

Drive both outputs through `slew(target, rise_rate, fall_rate)`. The hidden evaluator checks both the settled levels and intermediate ramp points, so replacing `slew()` with an immediate or `transition()` output is incorrect. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `slew_limited_voltage_follower.va`. Do not generate a Spectre testbench for this task.
