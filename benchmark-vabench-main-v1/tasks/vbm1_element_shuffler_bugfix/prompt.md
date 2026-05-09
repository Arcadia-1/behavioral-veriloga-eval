The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module element_shuffler(clk, rst_n, out0, out1, out2, out3);
    input clk, rst_n, out0, out1, out2; output out3;
    electrical clk, rst_n, out0, out1, out2, out3;
    analog begin V(out3) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `element_shuffler`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, out0, out1, out2, out3`.
Behavior: cycle through a deterministic non-monotonic one-hot order. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n out0 out1 out2 out3`.

Return exactly one complete Verilog-A code block for module `element_shuffler`.
