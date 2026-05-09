Write a pure Verilog-A `edge_detector` DUT and a minimal Spectre testbench.

Required module: `edge_detector`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, pulse`.
Behavior: emit a short pulse on rising input edges. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `sig rst_n pulse`.

Testbench requirements: include `edge_detector.va`, instantiate the DUT with positional port order `(sig rst_n pulse)`, save `sig rst_n pulse`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
