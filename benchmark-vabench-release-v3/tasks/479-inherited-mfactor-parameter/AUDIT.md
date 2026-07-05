# Audit: Inherited Mfactor Parameter

- Task id: `v3_479_inherited_mfactor_parameter`
- Category: `veriloga_mfactor_semantics`
- Scope: Verilog-A semantic/support row for the `(* inherited_mfactor *)` parameter attribute.
- Public behavior: the public parameter `m` supplies the voltage gain from `in` to `out`.
- Review note: the model must use the effective parameter value and must not hard-code the gain.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
