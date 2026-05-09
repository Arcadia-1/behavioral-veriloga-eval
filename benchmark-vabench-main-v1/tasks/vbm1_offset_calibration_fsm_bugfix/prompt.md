The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module offset_calibration_fsm(clk, rst, comp, trim);
    input clk, rst, comp; output trim;
    electrical clk, rst, comp, trim;
    analog begin V(trim) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `offset_calibration_fsm`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, comp, trim`.
Behavior: update trim state on clock edges using comparator polarity. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst comp trim`.

Return exactly one complete Verilog-A code block for module `offset_calibration_fsm`.
