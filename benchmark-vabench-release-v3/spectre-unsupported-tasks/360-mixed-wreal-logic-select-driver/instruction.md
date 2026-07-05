# Mixed Wreal Logic Select Driver

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `mixed_wreal_logic_select_driver.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module mixed_wreal_logic_select_driver(vin, clk, en, sel, a, b, vout);
    input vin, clk, en, sel, a, b;
    output vout;
    electrical vin, vout;
    logic clk, en, sel;
    wreal a, b;
```

## Public Parameter Contract

Preserve these public parameter declarations and default values:

```verilog
parameter real tr = 200p;
```

## Required Behavior

Implement this exact interface:

```verilog
module mixed_wreal_logic_select_driver(vin, clk, en, sel, a, b, vout);
    input vin, clk, en, sel, a, b;
    output vout;
    electrical vin, vout;
    logic clk, en, sel;
    wreal a, b, level;
```

Use a continuous assignment to select between the two wreal inputs:

```verilog
assign level = sel ? a : b;
```

Drive the electrical output with the selected level through a smooth behavioral voltage contribution:

```verilog
V(vout) <+ transition(level, 0.0, tr, tr);
```

The output must follow `b` while `sel` is low and `a` while `sel` is high. The unused ports are part of the mixed-signal interface contract and must remain present.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a mixed logic/wreal/electrical construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `mixed_wreal_logic_select_driver.vams`.
