The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module barrel_pointer_window(clk, rst_n, win0, win1, win2, win3);
    input clk, rst_n, win0, win1, win2; output win3;
    electrical clk, rst_n, win0, win1, win2, win3;
    analog begin V(win3) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `barrel_pointer_window`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, win0, win1, win2, win3`.
Behavior: rotate a two-element adjacent selection window. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n win0 win1 win2 win3`.

Return exactly one complete Verilog-A code block for module `barrel_pointer_window`.
