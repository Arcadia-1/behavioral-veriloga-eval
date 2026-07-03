# Slew Limited Mode Stepper

## Task Contract

Implement one behavioral Verilog-A DUT file named `slew_limited_mode_stepper.va`. The DUT converts a voltage-coded mode input into stepped target levels and drives both public outputs through the Verilog-A `slew()` operator.

## Form-Specific Requirements

This is a DUT-only Verilog-A modeling task. The supplied testbenches are verification scenarios; do not hard-code their stop times, sample times, or waveform breakpoints into the DUT.

## Public Verilog-A Interface

```verilog
module slew_limited_mode_stepper (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45` V is the reset and clock threshold.
- `rise_rate = 8.0e8` V/s is the positive output slew-rate limit.
- `fall_rate = 3.0e8` V/s is the positive magnitude of the falling slew-rate limit. Cadence Verilog-A `slew(expr, SRpos, SRneg)` expects `SRneg` to be negative, so use `-fall_rate` as the third argument.

## Required Behavior

On a rising `rst` event, clear the target outputs. On each rising crossing of `clk` through `vth` while reset is low, choose the target output from `mode`:

- `mode < 0.30`: target `out = 0.20`
- `0.30 <= mode < 0.70`: target `out = 0.80`
- `mode >= 0.70`: target `out = 0.20`

Set target `metric = target_out / 0.80`. Both `out` and `metric` must follow their targets with slew-limited upward and downward ramps instead of immediate steps.

## Modeling Constraints

Use pure voltage-domain behavioral Verilog-A. Do not instantiate devices, do not drive `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive the public outputs with `slew(target, rise_rate, -fall_rate)`, not with an immediate assignment or `transition()`.

## Output Contract

Return exactly one source artifact named `slew_limited_mode_stepper.va`. Do not generate a Spectre testbench for this task.
