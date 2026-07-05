# Always Enable Saturating Counter

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `always_enable_saturating_counter.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module always_enable_saturating_counter(clk, rst, en, q);
    input clk, rst, en;
    output [1:0] q;
    logic clk, rst, en;
    logic q;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Use an always block for enabled saturating state update.

Required behavior:

- declare `logic clk, rst, en`;
- declare `logic [1:0] q`;
- use `always @(posedge clk)`;
- when `rst` is high at a rising clock edge, set `q = 2'b00`;
- when `rst` is low and `en` is high, increment `q` by one until it reaches `2'b11`;
- once `q` is `2'b11`, further enabled clock edges must hold it at `2'b11`;
- when `en` is low, hold the previous `q` value.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital always-block construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `always_enable_saturating_counter.vams`.
