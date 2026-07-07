# Vector Concat Code Build

## Task Contract

Implement one behavioral Verilog-A source file named `vector_concat_code_build.va`. The model is a clocked compact-code generator that reports the generated code and asserts an analog high level for codes above the threshold.

This is a DUT task. Keep the implementation behavioral, voltage-domain, and event-driven; do not add branch-current contributions or extra modules.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module vector_concat_code_build (
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

Initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`. On each rising crossing of `V(clk) - vth`, reset `out_v`, `metric_v`, and `count_q` when `V(rst) > vth`. Otherwise, build a compact integer code whose upper prefix is binary `10` and whose two low bits follow the low two bits of `count_q`; equivalently for this nonnegative counter, the observable code sequence is `8, 9, 10, 11` repeating. Drive `out_v = vhi` when the code is greater than 8 and `0.0` otherwise, report the code value on `metric_v`, and increment `count_q` after computing the outputs.

## Modeling Constraints

Implement the compact-code behavior with Spectre-portable integer arithmetic rather than simulator-sensitive integer concatenation or integer bit-select syntax. Drive `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Output Contract

Return exactly one source artifact named `vector_concat_code_build.va`.
