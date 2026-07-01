# Ac Stim Small Signal Source

Implement one behavioral Verilog-A source file named `ac_stim_small_signal_source.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module ac_stim_small_signal_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `ac_stim()` for small-signal AC stimulus while retaining transient behavior:

```verilog
V(out) <+ transition(V(ctrl), 0.0, tr, tr);
if (analysis("ac")) V(out) <+ ac_stim("ac", mag, phase_deg);
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `mag`:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = mag;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies that `out` follows `ctrl` and that `metric` reports the configured AC magnitude. AC small-signal behavior itself requires an AC-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `ac_stim_small_signal_source.va`.
