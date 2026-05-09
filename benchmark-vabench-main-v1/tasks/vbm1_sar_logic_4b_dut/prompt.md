Create only the DUT Verilog-A model for the `sar_logic_4b` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `sar_logic_4b`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLKS`, `DCOMP`, `DP_DAC_3`, `DP_DAC_2`, `DP_DAC_1`, `DP_DAC_0`, `RDY`.

Behavior:
- Implement a 4-bit SAR control sequence driven by rising edges of `CLKS`.
- Start each conversion by asserting the MSB trial bit.
- On each bit phase, keep or clear the current trial bit from `DCOMP`, then assert the next lower trial bit.
- After four bit decisions, assert `RDY` for one cycle and then start a new conversion.
- Drive all outputs with voltage-domain `transition(...)`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=1.2u maxstep=2n`.
- Public waveform columns include `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.


Return exactly one complete Verilog-A code block for `sar_logic_4b.va`.
