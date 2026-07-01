# Noise Table Voltage Shaper

Implement one behavioral Verilog-A source file named `noise_table_voltage_shaper.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module noise_table_voltage_shaper (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `noise_table()` as a table-defined behavioral noise source on `out`:

```verilog
V(out) <+ noise_table("noise_profile.tbl", "profile_noise");
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `0.3 + V(ctrl) * 0.2`:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = 0.3 + V(ctrl) * 0.2;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked table-shaper sideband. The table-defined noise source is covered as an executable language feature; spectral noise behavior requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `noise_table_voltage_shaper.va`.
