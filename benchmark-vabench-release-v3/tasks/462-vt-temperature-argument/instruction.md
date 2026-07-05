# Vt Temperature Argument

## Task Contract

Implement one Verilog-A source file named `vt_temperature_argument.va`. The task is an L0/support row for `$vt(...)` with an explicit temperature argument.

## Form-Specific Requirements

This is a DUT task for environment-function semantics. It is not a standalone thermal sensor circuit.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module vt_temperature_argument (
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

Initialize `out`, `metric`, and an internal event counter to zero. On each rising crossing of `clk` through `vth`, clear the state when `rst > vth`; otherwise sample `$vt(600.0)` into both `out` and `metric` and increment the event counter.

## Modeling Constraints

Use the explicit `$vt(600.0)` form. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `vt_temperature_argument.va`.
