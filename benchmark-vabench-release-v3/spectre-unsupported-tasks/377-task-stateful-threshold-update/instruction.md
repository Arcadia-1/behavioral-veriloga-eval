# Task Stateful Threshold Update

Implement one behavioral Verilog-A source file named `task_stateful_threshold_update.va`.

## Interface

Use this exact module interface:

```verilog
module task_stateful_threshold_update (
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

Use a task named `threshold_update` to update state from thresholded analog inputs:

```verilog
task threshold_update;
    input real sample;
    input integer raise_mode;
```

Maintain a module-level real state `threshold_q`, initialized to `vth`. On each rising crossing of `clk`, reset `threshold_q` to `vth` and both outputs to zero if `rst > vth`; otherwise call `threshold_update(V(vin), V(mode) > vth)`.

The task must:

- compare `sample` against the current `threshold_q` before changing the threshold;
- drive `out_v = vhi` when `sample > threshold_q`, otherwise `0.0`;
- drive `metric_v = threshold_q`;
- when `raise_mode != 0`, increase `threshold_q` by `0.1` after the comparison, clamped to at most `0.75`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_stateful_threshold_update.va`.
