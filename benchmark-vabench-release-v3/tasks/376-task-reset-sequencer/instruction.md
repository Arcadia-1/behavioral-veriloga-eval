# Task Reset Sequencer

Implement one behavioral Verilog-A source file named `task_reset_sequencer.va`.

## Interface

Use this exact module interface:

```verilog
module task_reset_sequencer (
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

Use a task named `sequence_update` to share reset and normal update sequencing:

```verilog
task sequence_update;
    input real sample;
    input integer reset_active;
    input integer boost_mode;
```

On every rising crossing of `clk`, call `sequence_update(V(vin), V(rst) > vth, V(mode) > vth)`.

The task must:

- when `reset_active != 0`, set `phase_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- otherwise increment `phase_q`;
- set `out_v = sample + 0.2` when `boost_mode != 0`, otherwise `sample`;
- clamp `out_v` into `[0.0, vhi]`;
- set `metric_v = phase_q / 4.0` after a non-reset update.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_reset_sequencer.va`.
