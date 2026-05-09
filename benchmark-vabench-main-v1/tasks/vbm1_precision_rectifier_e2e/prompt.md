Write a pure Verilog-A `precision_rectifier` DUT and a minimal Spectre testbench.

Required module: `precision_rectifier`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: drive only the positive part of the input waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `vin vout`.

Testbench requirements: include `precision_rectifier.va`, instantiate the DUT with positional port order `(vin vout)`, save `vin vout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
