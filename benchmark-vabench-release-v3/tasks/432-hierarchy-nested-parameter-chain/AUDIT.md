# Audit: Hierarchy Nested Parameter Chain

- Task id: `v3_432_hierarchy_nested_parameter_chain`
- Category: `veriloga_hierarchy_semantics`
- Required syntax focus: `Use nested child module instances with parameter overrides across two stages.`
- EVAS status: `behavior-certified`
- Score claim: `extension_behavior_certified_outside_original_300`.

## Behavior Certification

- Checker: `hierarchy_nested_parameter_chain_contract`.
- Required behavior: two staged child instances apply their parameter overrides in sequence and expose the intermediate metric.
- Visible/hidden coverage: hidden stimulus varies input and reset windows to catch missing child lookup, wrong parameter override, and metric-only mistakes.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Evidence: `benchmark-vabench-release-v3/reports/verify_301_497_layered.json`.

## Boundary

This task certifies the benchmark's support-artifact hierarchy contract and transient behavior checker. It does not expand the original full-300 denominator.
