Create only the DUT Verilog-A model for `element_shuffler`. Do not generate a testbench.

Required module: `element_shuffler`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, out0, out1, out2, out3`.
Behavior: cycle through a deterministic non-monotonic one-hot order. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n out0 out1 out2 out3`.

Return exactly one complete Verilog-A code block for `element_shuffler.va`.
