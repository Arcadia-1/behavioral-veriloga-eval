Write a pure Verilog-A `settling_time_measurement_tb` DUT and a minimal Spectre testbench.

Required module: `settling_time_measurement_tb`. Ports, all `electrical`, exactly as named and ordered: `step, vout, done`.
Behavior: stimulate and expose a settling response for measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `step vout done`.

Testbench requirements: include `settling_time_measurement_tb.va`, instantiate the DUT with positional port order `(step vout done)`, save `step vout done`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
