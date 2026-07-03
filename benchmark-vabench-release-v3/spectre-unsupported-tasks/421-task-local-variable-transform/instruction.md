# Task Local Variable Transform

Implement one behavioral Verilog-A source file named `task_local_variable_transform.va`.

## Interface

Use this exact module interface:

```verilog
module task_local_variable_transform (
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

Use a task with an internal local variable before updating output and metric state.

Required behavior:

- declare real state variables for `out_v` and `metric_v`;
- implement a task named `update_with_local` that takes a real sample and declares a local real variable such as `clipped`;
- inside the task, clamp the sample to the range 0.0 to 0.9;
- set `out_v` to the clipped value and `metric_v` to `clipped / 0.9`;
- initialize `out_v` and `metric_v` to 0.0 at `initial_step`;
- on each rising `clk` crossing, reset both values to 0.0 when `rst` is high;
- otherwise call the task with `V(vin)`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_local_variable_transform.va`.
