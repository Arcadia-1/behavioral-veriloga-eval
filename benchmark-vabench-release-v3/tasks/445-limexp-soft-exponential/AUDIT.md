# Audit: Limexp Soft Exponential

- Task id: `v3_445_limexp_soft_exponential`
- Category: `veriloga_math_function_semantics`
- Gate 1 label: language-extension/L0 support row, not part of the original full-300 circuit-function claim.
- Independent value: exercises Spectre-compatible `limexp()` on a sampled voltage-domain transform.
- AMS-rescue note: `limexp()` is relevant to exponential device-style behavioral expressions, but this row intentionally remains voltage-domain and is not a diode/transistor current model.
- Prompt status: updated to mandatory vaBench v3 section format and explicit operator boundary.
- Reference artifact: computes `out_v = limexp(V(vin))`, mirrors it on `metric`, and removes the unused `vhi` parameter from starter/reference artifact.
- Boundary: behavioral voltage-domain modeling only; no `I(...)` current contribution.
- Validation: EVAS reference run 7/7 PASS across S2 and 35/35 negative variants rejected; targeted Spectre visible/private reference runs 7/7 PASS and private negative variants 35/35 rejected; AHDL preflight 14/14 PASS with zero task-specific diagnostics.
