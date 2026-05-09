Given a voltage-domain DUT module `file_metric_writer`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `file_metric_writer.va`. Positional port order: `(vin done)`.

Required module: `file_metric_writer`. Ports, all `electrical`, exactly as named and ordered: `vin, done`.
Behavior: open a public string-parameter file and expose a completion waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=90n maxstep=500p` and saves waveform columns `vin done`.

Return exactly one fenced `spectre` code block.
