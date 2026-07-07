# AC Stim Small Signal Source

## Task Contract

Implement one behavioral Verilog-A source file named `ac_stim_small_signal_source.va`. This is a support/L0 Verilog-A semantics task for `ac_stim()` in a voltage-domain behavioral source, not a standalone core circuit macro.

This is a DUT source task. Implement only the `ac_stim_small_signal_source` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module ac_stim_small_signal_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: clock crossing threshold in volts.
- `vhi = 0.9`: retained compatibility parameter for the shared source-task interface.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.
- `mag = 1.0`: AC stimulus magnitude.
- `phase_rad = 0.0`: AC stimulus phase in radians.

## Required Behavior

In transient analysis, drive `out` directly from the instantaneous control voltage: `V(out) <+ V(ctrl)`. When `analysis("ac")` is true, add an AC small-signal source contribution using `ac_stim("ac", mag, phase_rad)`.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `mag`. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `ac_stim()` directly in a voltage branch contribution and only under the AC-analysis guard. The `ac_stim()` phase argument is in radians. Do not place continuously varying branch voltages such as `V(ctrl)` inside `transition()`; drive continuous voltage behavior directly as a branch contribution.

## Output Contract

Return exactly one source artifact named `ac_stim_small_signal_source.va`.
