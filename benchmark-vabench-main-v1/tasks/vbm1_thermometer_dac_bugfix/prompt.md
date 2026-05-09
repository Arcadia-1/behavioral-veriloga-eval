The following DAC is wrong because it only mirrors `code_0`. Fix it without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module thermometer_dac_4b(code_0, code_1, code_2, code_3, vref, vss, aout);
    input code_0, code_1, code_2, code_3, vref, vss; output aout; electrical code_0, code_1, code_2, code_3, vref, vss, aout;
    analog begin V(aout, vss) <+ transition(V(code_0), 0, 500p, 500p); end
endmodule

```

Required module: `thermometer_dac_4b`. Ports, all `electrical`, exactly as named and ordered: `code_0`, `code_1`, `code_2`, `code_3`, `vref`, `vss`, `aout`.
Behavior: decode the 4-bit public input code and drive a monotonic analog output equal to `code / 15 * (vref-vss)` above `vss`, representing a unary/thermometer DAC abstraction. Use voltage-domain contributions and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=165n maxstep=500p`; public waveform columns are `code_0`, `code_1`, `code_2`, `code_3`, and `aout`.

Return exactly one complete Verilog-A code block for module `thermometer_dac_4b`.
