# Simparam Query Tnom

Implement one Verilog-A source file named `simparam_query_tnom.va`.

## Required Feature

Use $simparam() to query simulator/environment parameters.

## Required Interface

```verilog
module simparam_query_tnom (
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
  - Otherwise query `$simparam("tnom", 27.0)`.
  - Drive both `out` and `metric` with the queried value divided by 300.0.
  - Increment the internal event counter.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `simparam_query_tnom.va`.
