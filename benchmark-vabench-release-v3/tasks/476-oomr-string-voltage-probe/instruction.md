# OOMR String Voltage Probe

## Task Contract

Implement one Verilog-A source file named `oomr_string_voltage_probe.va`. This task exercises a string out-of-module reference used as a voltage probe target.

This is a Verilog-A semantic/support task. The observable behavior must come from the string OOMR voltage probe, not from an ordinary input port added to the module.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module oomr_string_voltage_probe(
    output electrical out
);
```

## Public Parameter Contract

Declare `parameter string sigpath = "$root.vin";`. The parameter names the external voltage node that the model probes.

## Required Behavior

Probe the referenced node with `V(sigpath)` and drive `out` with the probed voltage.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Do not add ordinary electrical input ports or bypass the string OOMR probe.

## Output Contract

Return exactly one source artifact named `oomr_string_voltage_probe.va`.
