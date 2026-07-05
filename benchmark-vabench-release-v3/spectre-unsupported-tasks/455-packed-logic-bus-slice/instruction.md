# Packed Logic Bus Slice

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `packed_logic_bus_slice.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module packed_logic_bus_slice(input [7:0] a, output [3:0] y);
    logic a;
    logic y;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Required behavior:

- declare an 8-bit logic input bus;
- declare a 4-bit logic output bus;
- use bit select or part select on the input bus;
- use concatenation to build the output bus;
- continuously assign `{a[7:6], a[1:0]}` to `y`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital logic-vector construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `packed_logic_bus_slice.vams`.
