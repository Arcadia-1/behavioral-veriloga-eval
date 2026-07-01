# File Ftell Position Meter

Implement one behavioral Verilog-A source file named `file_ftell_position_meter.va`.

## Interface

Use this exact module interface:

```verilog
module file_ftell_position_meter (
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

Use `$fopen()`, `$fgets(line, fd)`, `$ftell()`, and `$fclose()` in `initial_step` file-read initialization logic. The solution must read `config_lines.txt`.

Required behavior:

- read the first line with `$fgets(line_buf, fd)`;
- call `$ftell(fd)` after that read;
- set `position_hit_q = 1` only when the file position is exactly `9`;
- set `metric_v = vhi` when `position_hit_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `position_hit_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_ftell_position_meter.va`.
