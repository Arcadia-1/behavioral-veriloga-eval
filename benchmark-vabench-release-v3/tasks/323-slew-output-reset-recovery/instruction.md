# Slew Output Reset Recovery

## Task Contract

Implement one behavioral Verilog-A DUT file named `slew_output_reset_recovery.va`. The DUT models a resettable slew-limited output that ramps up after clock qualification, slews down during reset, and slews up again after reset release.

## Form-Specific Requirements

This is a DUT-only Verilog-A modeling task. The supplied testbenches are verification scenarios; do not hard-code their stop times, sample times, or waveform breakpoints into the DUT.

## Public Verilog-A Interface

```verilog
module slew_output_reset_recovery (
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

On a rising `rst` event, clear target `out` and `metric` to zero. On each rising crossing of `clk` through `vth` while reset is low, set target `out = 0.80` and target `metric = 1.00`.

Both public outputs must slew toward zero while reset is asserted and then slew back toward their high targets after reset release and the next clock event.

## Modeling Constraints

Use pure voltage-domain behavioral Verilog-A. Do not instantiate devices, do not drive `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive the public outputs with `slew(target, rise_rate, -fall_rate)`, not with an immediate assignment or `transition()`.

## Output Contract

Return exactly one source artifact named `slew_output_reset_recovery.va`. Do not generate a Spectre testbench for this task.
