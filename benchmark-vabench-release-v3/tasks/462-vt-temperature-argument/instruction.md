# Vt Temperature Argument

Implement one Verilog-A source file named `vt_temperature_argument.va`.

## Required Feature

Use $vt(temp) with an explicit temperature argument.

## Required Interface

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

## Required Behavior

- Initialize `out`, `metric`, and an internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the event counter.
  - Otherwise assign `$vt(600.0)` to both `out` and `metric`, then increment the event counter.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `vt_temperature_argument.va`.
