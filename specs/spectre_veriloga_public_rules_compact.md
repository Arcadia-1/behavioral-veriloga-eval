Use Spectre-compatible Verilog-A/Spectre only.

Verilog-A DUT rules:
- Separate direction and discipline declarations: `input a; output y; electrical a, y;`.
- Do not use `reg`, `wire`, `logic`, `always`, `initial`, digital bit literals, scalar bit-select assignment, or SystemVerilog `#(...)` module parameters.
- Put state initialization inside `analog begin @(initial_step) ... end`.
- Use `@(cross(...))` for events. Do not place `cross()` or `transition()` inside conditional branches.
- Do not write empty branches such as `end else if (...) end`; remove them or add real `begin ... end` statements.
- Avoid dynamic analog vector indices, embedded declarations after statements, parameter names that shadow ports, invalid `from` ranges, and direct filename arguments to `$fwrite/$fstrobe/$fdisplay`.

Spectre testbench rules:
- Use `simulator lang=spectre`, `global 0`, `vsource`, `tran`, `save`, and `ahdl_include` only unless the prompt requires more.
- Instance syntax is `Xname (nodes...) module_name`; do not use named-port or colon instance syntax.
- Continue multiline source/instance statements with `\`, or keep `wave=[t0 v0 ...]` on one line.
- PWL times must be strictly increasing; pulse rise/fall must be positive.
