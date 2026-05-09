Create only the DUT Verilog-A model for the `offset_comparator` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

Behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against the public real parameter `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=28n maxstep=20p`.
- Public waveform columns are `CLK`, `VINP`, `VINN`, and `OUT_P`.

Return exactly one complete Verilog-A code block for `cmp_offset_ref.va`.
