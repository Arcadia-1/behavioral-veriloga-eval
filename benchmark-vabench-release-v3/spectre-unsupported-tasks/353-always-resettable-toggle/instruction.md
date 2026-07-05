# Always Resettable Toggle

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `always_resettable_toggle.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module always_resettable_toggle(clk, rst, d, en, q);
    input clk, rst, d, en;
    output q;
    logic clk, rst, d, en, q;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Use edge-triggered `always` logic with asynchronous reset:

```verilog
always @(posedge clk or posedge rst)
```

When `rst` is high, clear `q` to `1'b0`. Otherwise, when both `en` and `d` are high on a positive clock edge, toggle `q` using logical `!q`; when either control is low, hold the previous value.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital always-block construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `always_resettable_toggle.vams`.
