# Audit: Mfactor System Function Gain

- Task id: `v3_480_mfactor_system_function_gain`
- Category: `veriloga_mfactor_semantics`
- Scope: Verilog-A semantic/support row for the Cadence `$mfactor` system function.
- Public behavior: the module reads the effective simulator instance multiplicity with `$mfactor` and uses it as the voltage gain from `in` to `out`.
- Review note: the model must use `$mfactor` rather than a public gain parameter or a hard-coded testbench value.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
