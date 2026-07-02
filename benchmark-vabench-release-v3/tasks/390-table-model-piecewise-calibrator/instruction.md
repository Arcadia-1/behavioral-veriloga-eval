# Table Model Piecewise Calibrator

Implement one behavioral Verilog-A source file named `table_model_piecewise_calibrator.va`.

## Interface

Use this exact module interface:

```verilog
module table_model_piecewise_calibrator (
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

Use `$table_model()` as a piecewise calibration primitive. The solution must read `table-model-piecewise-calibrator.tbl`.

Required behavior:

- treat `V(vin)` as a raw normalized code coordinate;
- initialize `out_v` and `metric_v` to `0.0`;
- on each rising crossing of `clk`, reset `out_v` and `metric_v` to zero when `rst > vth`;
- otherwise set `out_v = $table_model(V(vin), "table-model-piecewise-calibrator.tbl")`;
- use the table to apply a nonuniform piecewise calibration curve;
- set `metric_v = out_v / vhi`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `table_model_piecewise_calibrator.va`.
