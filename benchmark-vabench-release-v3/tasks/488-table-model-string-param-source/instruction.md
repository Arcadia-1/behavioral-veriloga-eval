# Table Model String Param Source

Implement one Verilog-A source file named `table_model_string_param_source.va`.

## Required Feature

Use a string parameter as the $table_model() data source.

## Required Interface

```verilog
module table_model_string_param_source(
    input electrical in,
    output electrical out
);
```

## Required Behavior

- Declare `parameter string tmdata = "gain_profile.tbl";`.
- Use `$table_model(V(in), tmdata, "1L")` to read the table data through that string parameter.
- Drive `out` with the returned table value using `transition(..., 0, 200p, 200p)`.
- The supplied `gain_profile.tbl` maps `0.0 -> 0.1`, `0.5 -> 0.6`, and `1.0 -> 1.1`.

Return exactly one source artifact named `table_model_string_param_source.va`.
