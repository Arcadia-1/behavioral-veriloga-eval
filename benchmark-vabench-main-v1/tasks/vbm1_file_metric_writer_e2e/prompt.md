Write a pure Verilog-A `file_metric_writer` DUT and a minimal Spectre testbench.

Required module: `file_metric_writer`. Ports, all `electrical`, exactly as named and ordered: `vin, done`.
Behavior: open a public string-parameter file and expose a completion waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=90n maxstep=500p` and saves waveform columns `vin done`.

Testbench requirements: include `file_metric_writer.va`, instantiate the DUT with positional port order `(vin done)`, save `vin done`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
