# File Feof Line Counter

## Task Contract

Implement one behavioral Verilog-A source file named `file_feof_line_counter.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module file_feof_line_counter (
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

Use `$fopen()`, `$feof()`, `$fgets(line, fd)`, and `$fclose()` in `initial_step` file-read initialization logic. The solution must read `config_lines.txt`.

Required behavior:

- loop while `!$feof(fd)` and the line count is below four;
- call `$fgets(line_buf, fd)` inside the loop;
- increment `line_count_q` once per non-empty loaded line;
- after closing the file, set `metric_v = clamp(vhi * line_count_q / 2.0, 0.0, vhi)`;
- on each rising crossing of `clk`, reset `out_v` to zero when `rst > vth`;
- otherwise drive `out_v = vhi` only when exactly two lines were counted and `V(vin) > vth`, else `0.0`.

Drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `file_feof_line_counter.va`.
