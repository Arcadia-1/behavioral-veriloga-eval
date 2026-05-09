Write a pure Verilog-A `peak_detector` DUT and a minimal Spectre testbench.

Required module: `peak_detector`. Ports, all `electrical`, exactly as named and ordered: `vin, rst, vout`.
Behavior: track and hold the maximum input value until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vin rst vout`.

Testbench requirements: include `peak_detector.va`, instantiate the DUT with positional port order `(vin rst vout)`, save `vin rst vout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
