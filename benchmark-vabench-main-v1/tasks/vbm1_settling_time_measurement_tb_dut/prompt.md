Create only the DUT Verilog-A model for `settling_time_measurement_tb`. Do not generate a testbench.

Required module: `settling_time_measurement_tb`. Ports, all `electrical`, exactly as named and ordered: `step, vout, done`.
Behavior: stimulate and expose a settling response for measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `step vout done`.

Return exactly one complete Verilog-A code block for `settling_time_measurement_tb.va`.
