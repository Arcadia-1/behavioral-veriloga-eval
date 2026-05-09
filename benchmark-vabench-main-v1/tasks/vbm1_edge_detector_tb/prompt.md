Given a voltage-domain DUT module `edge_detector`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `edge_detector.va`. Positional port order: `(sig rst_n pulse)`.

Required module: `edge_detector`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, pulse`.
Behavior: emit a short pulse on rising input edges. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `sig rst_n pulse`.

Return exactly one fenced `spectre` code block.
