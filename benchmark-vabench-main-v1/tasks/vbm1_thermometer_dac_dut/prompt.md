Create only the DUT Verilog-A model for `thermometer_dac_4b`. Do not generate a testbench.

Required module: `thermometer_dac_4b`. Ports, all `electrical`, exactly as named and ordered: `code_0`, `code_1`, `code_2`, `code_3`, `vref`, `vss`, `aout`.
Behavior: decode the 4-bit public input code and drive a monotonic analog output equal to `code / 15 * (vref-vss)` above `vss`, representing a unary/thermometer DAC abstraction. Use voltage-domain contributions and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=165n maxstep=500p`; public waveform columns are `code_0`, `code_1`, `code_2`, `code_3`, and `aout`.

Return exactly one complete Verilog-A code block for `thermometer_dac_4b.va`.
