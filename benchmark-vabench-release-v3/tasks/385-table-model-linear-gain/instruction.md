# Table Model Linear Gain

## Task Contract

Implement one behavioral Verilog-A source file named `table_model_linear_gain.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_linear_gain (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use `$table_model()` for a one-dimensional linear gain lookup. The solution must read `table-model-linear-gain.tbl`.

Required behavior:

- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-linear-gain.tbl")`;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `table_model_linear_gain.va`.
