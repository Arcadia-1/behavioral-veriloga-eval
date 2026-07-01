# Analysis Aware Noise Metric

Implement one behavioral Verilog-A source file named `analysis_aware_noise_metric.va`.

This is a noise/analysis extension task based on the Cadence Verilog-A Language Reference. It intentionally exercises noise or analysis-dependent source functions. These tasks may require an AC/noise-capable simulator such as Spectre for final certification.

## Interface

```verilog
module analysis_aware_noise_metric (
    input  electrical ctrl,
    input  electrical clk,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `analysis()` and a noise contribution while maintaining deterministic transient outputs:

```verilog
V(out) <+ transition(V(ctrl), 0.0, tr, tr);
if (analysis("noise")) V(out) <+ white_noise(noise_power, "metric_noise");
```

Also provide a transient-checkable metric counter. Initialize `metric_v` and `count_q` to zero at `initial_step`; on every rising crossing of `clk` through `vth`, increment `count_q` and update `metric_v` to `count_q / 8.0`:

```verilog
@(cross(V(clk)-vth,+1)) begin
    count_q = count_q + 1;
    metric_v = count_q / 8.0;
end
V(metric) <+ transition(metric_v, 0.0, tr, tr);
```

The transient checker verifies that `out` follows `ctrl` and that `metric` advances by one eighth per sampled clock edge. Noise-analysis behavior itself requires a noise-analysis-capable certification layer.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `analysis_aware_noise_metric.va`.
