Write a pure Verilog-A `rotating_element_selector` DUT and a minimal Spectre testbench.

Required module: `rotating_element_selector`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, sel0, sel1, sel2, sel3`.
Behavior: rotate a one-hot element-selection pointer. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n sel0 sel1 sel2 sel3`.

Testbench requirements: include `rotating_element_selector.va`, instantiate the DUT with positional port order `(clk rst_n sel0 sel1 sel2 sel3)`, save `clk rst_n sel0 sel1 sel2 sel3`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
