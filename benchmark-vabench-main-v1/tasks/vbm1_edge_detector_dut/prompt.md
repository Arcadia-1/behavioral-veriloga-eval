Create only the DUT Verilog-A model for `edge_detector`. Do not generate a testbench.

Required module: `edge_detector`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, pulse`.
Behavior: emit a short pulse on rising input edges. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `sig rst_n pulse`.

Return exactly one complete Verilog-A code block for `edge_detector.va`.
