# Fstrobe File Line Writer

## Task Contract

Implement one behavioral Verilog-A source file named `fstrobe_file_line_writer.va`. This is a language-extension/L0 support task for Spectre-compatible `$fstrobe()` file-output syntax on a clocked voltage-domain update path, not a standalone core circuit macro.

Use `$fopen` at `initial_step` to open `fstrobe_lines.log`, use `$fstrobe(fd, ...)` on each non-reset sampled update to write a formatted line containing the count and output value, and close the handle with `$fclose` at `final_step`. The file-output side effect is part of the language-semantics contract but must not change the voltage-domain output behavior.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high outputs near `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

- Initialize `out_v`, `metric_v`, `count_q`, and the file handle at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise set `out_v` to `vhi` when `V(vin) > vth`, else `0.0`.
- Set `metric_v` to the current `count_q` value before incrementing it.
- Call `$fstrobe(fd, ...)` with a formatted line containing the count and output value.
- Increment `count_q` after writing the line.
- Close the file handle at `final_step`.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. The log file is an auxiliary simulator side effect; the voltage-domain outputs must be determined by the sampled input/reset state and the public parameter contract.

## Output Contract

Return exactly one source artifact named `fstrobe_file_line_writer.va`.
