# Audit: Nested Function Pipeline

- Task id: `v3_457_nested_function_pipeline`
- Category: `veriloga_function_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises nested user-defined `analog function real` calls inside a continuous voltage-domain contribution.
- Duplicate boundary: retained as an atomic function-semantics row; it is not a separate AMS circuit macro.
- Prompt status: already used mandatory vaBench v3 section format; updated to make the L0/support boundary explicit.
- Reference artifact: two-port `vin/out` model computes `f1(V(vin))`, where `f1` calls `f2(x)` and adds 1.0.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- Public artifact fix: starter interface was corrected from an old six-port template to the public two-port `vin/out` interface used by the prompt and supplied testbenches.
- Validation: EVAS reference run 7/7 PASS across S2 and 35/35 negative variants rejected; targeted Spectre visible/private reference runs 7/7 PASS and private negative variants 35/35 rejected; AHDL preflight 14/14 PASS with zero task-specific diagnostics.
