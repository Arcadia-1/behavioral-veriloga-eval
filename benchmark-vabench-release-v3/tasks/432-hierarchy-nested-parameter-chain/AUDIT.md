# Audit: Hierarchy Nested Parameter Chain

- Task id: `v3_432_hierarchy_nested_parameter_chain`
- Category: `veriloga_hierarchy_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises reuse of a supplied child module twice with distinct parameter overrides across a two-stage voltage chain.
- Duplicate boundary: distinct from `431-hierarchy-support-artifact-staging` because this row checks repeated use of the same child with parameter propagation rather than staging a gain child into a limiter child.
- Prompt status: updated to mandatory vaBench v3 section format and explicit target/support boundary.
- Reference artifact: parent source instantiates `staged_gain_child` twice with gains 1.2 and 0.5; support file remains a supplied artifact.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- Validation: EVAS reference run 7/7 PASS across S2 and 35/35 negative variants rejected; targeted Spectre visible/private reference runs 7/7 PASS and private negative variants 35/35 rejected; AHDL preflight 14/14 PASS with zero task-specific diagnostics.
