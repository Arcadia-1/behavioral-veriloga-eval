# Hierarchy Support Artifact Staging

Implement one behavioral Verilog-A source file named `hierarchy_support_artifact_staging.va`.
The test harness also supplies read-only support child modules in
`staged_gain_child.va` and `staged_limit_child.va`.

## Interface

Use this exact module interface:

```verilog
module hierarchy_support_artifact_staging (
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

Use a parent module plus staged child modules supplied as support artifacts.

Required behavior:

- define the top module `hierarchy_support_artifact_staging`;
- instantiate `staged_gain_child` from the parent with a parameter override `gain=0.75`;
- instantiate `staged_limit_child` after the gain stage;
- connect the parent input `vin` through the gain child into an internal electrical node such as `mid`;
- drive `metric` from the gained intermediate value `V(mid)`;
- drive `out` from the limiter output, clamping the gained value to 0.9 V;
- keep the implementation behavioral and avoid current contributions.

Return exactly one source artifact named `hierarchy_support_artifact_staging.va`.
