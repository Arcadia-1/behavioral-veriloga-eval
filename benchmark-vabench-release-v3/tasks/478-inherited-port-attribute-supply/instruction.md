# Inherited Port Attribute Supply

## Task Contract

Implement one Verilog-A source file named `inherited_port_attribute_supply.va`. This task exercises inherited connection attributes on supply-like ports while preserving explicit supply-pin behavior.

This is a Verilog-A semantic/support task. Keep the inherited connection attributes on the supply ports even when the testbench connects the supplies explicitly.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module inherited_port_attribute_supply(out, in, vdd, gnd);
```

Declare `out` as output, `in` as input, and `vdd`/`gnd` as `inout` supply-like electrical ports.

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

Attach inherited connection attributes to `vdd` and `gnd` using `inh_conn_prop_name` and `inh_conn_def_value`. Drive `V(out, gnd)` from `V(in, gnd)`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` on the output contribution. Use voltage-domain behavior and do not use current contributions.

## Output Contract

Return exactly one source artifact named `inherited_port_attribute_supply.va`.
