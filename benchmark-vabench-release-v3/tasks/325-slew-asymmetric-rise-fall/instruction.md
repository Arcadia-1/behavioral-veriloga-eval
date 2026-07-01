# Slew Asymmetric Rise Fall

Implement one behavioral Verilog-A DUT file named `slew_asymmetric_rise_fall.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module slew_asymmetric_rise_fall (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `slew()` with intentionally asymmetric rise and fall rates.

Use voltage-coded logic with `vth = 0.45` V, `rise_rate = 8.0e8` V/s, and `fall_rate = 2.0e8` V/s.

On reset, clear target `out` and `metric` to zero. On each rising crossing of `clk` while reset is low:

- if `mode` is low, set target `out = 0.80`
- if `mode` is high, set target `out = 0.10`
- set target `metric = target_out / 0.80`

Drive both outputs using `slew(target, rise_rate, fall_rate)`. The hidden evaluator checks that the rise reaches its target quickly while the fall takes several nanoseconds, so using equal rise/fall rates or immediate transitions is incorrect. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `slew_asymmetric_rise_fall.va`. Do not generate a Spectre testbench for this task.
