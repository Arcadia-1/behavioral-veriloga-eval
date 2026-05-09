Create only the DUT Verilog-A model for `thermometer_decoder_guarded`. Do not generate a testbench.

Required module: `thermometer_decoder_guarded`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, en, th0, th1, th2, th3`.
Behavior: decode a guarded binary input into thermometer outputs. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `b0 b1 en th0 th1 th2 th3`.

Return exactly one complete Verilog-A code block for `thermometer_decoder_guarded.va`.
