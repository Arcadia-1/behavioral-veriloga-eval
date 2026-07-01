# File Fseek Offset Reader

Implement one behavioral Verilog-A source file named `file_fseek_offset_reader.va`.

## Interface

Use this exact module interface:

```verilog
module file_fseek_offset_reader (
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

Use `$fopen()`, `$fseek()`, `$fgets(line, fd)`, and `$fclose()` in `initial_step` file-read initialization logic. The solution must read `config_lines.txt`.

Required behavior:

- open `config_lines.txt`;
- call `$fseek(fd, 9, 0)` to skip the first line `gain=0.8`;
- call `$fgets(line_buf, fd)` after the seek;
- set `seek_hit_q = 1` only when the loaded line is exactly `mode=1`;
- set `metric_v = vhi` when `seek_hit_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `seek_hit_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_fseek_offset_reader.va`.
