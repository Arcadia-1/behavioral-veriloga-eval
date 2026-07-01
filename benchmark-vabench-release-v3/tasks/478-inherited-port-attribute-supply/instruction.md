# Inherited Port Attribute Supply

Implement one Verilog-A source file named `inherited_port_attribute_supply.va`.

## Required Feature

Declare inherited terminal attributes on supply-like ports.

## Required Interface

```verilog
module inherited_port_attribute_supply(out, in, vdd, gnd);
```

## Required Behavior

- Declare `out` as output, `in` as input, and `vdd`/`gnd` as `inout` supply-like ports.
- Attach inherited connection attributes to `vdd` and `gnd` using `inh_conn_prop_name` and `inh_conn_def_value`.
- Drive `V(out, gnd)` from `V(in, gnd)` using `transition(..., 0, 200p, 200p)`.
- Use the inherited-port attribute syntax even when the testbench connects the supply ports explicitly.

Return exactly one source artifact named `inherited_port_attribute_supply.va`.
