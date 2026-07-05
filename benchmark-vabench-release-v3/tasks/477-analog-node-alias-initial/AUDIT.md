# Audit: Analog Node Alias Initial

- Task id: `v3_477_analog_node_alias_initial`
- Category: `veriloga_alias_semantics`
- Scope: Verilog-A semantic/support row for `analog initial` node aliasing.
- Public behavior: `$analog_node_alias(aliased, target_path)` maps the internal node to the default `$root.vin` path, and `out` follows `V(aliased)`.
- Review note: the task intentionally has no ordinary electrical input port; bypassing the alias feature is outside the contract.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
