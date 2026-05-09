Write a pure Verilog-A `element_shuffler` DUT and a minimal Spectre testbench.

Required module: `element_shuffler`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, out0, out1, out2, out3`.
Behavior: cycle through a deterministic non-monotonic one-hot order. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n out0 out1 out2 out3`.

Testbench requirements: include `element_shuffler.va`, instantiate the DUT with positional port order `(clk rst_n out0 out1 out2 out3)`, save `clk rst_n out0 out1 out2 out3`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
