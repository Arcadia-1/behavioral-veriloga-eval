# Vt Thermal Voltage Source

Implement one Verilog-A source file named `vt_thermal_voltage_source.va`.

## Required Feature

Use $vt as a thermal voltage environment value.

## Required Interface

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

## Required Behavior

- Initialize `out`, `metric`, and an internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the event counter.
  - Otherwise assign `$vt` to `out` and `metric`, then increment the event counter.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `vt_thermal_voltage_source.va`.
