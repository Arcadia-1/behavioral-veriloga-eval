# Audit: Table Model 2D Array Surface

- Task id: `v3_487_table_model_2d_array_surface`
- Category: `veriloga_table_model_semantics`
- Scope: Verilog-A semantic/support row for a 2D array-backed `$table_model()` surface.
- Public behavior: four public `(x,y,z)` surface points are initialized in arrays and evaluated with `$table_model(V(xnode), V(ynode), x, y, z, "1L,1L")`.
- Review note: the table helper is part of the public contract; replacing it with a manually coded surface is outside the task.
- Validation: Rust EVAS gold/negative, targeted Spectre visible/hidden gold, and AHDL read-in triage pass. EVAS AHDL-like `W5007` is triaged against real Spectre read-in; Spectre reports only the shared `VACOMP-2435` environment notice.
