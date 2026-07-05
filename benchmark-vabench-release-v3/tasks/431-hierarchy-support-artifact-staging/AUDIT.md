# Audit: Hierarchy Support Artifact Staging

- Task id: `v3_431_hierarchy_support_artifact_staging`
- Category: `veriloga_hierarchy_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises parent-module instantiation of two supplied support artifacts with a parameter override and an intermediate voltage metric.
- Duplicate boundary: distinct from `432-hierarchy-nested-parameter-chain` because this row stages two different support children, including a limiter child, rather than two instances of the same gain child.
- Prompt status: updated to mandatory vaBench v3 section format and explicit target/support boundary.
- Reference artifact: parent source instantiates `staged_gain_child #(.gain(0.75))` and `staged_limit_child`; support files remain supplied artifacts.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- Validation: EVAS reference run 7/7 PASS across S2 and 35/35 negative variants rejected; targeted Spectre visible/private reference runs 7/7 PASS and private negative variants 35/35 rejected; AHDL preflight 14/14 PASS with zero task-specific diagnostics.
