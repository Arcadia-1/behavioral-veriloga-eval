# Hierarchy Ordered Port Map

## Task Contract

Implement one behavioral Verilog-A source file named `hierarchy_ordered_port_map.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module hierarchy_ordered_port_map (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use ordered port mapping for child module instances.

Required behavior:

- use the provided support module `v3_child_gain`;
- declare an internal electrical node named `mid`;
- instantiate `u1` as `v3_child_gain u1(vin, mid)` using ordered port mapping;
- instantiate `u2` as `v3_child_gain #(.gain(0.5)) u2(mid, out)` using ordered port mapping;
- therefore produce `V(mid) = 0.8 * V(vin)` and `V(out) = 0.5 * V(mid)`;
- drive `metric` from `V(mid)` through `transition(...)`;
- do not introduce current contributions.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `hierarchy_ordered_port_map.va`.
