# Hierarchy Named Port Map

Implement one behavioral Verilog-A source file named `hierarchy_named_port_map.va`.

## Interface

Use this exact module interface:

```verilog
module hierarchy_named_port_map (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use named port mapping for a child module instance.

Required behavior:

- use the provided support module `v3_child_gain`;
- instantiate `v3_child_gain` as `u1` with named port mapping;
- connect `.out(out)` and `.vin(vin)` by name; the order may differ from the child module port declaration;
- preserve the support child gain behavior, so `V(out) = 0.8 * V(vin)`;
- leave `mid` unforced and drive `metric` from `V(mid)`, which should remain at 0.0 in this behavioral harness;
- do not introduce current contributions.

Return exactly one source artifact named `hierarchy_named_port_map.va`.
