Create only the DUT Verilog-A model for the `pfd_reset_race` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `pfd_updn`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

Behavior:
- Rising edge of `REF` asserts `UP`.
- Rising edge of `DIV` asserts `DN`.
- If both states become high, reset both outputs promptly so `UP` and `DN` do not significantly overlap.
- Use `@(cross(...))` and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Public waveform columns are `ref`, `div`, `up`, and `dn`.

Return exactly one complete Verilog-A code block for `pfd_updn.va`.
