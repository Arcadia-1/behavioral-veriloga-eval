# Vector Part Select Window

## Task Contract

Implement one behavioral Verilog-A source file named `vector_part_select_window.va`. The model is a clocked control-code window decoder with an analog voltage output and an analog metric output.

This is a DUT task. Keep the implementation behavioral, voltage-domain, and event-driven; do not add branch-current contributions or extra modules.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module vector_part_select_window (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. These parameters may be overridden by the testbench. Use `vth` for clock and reset thresholds, `vhi` for the high output level, and `tr` for output transitions.

## Required Behavior

Initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`. On each rising crossing of `V(clk) - vth`, reset `out_v`, `metric_v`, and `count_q` when `V(rst) > vth`. Otherwise, compute `code_q = count_q + 9`, derive a three-bit window equivalent to bits 3 down to 1 of that nonnegative code, drive `out_v = vhi` when the window is greater than 3 and `0.0` otherwise, report the window value on `metric_v`, and increment `count_q` after computing the outputs.

## Modeling Constraints

Implement the window extraction with Spectre-portable integer arithmetic rather than simulator-sensitive integer vector part-select syntax. Drive `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Output Contract

Return exactly one source artifact named `vector_part_select_window.va`.
