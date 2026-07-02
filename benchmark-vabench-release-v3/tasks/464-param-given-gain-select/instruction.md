# Param Given Gain Select

Implement one Verilog-A source file named `param_given_gain_select.va`.

## Required Feature

Use $param_given() to choose behavior based on parameter override presence.

## Required Interface

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

## Required Behavior

- Declare `parameter real gain = 0.8`.
- Initialize `out`, `metric`, and an internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the event counter.
  - Otherwise use `$param_given(gain)` to choose the active gain.
  - When `gain` was explicitly provided on the instance, drive `out = gain * V(vin)` and `metric = 1.0`.
  - When `gain` was not explicitly provided, drive `out = V(vin)` and `metric = 0.0`.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `param_given_gain_select.va`.
