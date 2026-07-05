# Connectmodule Electrical Bridge

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `connectmodule_electrical_bridge.vams`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
connectmodule connectmodule_electrical_bridge(input electrical a, output electrical y);
```

## Public Parameter Contract

Preserve these public parameter declarations and default values:

```verilog
parameter real gain = 1.0;
```

## Required Behavior

Required behavior:

- declare a `connectmodule`;
- use electrical input/output ports;
- include a behavioral voltage bridge from input to output;
- keep current contributions out of the task.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Use the AMS/digital construct required by this archived row, such as `wreal`, `logic`, `assign`, `always`, `generate`, `connectmodule`, `connectrules`, or `specify`, only where it is part of the public contract.

This row remains archived because it uses a Verilog-AMS connectmodule construct outside the default standalone Spectre Verilog-A target. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `connectmodule_electrical_bridge.vams`.
