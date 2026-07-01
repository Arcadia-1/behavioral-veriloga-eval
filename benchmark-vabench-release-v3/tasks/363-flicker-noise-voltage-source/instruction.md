# Flicker Noise Voltage Source

Implement one behavioral Verilog-A source file named `flicker_noise_voltage_source.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module flicker_noise_voltage_source (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `flicker_noise()` as a behavioral 1/f noise contribution on `out`:

```verilog
V(out) <+ flicker_noise(kf, af, "flicker_voltage_noise");
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `kf * 1.0e12`:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = kf * 1.0e12;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked parameter sideband. The flicker noise source is covered as an executable language feature; spectral 1/f behavior requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `flicker_noise_voltage_source.va`.
