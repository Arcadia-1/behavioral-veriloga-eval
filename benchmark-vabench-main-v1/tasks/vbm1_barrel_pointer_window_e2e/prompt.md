Write a pure Verilog-A `barrel_pointer_window` DUT and a minimal Spectre testbench.

Required module: `barrel_pointer_window`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, win0, win1, win2, win3`.
Behavior: rotate a two-element adjacent selection window. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n win0 win1 win2 win3`.

Testbench requirements: include `barrel_pointer_window.va`, instantiate the DUT with positional port order `(clk rst_n win0 win1 win2 win3)`, save `clk rst_n win0 win1 win2 win3`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
