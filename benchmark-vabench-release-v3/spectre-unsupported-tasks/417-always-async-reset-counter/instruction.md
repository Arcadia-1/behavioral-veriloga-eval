# Always Async Reset Counter

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `always_async_reset_counter.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module always_async_reset_counter(clk, rst, en, q);
    input clk, rst, en;
    output q;
    logic clk, rst, en;
    logic q;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Use an always block with asynchronous reset sensitivity.

Required behavior:

- declare `logic clk, rst, en`;
- declare scalar `logic q`;
- use `always @(posedge clk or posedge rst)`;
- if `rst` is high at a triggering event, drive `q = 1'b0`;
- otherwise, if `en` is high on a rising clock edge, toggle `q` with `q = ~q`;
- otherwise hold the previous value of `q`;
- a rising edge of `rst` must reset `q` even when there is no clock edge.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital always-block construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `always_async_reset_counter.vams`.
