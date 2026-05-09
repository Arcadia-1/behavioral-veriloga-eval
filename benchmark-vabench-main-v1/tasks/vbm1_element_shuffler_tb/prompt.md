Given a voltage-domain DUT module `element_shuffler`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `element_shuffler.va`. Positional port order: `(clk rst_n out0 out1 out2 out3)`.

Required module: `element_shuffler`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, out0, out1, out2, out3`.
Behavior: cycle through a deterministic non-monotonic one-hot order. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n out0 out1 out2 out3`.

Return exactly one fenced `spectre` code block.
