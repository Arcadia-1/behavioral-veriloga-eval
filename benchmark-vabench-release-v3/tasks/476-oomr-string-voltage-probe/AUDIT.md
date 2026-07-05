# Audit: OOMR String Voltage Probe

- Task id: `v3_476_oomr_string_voltage_probe`
- Category: `veriloga_oomr_semantics`
- Scope: Verilog-A semantic/support row for string out-of-module voltage probes.
- Public behavior: `V(sigpath)` resolves the default `$root.vin` path and drives `out` through the required transition.
- Review note: the task intentionally has no ordinary electrical input port; bypassing the string OOMR probe is outside the contract.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
