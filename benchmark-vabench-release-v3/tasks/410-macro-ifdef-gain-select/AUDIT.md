# Audit: Macro Ifdef Gain Select

- Task id: `v3_410_macro_ifdef_gain_select`
- Category: `veriloga_preprocessor_control_semantics`
- Required syntax focus: `Use `ifdef selection to alter a behavioral gain constant.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: language extension candidate pending full behavioral certification.
- Blocking issue: local `define/`ifdef support is not yet behavior-certified in EVAS; see https://github.com/Arcadia-1/EVAS/issues/42.
