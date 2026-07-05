# Audit: Inherited Port Attribute Supply

- Task id: `v3_478_inherited_port_attribute_supply`
- Category: `veriloga_inherited_port_semantics`
- Scope: Verilog-A semantic/support row for inherited supply-port attributes.
- Public behavior: explicit `vdd`/`gnd` ports carry inherited connection attributes while `V(out, gnd)` follows `V(in, gnd)`.
- Review note: current behavior remains voltage-domain only; current/KCL solving is outside this row.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007/W5017` are triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
