# Task Event Counter Service

Implement one behavioral Verilog-A source file named `task_event_counter_service.va`.

## Interface

Use this exact module interface:

```verilog
module task_event_counter_service (
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

Use a task named `service_event` to update counter state on clock crossings:

```verilog
task service_event;
    input real sample;
    input integer enabled;
```

On each rising crossing of `clk`, if `rst > vth`, reset `count_q`, `sum_v`, `out_v`, and `metric_v` to zero. Otherwise call `service_event(V(vin), V(mode) > vth)`.

The task must:

- increment `count_q` only when `enabled != 0`;
- add `sample` to `sum_v` only when the event is enabled;
- set `out_v = min(vhi, 0.15 * count_q)`;
- set `metric_v = sum_v / count_q` when `count_q > 0`, otherwise `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_event_counter_service.va`.
