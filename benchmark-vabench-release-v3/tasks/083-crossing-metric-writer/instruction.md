# Crossing Metric Writer

Implement `file_metric_writer.va` in Verilog-A.

## Interface

```verilog
module file_metric_writer(vin, done);
```

Inputs:

- `vin`: electrical input being monitored.

Outputs:

- `done`: electrical completion flag.

## Required Behavior

Write a pure voltage-domain measurement helper that records the first rising
threshold crossing of `vin`.

Public parameters:

- `filename = "metric.out"`: text file opened by the model at startup.
- `vth = 0.45 V`: rising-crossing threshold for `vin`.
- `tr = 300 ps`: rise/fall smoothing for `done`.

Required observable behavior:

- Open `filename` on `initial_step`.
- On the first rising crossing of `vin` through `vth`, write the crossing time
  to the metric file and latch completion.
- Keep `done` low before the first crossing and high after completion.
- Ignore later crossings after the first recorded event.

Use voltage contributions only. Smooth the `done` output with `transition()`.
Do not generate a Spectre testbench, waveform files, checker artifacts,
transistor-level devices, current contributions, `ddt()`, or `idt()`.

## Output

Return exactly one complete Verilog-A file named `file_metric_writer.va`.
