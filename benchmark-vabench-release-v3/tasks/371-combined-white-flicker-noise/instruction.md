# Combined White Flicker Noise

Implement one behavioral Verilog-A source file named `combined_white_flicker_noise.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module combined_white_flicker_noise (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Combine `white_noise()` and `flicker_noise()` in one behavioral voltage source:

```verilog
V(out) <+ white_noise(white_pwr, "white") + flicker_noise(kf, 1.0, "flicker");
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to the normalized sum of the two noise-strength parameters:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = white_pwr * 1.0e12 + kf * 1.0e12;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked parameter sideband. The combined noise spectrum itself requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `combined_white_flicker_noise.va`.
