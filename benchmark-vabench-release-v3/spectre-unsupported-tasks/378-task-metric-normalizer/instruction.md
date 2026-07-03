# Task Metric Normalizer

Implement one behavioral Verilog-A source file named `task_metric_normalizer.va`.

## Interface

Use this exact module interface:

```verilog
module task_metric_normalizer (
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

Use a task named `normalize_metric` to normalize a computed metric into a voltage-domain output:

```verilog
task normalize_metric;
    input real sample;
    input real norm_span;
```

On each rising crossing of `clk`, if `rst > vth`, reset both output states to zero. Otherwise call `normalize_metric(V(vin), V(mode) > vth ? vhi : vth)`.

The task must:

- clamp `sample` into `[0.0, vhi]` and assign it to `out_v`;
- compute `raw_metric = abs(sample - vth)`;
- compute `metric_v = vhi * raw_metric / norm_span`;
- clamp `metric_v` into `[0.0, vhi]`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `task_metric_normalizer.va`.
