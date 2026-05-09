The following module is not a SAR sequencer; it only mirrors `DCOMP` onto one output.
Fix it without changing the public module name or ports.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"

module sar_logic_4b(VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY);
    inout VDD, VSS;
    input CLKS, DCOMP;
    output DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;
    electrical VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY;
    analog begin
        V(DP_DAC_3) <+ transition(V(DCOMP), 0, 1n, 1n);
        V(DP_DAC_2) <+ 0;
        V(DP_DAC_1) <+ 0;
        V(DP_DAC_0) <+ 0;
        V(RDY) <+ 0;
    end
endmodule

```

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


Return exactly one complete Verilog-A code block for module `sar_logic_4b`.
