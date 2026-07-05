# Logic Vector Reduction Flag

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `logic_vector_reduction_flag.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module logic_vector_reduction_flag(input [3:0] code, output valid);
    logic code;
    logic valid;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Use logic vector reduction in a continuous assignment.

Required behavior:

- declare `logic [3:0] code`;
- declare scalar `logic valid`;
- continuously assign `valid = |code`;
- `valid` must be low only when all four bits of `code` are low;
- `valid` must be high when any one or more bits of `code` are high.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital logic-vector construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `logic_vector_reduction_flag.vams`.
