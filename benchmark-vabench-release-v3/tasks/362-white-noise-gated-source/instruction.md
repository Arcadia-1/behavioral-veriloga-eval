# White Noise Gated Source

Implement one behavioral Verilog-A source file named `white_noise_gated_source.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module white_noise_gated_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Gate `white_noise()` with the control voltage:

```verilog
V(out) <+ (V(ctrl) > vth ? white_noise(noise_power, "gated_white") : 0.0);
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `vhi` when `ctrl` is above `vth`, otherwise to zero:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = V(ctrl) > vth ? vhi : 0.0;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked gate-status sideband. The noise source is covered as an executable language feature; spectral noise power requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `white_noise_gated_source.va`.
