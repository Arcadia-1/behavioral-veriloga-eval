Create only the DUT Verilog-A model for the `strongarm_comparator_behavior` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `cmp_strongarm`.
Ports, all `electrical`, exactly as named and ordered:
`CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, `VDD`.

Behavior:
- Detect the rising edge of `CLK`.
- When `VINP > VINN`, drive `DCMPP` high and `DCMPN` low.
- When `VINP < VINN`, drive `DCMPP` low and `DCMPN` high.
- Clear or deassert the decision outputs on the falling clock edge.
- Use voltage-domain contributions and `transition(...)`; do not use current contributions.

Public evaluation contract:
- The fixed harness runs `tran tran stop=4n maxstep=5p`.
- Public waveform columns include `clk`, `vinp`, `vinn`, `out_p`, `out_n`.

Return exactly one complete Verilog-A code block for `cmp_strongarm.va`.
