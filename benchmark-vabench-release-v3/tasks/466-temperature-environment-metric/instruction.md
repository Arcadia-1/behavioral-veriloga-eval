# Temperature Environment Metric

Implement one Verilog-A source file named `temperature_environment_metric.va`.

## Required Feature

Use $temperature as an environment-dependent metric.

## Required Interface

```verilog
module temperature_environment_metric (
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
  - Otherwise drive `out = $temperature / 300.0`.
  - Drive `metric = $temperature`.
  - Increment the internal event counter.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `temperature_environment_metric.va`.
