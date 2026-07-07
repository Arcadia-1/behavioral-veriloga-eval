# Analysis Dependent DC/TRAN Mode

## Task Contract

Implement one behavioral Verilog-A source file named `analysis_dependent_dc_tran_mode.va`. This is a support/L0 Verilog-A semantics task for `analysis()` mode-dependent voltage behavior, not a standalone core circuit macro.

This is a DUT source task. Implement only the `analysis_dependent_dc_tran_mode` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module analysis_dependent_dc_tran_mode (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: clock crossing threshold in volts.
- `vhi = 0.9`: high value reported on `metric` when transient analysis is active.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.

## Required Behavior

Drive `out` as an analysis-dependent voltage contribution: `0.25` during `analysis("dc")`, the instantaneous `V(ctrl)` during `analysis("tran")`, and `0.0` otherwise.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `vhi` when `analysis("tran")` is true, otherwise set it to zero. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `analysis()` only to select branch behavior, not to infer private simulator state. Do not place continuously varying branch voltages such as `V(ctrl)` inside `transition()`; drive continuous voltage behavior directly as a branch contribution. Use `transition()` only for event-updated state such as `metric_v`.

## Output Contract

Return exactly one source artifact named `analysis_dependent_dc_tran_mode.va`.
