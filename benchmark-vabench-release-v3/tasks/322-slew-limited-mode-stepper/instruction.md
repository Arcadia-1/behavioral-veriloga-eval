# Slew Limited Mode Stepper

Implement one behavioral Verilog-A DUT file named `slew_limited_mode_stepper.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `slew()` to limit a mode-selected voltage stepper output.

Use voltage-coded logic with `vth = 0.45` V, `rise_rate = 8.0e8` V/s, and `fall_rate = 3.0e8` V/s.

On a rising `rst` event, clear the target outputs. On each rising crossing of `clk` through `vth` while reset is low, choose the target output from `mode`:

- `mode < 0.30`: target `out = 0.20`
- `0.30 <= mode < 0.70`: target `out = 0.80`
- `mode >= 0.70`: target `out = 0.20`

Set target `metric = target_out / 0.80`. Drive both public outputs using `slew(target, rise_rate, fall_rate)`. The hidden evaluator checks intermediate ramp points after the upward and downward steps, so an immediate output step is incorrect. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `slew_limited_mode_stepper.va`. Do not generate a Spectre testbench for this task.
