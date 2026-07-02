# File Fopen Mode Selector

Implement one behavioral Verilog-A source file named `file_fopen_mode_selector.va`.

## Interface

Use this exact module interface:

```verilog
module file_fopen_mode_selector (
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

Use `$fopen()` mode selection with string-line ingestion. The solution must read `config_lines.txt`.

Required behavior:

- open `config_lines.txt` with explicit read mode `"r"`;
- read the first line using `$fgets(line_buf, fd)`;
- close the file with `$fclose(fd)`;
- set `mode_hit_q = 1` only when the loaded line is exactly `gain=0.8`;
- set `metric_v = vhi` when `mode_hit_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `mode_hit_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_fopen_mode_selector.va`.
