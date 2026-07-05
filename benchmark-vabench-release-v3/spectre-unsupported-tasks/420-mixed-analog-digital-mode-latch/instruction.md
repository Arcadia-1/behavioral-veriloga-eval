# Mixed Analog Digital Mode Latch

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `mixed_analog_digital_mode_latch.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module mixed_analog_digital_mode_latch(vin, clk, flag);
    input vin, clk;
    output flag;
    electrical vin;
    logic clk, flag;
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

Combine electrical threshold sampling with logic state output.

Required behavior:

- use `always @(posedge clk)`;
- on each rising clock edge, sample the electrical input with `V(vin)`;
- set `flag = 1'b1` when `V(vin) > 0.45` at that rising edge;
- set `flag = 1'b0` when `V(vin) <= 0.45` at that rising edge;
- hold the previous `flag` value between clock edges.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a mixed analog/digital latch outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `mixed_analog_digital_mode_latch.vams`.
