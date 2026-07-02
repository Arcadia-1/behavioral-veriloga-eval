# Parameter Range Real Control

Implement one behavioral Verilog-A source file named `parameter_range_real_control.va`.

## Interface

Use this exact module interface:

```verilog
module parameter_range_real_control (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use parameter range constraints for real-valued controls.

Required behavior:

- declare `parameter real gain_limited = 0.8 from [0.0:2.0]`;
- declare `parameter integer max_count = 8 from [1:32]`;
- initialize `count_q = 0`, `out_v = 0.0`, `metric_v = 0.0`, and `state_q = 0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and `state_q` when `rst > vth`;
- otherwise update `count_q = (count_q + 1) % max_count`;
- set `out_v = gain_limited * V(vin)`;
- set `metric_v = count_q`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `parameter_range_real_control.va`.
