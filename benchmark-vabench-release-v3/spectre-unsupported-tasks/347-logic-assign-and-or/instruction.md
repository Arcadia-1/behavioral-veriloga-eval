# Logic Assign And Or

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `logic_assign_and_or.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module logic_assign_and_or(a, b, en, y);
    input a, b, en;
    output y;
    logic a, b, en, y;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Use `logic` nets and a bitwise continuous `assign`.

Drive `y` with one continuous assignment:

```verilog
assign y = (a & b) | en;
```

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a digital logic/assign construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `logic_assign_and_or.vams`.
