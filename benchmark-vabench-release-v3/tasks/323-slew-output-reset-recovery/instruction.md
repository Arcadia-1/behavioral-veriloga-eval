# Slew Output Reset Recovery

Implement one behavioral Verilog-A DUT file named `slew_output_reset_recovery.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `slew()` to limit output slope through a reset-and-recovery sequence.

Use voltage-coded logic with `vth = 0.45` V, `rise_rate = 8.0e8` V/s, and `fall_rate = 3.0e8` V/s.

On a rising `rst` event, clear target `out` and `metric` to zero. On each rising crossing of `clk` while reset is low, set target `out = 0.80` and target `metric = 1.00`. Drive both public outputs using `slew(target, rise_rate, fall_rate)`.

The hidden testbench first slews up to the high target, then asserts reset long enough to force a falling slew toward zero, then releases reset and clocks the DUT again to verify slew-limited recovery. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `slew_output_reset_recovery.va`. Do not generate a Spectre testbench for this task.
