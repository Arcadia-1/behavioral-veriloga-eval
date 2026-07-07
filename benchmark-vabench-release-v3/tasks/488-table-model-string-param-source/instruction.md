# Table Model String Param Source

## Task Contract

Implement one Verilog-A source file named `table_model_string_param_source.va`. This task exercises a `$table_model()` data source supplied through a string parameter.

This is a Verilog-A semantic/support task. The table data source must be named by the string parameter and then passed to `$table_model()`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module table_model_string_param_source(
    input electrical in,
    output electrical out
);
```

The support table file `gain_profile.tbl` is supplied by the task harness and must be available at simulation time.

## Public Parameter Contract

Declare `parameter string tmdata = "gain_profile.tbl";`. The parameter names the table file used by `$table_model()`.

## Required Behavior

Evaluate `$table_model(V(in), tmdata, "1L")` and drive `out` with the returned value. The supplied support table maps `0.0` to `0.1`, `0.5` to `0.6`, and `1.0` to `1.1`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `table_model_string_param_source.va`.
