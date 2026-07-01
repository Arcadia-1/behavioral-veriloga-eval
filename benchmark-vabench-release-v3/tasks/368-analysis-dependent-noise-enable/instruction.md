# Analysis Dependent Noise Enable

Implement one behavioral Verilog-A source file named `analysis_dependent_noise_enable.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module analysis_dependent_noise_enable (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `analysis()` to enable a noise contribution only during noise analysis:

```verilog
V(out) <+ transition(0.0, 0.0, tr, tr);
if (analysis("noise")) V(out) <+ white_noise(noise_power, "enabled_noise");
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to the current control voltage:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = V(ctrl);
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked `metric` sideband and that the analysis-dependent noise form is executable. Noise-analysis behavior itself requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `analysis_dependent_noise_enable.va`.
