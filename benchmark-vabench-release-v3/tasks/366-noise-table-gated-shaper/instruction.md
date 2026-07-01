# Noise Table Gated Shaper

Implement one behavioral Verilog-A source file named `noise_table_gated_shaper.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module noise_table_gated_shaper (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Gate a `noise_table()` contribution with the control voltage:

```verilog
V(out) <+ (V(ctrl) > vth ? noise_table("noise_profile.tbl", "profile_noise") : 0.0);
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `vhi` when `ctrl` enables the table-defined noise source, otherwise to zero:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = V(ctrl) > vth ? vhi : 0.0;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies the clocked gate-status sideband. The table-defined noise source is covered as an executable language feature; spectral noise behavior requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `noise_table_gated_shaper.va`.
