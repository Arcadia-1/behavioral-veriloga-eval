# Final Step File Metric

Implement `final_step_file_metric_ref.va` in Verilog-A.

## Interface

```verilog
module final_step_file_metric_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical ref,
    output electrical metric_out
);
```

## Required Behavior

Write a pure voltage-domain measurement helper that counts rising reference
events during transient simulation, exposes a voltage-coded metric, and writes
the final metric at `final_step`.

Public parameters:

- `vth = 0.45 V`: rising-crossing threshold for `ref` relative to `VSS`.
- `tedge = 200 ps`: rise/fall smoothing for `metric_out`.

Required observable behavior:

- Initialize the event count and metric to zero.
- On every rising crossing of `ref` through `vth`, increment the event count.
- Expose the normalized metric as `metric_out = V(VDD,VSS) * count / 4`.
- At `final_step`, write a text metric record containing the final count and
  normalized metric.

Use voltage-coded logic referenced to `VDD` and `VSS`. Smooth only event-updated
metric state; do not feed a continuously varying branch expression directly
into `transition()`. Do not generate a Spectre testbench, waveform files,
checker artifacts, transistor-level devices, current contributions, `ddt()`, or
`idt()`.

## Output

Return exactly one complete Verilog-A file named
`final_step_file_metric_ref.va`.
