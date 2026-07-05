# Simparam Query Tnom

## Task Contract

Implement one Verilog-A source file named `simparam_query_tnom.va`. The task is an L0/support row for querying simulator/environment parameters with `$simparam()`.

## Form-Specific Requirements

This is a DUT task for simulator environment-function semantics. It is not a standalone temperature-reference circuit.

## Public Verilog-A Interface

Use this exact module interface:

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

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. `vth` is the clock/reset threshold and `tr` is the transition rise/fall time. `vhi` is retained as a compatibility parameter.

## Required Behavior

Initialize `out`, `metric`, and an internal event counter to zero. On each rising crossing of `clk` through `vth`, clear the state when `rst > vth`; otherwise query `$simparam("tnom", 27.0)`, divide the returned value by `300.0`, drive both `out` and `metric` with that normalized value, and increment the event counter.

## Modeling Constraints

Use `$simparam("tnom", 27.0)` for the environment query. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `simparam_query_tnom.va`.
