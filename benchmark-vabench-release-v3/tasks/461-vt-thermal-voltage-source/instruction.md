# Vt Thermal Voltage Source

## Task Contract

Implement one Verilog-A source file named `vt_thermal_voltage_source.va`. The task is an L0/support row for using `$vt` as a simulator thermal-voltage environment value.

## Form-Specific Requirements

This is a DUT task for environment-function semantics. It is not a standalone voltage source benchmark beyond exposing the sampled `$vt` value.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module vt_thermal_voltage_source (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. `vth` is the clock/reset threshold and `tr` is the transition rise/fall time. `vhi` is retained as a compatibility parameter.

## Required Behavior

Initialize `out`, `metric`, and an internal event counter to zero. On each rising crossing of `clk` through `vth`, clear the state when `rst > vth`; otherwise sample `$vt` into both `out` and `metric` and increment the event counter.

## Modeling Constraints

Use `$vt` without an explicit argument. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `vt_thermal_voltage_source.va`.
