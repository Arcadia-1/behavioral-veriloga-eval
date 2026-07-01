# Fstrobe File Line Writer

Implement one behavioral Verilog-A/AMS source file named `fstrobe_file_line_writer.va`.

## Interface

Use this exact module interface:

```verilog
module fstrobe_file_line_writer (
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

Use $fstrobe() to write a formatted line to a file handle.

Required behavior:

- open `fstrobe_lines.log` with `$fopen` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise set `out_v` to `vhi` when `V(vin) > vth`, else 0.0;
- set `metric_v` to the current `count_q`;
- call `$fstrobe(fd, ...)` with a formatted line containing the count and output value;
- increment `count_q` after writing;
- close the file handle at `final_step`;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `fstrobe_file_line_writer.va`.
