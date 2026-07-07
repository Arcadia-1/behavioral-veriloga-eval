# File Fgets Config Loader

## Task Contract

Implement one behavioral Verilog-A source file named `file_fgets_config_loader.va`.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use `$fopen()`, `$fgets()`, and `$fclose()` in `initial_step` configuration loading. The solution must read `config_lines.txt`.

Required behavior:

- call `$fgets(line, fd)` twice to load the first two configuration lines;
- set `loaded_q = 1` only when both loaded strings are non-empty;
- set `metric_v = vhi` when `loaded_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `loaded_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `file_fgets_config_loader.va`.
