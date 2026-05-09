Given a voltage-domain DUT module `peak_detector`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `peak_detector.va`. Positional port order: `(vin rst vout)`.

Required module: `peak_detector`. Ports, all `electrical`, exactly as named and ordered: `vin, rst, vout`.
Behavior: track and hold the maximum input value until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vin rst vout`.

Return exactly one fenced `spectre` code block.
