# Wreal Threshold Flag

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `wreal_threshold_flag.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module wreal_threshold_flag(a, b, sel, y);
    input a, b, sel;
    output y;
    wreal a, b, sel, y;
```

## Public Parameter Contract

Preserve these public parameter declarations and default values:

```verilog
parameter real gain = 0.75;
parameter real offset = 0.1;
parameter real threshold = 0.45;
parameter real high = 0.9;
parameter real low = 0.0;
```

## Required Behavior

Use `wreal` threshold logic with a continuous `assign`.

Declare:

```verilog
parameter real offset = 0.1;
parameter real threshold = 0.45;
parameter real high = 0.9;
parameter real low = 0.0;
```

Drive `y` with one continuous assignment:

1. When `sel <= threshold`, compare `a` directly against `threshold`.
2. When `sel > threshold`, compare `a + offset` against `threshold`.
3. Drive `high` when the selected value is above threshold, otherwise drive `low`.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a Verilog-AMS/wreal construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `wreal_threshold_flag.vams`.
