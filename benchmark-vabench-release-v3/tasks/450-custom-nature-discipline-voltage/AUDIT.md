# Audit: Custom Nature Discipline Voltage

- Task id: `v3_450_custom_nature_discipline_voltage`
- Category: `verilogams_discipline_semantics`
- Scope: Verilog-AMS semantic/support row for custom nature and discipline declarations.
- Public behavior: `V(y)` follows `V(a)` through ports declared on the custom `v3electrical` discipline.
- Review note: starter and public testbenches use the same custom-discipline module interface as the solution.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. Spectre reports only the shared `VACOMP-2435` environment notice.
