# Event Task Function State Update

Implement one Verilog-A source file named `event_task_function_state_update.va`.

## Required Feature

Combine event body, task state update, and function post-processing.

## Required Interface

```verilog
module event_task_function_state_update(
    input electrical clk,
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Maintain an integer `count` and real state `q`.
- Define a user function `clamp01` that clamps a real value into `[0.0, 1.0]`.
- Define a task `update_state` with one real input `sample`.
- On every `cross(V(clk) - 0.45, +1)`, call `update_state(V(in))`.
- The task must increment `count` and set `q = clamp01(sample + 0.05 * count)`.
- Drive `out` with `q` using `transition(..., 0, 200p, 200p)`.

Return exactly one source artifact named `event_task_function_state_update.va`.
