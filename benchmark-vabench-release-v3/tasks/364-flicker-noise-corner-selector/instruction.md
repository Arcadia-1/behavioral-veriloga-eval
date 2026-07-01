# Flicker Noise Corner Selector

Implement one behavioral Verilog-A source file named `flicker_noise_corner_selector.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module flicker_noise_corner_selector (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Select `flicker_noise()` strength with the control voltage:

```verilog
V(out) <+ flicker_noise(V(ctrl) > vth ? kf_hi : kf_lo, 1.0, "corner_select");
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `vhi` when `ctrl` selects the high-noise corner, otherwise to zero:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = V(ctrl) > vth ? vhi : 0.0;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked corner-select sideband. The flicker noise source is covered as an executable language feature; spectral 1/f behavior requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `flicker_noise_corner_selector.va`.
