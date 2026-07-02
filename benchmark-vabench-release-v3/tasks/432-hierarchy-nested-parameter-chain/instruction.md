# Hierarchy Nested Parameter Chain

Implement one behavioral Verilog-A source file named `hierarchy_nested_parameter_chain.va`.
The test harness also supplies the read-only support child module
`staged_gain_child.va`.

## Interface

Use this exact module interface:

```verilog
module hierarchy_nested_parameter_chain (
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

Use nested child module instances with parameter overrides across two stages.

Required behavior:

- define the top module `hierarchy_nested_parameter_chain`;
- instantiate the supplied reusable child gain module;
- instantiate two gain stages from the parent using named port maps;
- override the first child gain to 1.2 and the second child gain to 0.5;
- connect `vin -> gain0 -> mid -> gain1 -> out`;
- drive `metric` from the intermediate node `V(mid)`;
- keep the implementation behavioral and avoid current contributions.

Return exactly one source artifact named `hierarchy_nested_parameter_chain.va`.
