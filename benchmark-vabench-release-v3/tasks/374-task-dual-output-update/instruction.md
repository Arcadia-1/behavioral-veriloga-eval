# Task Dual Output Update

Implement one behavioral Verilog-A source file named `task_dual_output_update.va`.

## Interface

Use this exact module interface:

```verilog
module task_dual_output_update (
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

Use a task named `update_outputs` with two real inputs:

```verilog
task update_outputs;
    input real sample;
    input real trim;
```

On each rising crossing of `clk`, if `rst > vth`, reset both output states to zero. Otherwise call the task with `V(vin)` and `V(mode)`.

The task must compute:

- `out_v = clamp(sample + trim, 0.0, vhi)`
- `metric_v = clamp(sample - trim + 0.3, 0.0, vhi) / vhi`

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_dual_output_update.va`.
