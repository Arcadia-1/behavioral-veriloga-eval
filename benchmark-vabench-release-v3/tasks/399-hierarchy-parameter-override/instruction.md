# Hierarchy Parameter Override

## Task Contract

Implement one behavioral Verilog-A source file named `hierarchy_parameter_override.va`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module hierarchy_parameter_override (
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

Override a child module parameter at instantiation.

Required behavior:

- use the provided support module `v3_child_gain`;
- instantiate `v3_child_gain` as `u1` with named port mapping;
- override the child parameter with `#(.gain(1.5))`;
- connect parent `vin` to child `vin` and parent `out` to child `out`;
- therefore produce `V(out) = 1.5 * V(vin)`;
- leave `mid` unforced and drive `metric` from `V(mid)`, which should remain at 0.0 in this behavioral harness;
- do not introduce current contributions.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `hierarchy_parameter_override.va`.
