# Analysis Dependent Dc Tran Mode

Implement one behavioral Verilog-A source file named `analysis_dependent_dc_tran_mode.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module analysis_dependent_dc_tran_mode (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `analysis()` to choose DC versus transient behavior:

```verilog
if (analysis("dc")) out_drive_v = 0.25;
else if (analysis("tran")) out_drive_v = V(ctrl);
else out_drive_v = 0.0;
V(out) <+ transition(out_drive_v, 0.0, tr, tr);
```

Also provide a deterministic transient-checkable sideband on `metric`. Initialize `metric_v` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, update `metric_v` to `vhi` when the current analysis is transient, otherwise zero:

```verilog
@(cross(V(clk)-vth,+1)) metric_v = analysis("tran") ? vhi : 0.0;
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

In a transient run, `out` must follow `ctrl` and `metric` must report `vhi` after each sampled clock edge.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `analysis_dependent_dc_tran_mode.va`.
