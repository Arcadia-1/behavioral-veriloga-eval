# File Fgets Config Loader

Implement one behavioral Verilog-A source file named `file_fgets_config_loader.va`.

## Interface

Use this exact module interface:

```verilog
module file_fgets_config_loader (
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

Use `$fopen()`, `$fgets()`, and `$fclose()` in `initial_step` configuration loading. The solution must read `config_lines.txt`.

Required behavior:

- call `$fgets(line, fd)` twice to load the first two configuration lines;
- set `loaded_q = 1` only when both loaded strings are non-empty;
- set `metric_v = vhi` when `loaded_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `loaded_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_fgets_config_loader.va`.
