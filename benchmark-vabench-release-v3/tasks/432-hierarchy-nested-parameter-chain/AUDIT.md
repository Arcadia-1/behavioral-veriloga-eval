# Audit: Hierarchy Nested Parameter Chain

- Task id: `v3_432_hierarchy_nested_parameter_chain`
- Category: `veriloga_hierarchy_semantics`
- Required syntax focus: `Use nested child module instances with parameter overrides across two stages.`
- EVAS status: `pending EVAS issue #41: https://github.com/Arcadia-1/EVAS/issues/41: https://github.com/Arcadia-1/EVAS/issues/41`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: executable hierarchy candidate staged with visible/hidden benches and checker; behavior certification is blocked by same-source child module lookup support.
