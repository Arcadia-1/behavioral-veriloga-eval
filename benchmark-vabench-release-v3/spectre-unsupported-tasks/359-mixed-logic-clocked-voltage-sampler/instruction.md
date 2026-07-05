# Mixed Logic Clocked Voltage Sampler

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `mixed_logic_clocked_voltage_sampler.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module mixed_logic_clocked_voltage_sampler(vin, clk, en, sel, a, b, vout);
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

Combine logic `always` sampling with an analog voltage output.

On every positive clock edge, sample `en` into the internal logic state:

```verilog
always @(posedge clk) sampled = en;
```

In the analog block, drive `V(vout)` from `V(vin)` when `sampled` is high and from `0.0` when it is low, using `transition(sampled ? V(vin) : 0.0, 0.0, tr, tr)`.

Use the module and port names from the starter. Do not use current-domain `I(...)` contributions or transistor-level primitives.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a mixed logic/wreal/electrical construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `mixed_logic_clocked_voltage_sampler.vams`.
