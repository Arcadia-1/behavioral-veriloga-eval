# Audit: Table Model String Param Source

- Task id: `v3_488_table_model_string_param_source`
- Category: `veriloga_table_model_semantics`
- Scope: Verilog-A semantic/support row for `$table_model()` file selection through a string parameter.
- Public behavior: `tmdata` names the supplied `gain_profile.tbl` table used by `$table_model(V(in), tmdata, "1L")`.
- Review note: the support table is part of the harness contract and must be available at simulation time.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
