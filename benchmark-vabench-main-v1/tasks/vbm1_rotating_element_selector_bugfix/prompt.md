The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module rotating_element_selector(clk, rst_n, sel0, sel1, sel2, sel3);
    input clk, rst_n, sel0, sel1, sel2; output sel3;
    electrical clk, rst_n, sel0, sel1, sel2, sel3;
    analog begin V(sel3) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `rotating_element_selector`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, sel0, sel1, sel2, sel3`.
Behavior: rotate a one-hot element-selection pointer. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n sel0 sel1 sel2 sel3`.

Return exactly one complete Verilog-A code block for module `rotating_element_selector`.
