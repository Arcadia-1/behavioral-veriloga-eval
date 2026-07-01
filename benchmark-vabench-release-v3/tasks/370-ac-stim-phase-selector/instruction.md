# Ac Stim Phase Selector

Implement one behavioral Verilog-A source file named `ac_stim_phase_selector.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module ac_stim_phase_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Select `ac_stim()` phase from a behavioral control voltage:

```verilog
V(out) <+ transition(V(ctrl), 0.0, tr, tr);
if (analysis("ac")) V(out) <+ ac_stim("ac", 1.0, V(ctrl) > vth ? 90.0 : 0.0);
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `vhi` when `ctrl` selects the 90 degree phase, otherwise zero:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = V(ctrl) > vth ? vhi : 0.0;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies that `out` follows `ctrl` and that `metric` reports the selected AC phase state. AC small-signal phase behavior itself requires an AC-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `ac_stim_phase_selector.va`.
