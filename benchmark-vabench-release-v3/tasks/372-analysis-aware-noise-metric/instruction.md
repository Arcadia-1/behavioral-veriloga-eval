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

Use analysis() and noise contribution while maintaining a transient metric output.

Keep the model behavioral and voltage-domain. Do not use current-domain `I(...)` contributions or transistor-level devices.

## Output

Return exactly one source artifact named `analysis_aware_noise_metric.va`.
