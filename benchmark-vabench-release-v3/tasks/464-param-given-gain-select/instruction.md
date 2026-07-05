# Param Given Gain Select

## Task Contract

Implement one Verilog-A source file named `param_given_gain_select.va`. The task is an L0/support row for using `$param_given()` to select behavior based on whether an instance parameter was explicitly overridden.

## Form-Specific Requirements

This is a DUT task for environment-function semantics. The supplied testbenches instantiate both default and explicitly overridden parameter paths.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module param_given_gain_select (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real gain = 0.8`, `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. `gain` is used only when `$param_given(gain)` is true. `vth` is the clock/reset threshold and `tr` is the transition rise/fall time. `vhi` is retained as a compatibility parameter.

## Required Behavior

Initialize `out`, `metric`, and an internal event counter to zero. On each rising crossing of `clk` through `vth`, clear the state when `rst > vth`; otherwise use `$param_given(gain)` to choose the active gain. If `gain` was explicitly provided, drive `out = gain * V(vin)` and `metric = 1.0`; otherwise drive `out = V(vin)` and `metric = 0.0`.

## Modeling Constraints

Use `$param_given(gain)` for the selection. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `param_given_gain_select.va`.
