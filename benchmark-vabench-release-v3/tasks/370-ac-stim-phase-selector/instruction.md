# AC Stim Phase Selector

## Task Contract

Implement one behavioral Verilog-A source file named `ac_stim_phase_selector.va`. This is a support/L0 Verilog-A semantics task for selecting an `ac_stim()` phase from an analog control level, not a standalone core circuit macro.

This is a DUT source task. Implement only the `ac_stim_phase_selector` module; no external testbench or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module ac_stim_phase_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45`: control and clock threshold in volts.
- `vhi = 0.9`: high value reported on `metric` when the high-phase state is selected.
- `tr = 200p`: rise/fall time for the event-updated `metric` transition.

## Required Behavior

In transient analysis, drive `out` directly from the instantaneous control voltage: `V(out) <+ V(ctrl)`. When `analysis("ac")` is true, add `ac_stim("ac", 1.0, selected_phase)` where `selected_phase` is `1.5707963267948966` radians when `V(ctrl) > vth` and `0.0` otherwise.

Initialize `metric_v` to zero at `initial_step`. On every rising crossing of `clk` through `vth`, set `metric_v` to `vhi` when `V(ctrl) > vth`, otherwise set it to zero. Drive `metric` with `transition(metric_v, 0.0, tr, tr)`.

## Modeling Constraints

Use `ac_stim()` directly in a voltage branch contribution and only under the AC-analysis guard. The `ac_stim()` phase argument is in radians. Do not place continuously varying branch voltages such as `V(ctrl)` inside `transition()`; drive continuous voltage behavior directly as a branch contribution.

## Output Contract

Return exactly one source artifact named `ac_stim_phase_selector.va`.
