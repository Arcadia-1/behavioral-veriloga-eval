# File Rewind Second Pass

Implement one behavioral Verilog-A source file named `file_rewind_second_pass.va`.

## Interface

Use this exact module interface:

```verilog
module file_rewind_second_pass (
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

Use `$fopen()`, `$fgets(line, fd)`, `$rewind()`, and `$fclose()` in `initial_step` file-read initialization logic. The solution must read `config_lines.txt`.

Required behavior:

- read the first two lines into `line0` and `line1`;
- call `$rewind(fd)`;
- read one more line into `line_again`;
- set `rewind_hit_q = 1` only when `line0 == "gain=0.8"`, `line1 == "mode=1"`, and `line_again == "gain=0.8"`;
- set `metric_v = vhi` when `rewind_hit_q == 1`, otherwise `0.0`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when `rewind_hit_q == 1` and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `file_rewind_second_pass.va`.
