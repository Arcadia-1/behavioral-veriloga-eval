# Hierarchy Support Artifact Staging

## Task Contract

Implement one behavioral Verilog-A source file named `hierarchy_support_artifact_staging.va`. This is a language-extension/L0 support task for hierarchy and support-artifact staging around a voltage-domain transfer path, not a standalone core circuit macro.

## Form-Specific Requirements

The public harness supplies read-only support child modules in `staged_gain_child.va` and `staged_limit_child.va`. Return only the parent source file and instantiate the supplied child modules from it.

## Public Verilog-A Interface

Use this exact parent module interface:

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

## Public Parameter Contract

The supplied `staged_gain_child` exposes a `gain` parameter; override it to `0.75` in the parent instance. The supplied `staged_limit_child` clamps the gained value to 0.9 V.

## Required Behavior

- Define the top module `hierarchy_support_artifact_staging`.
- Instantiate `staged_gain_child` from the parent with parameter override `gain=0.75`.
- Instantiate `staged_limit_child` after the gain stage.
- Connect the parent input `vin` through the gain child into an internal electrical node such as `mid`.
- Drive `metric` directly from the gained intermediate value `V(mid)`.
- Drive `out` from the supplied limiter child output, clamping the gained value to 0.9 V.

## Modeling Constraints

Keep the implementation behavioral and voltage-domain only. Do not introduce current contributions or redefine the supplied support modules in the returned artifact.

## Output Contract

Return exactly one source artifact named `hierarchy_support_artifact_staging.va`.
