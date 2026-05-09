Create only the DUT Verilog-A model for `rotating_element_selector`. Do not generate a testbench.

Required module: `rotating_element_selector`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, sel0, sel1, sel2, sel3`.
Behavior: rotate a one-hot element-selection pointer. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n sel0 sel1 sel2 sel3`.

Return exactly one complete Verilog-A code block for `rotating_element_selector.va`.
