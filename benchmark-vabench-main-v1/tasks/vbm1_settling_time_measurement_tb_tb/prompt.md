Given a voltage-domain DUT module `settling_time_measurement_tb`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `settling_time_measurement_tb.va`. Positional port order: `(step vout done)`.

Required module: `settling_time_measurement_tb`. Ports, all `electrical`, exactly as named and ordered: `step, vout, done`.
Behavior: stimulate and expose a settling response for measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `step vout done`.

Return exactly one fenced `spectre` code block.
