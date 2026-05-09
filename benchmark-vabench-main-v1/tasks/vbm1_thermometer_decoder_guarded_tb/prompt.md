Given a voltage-domain DUT module `thermometer_decoder_guarded`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `thermometer_decoder_guarded.va`. Positional port order: `(b0 b1 en th0 th1 th2 th3)`.

Required module: `thermometer_decoder_guarded`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, en, th0, th1, th2, th3`.
Behavior: decode a guarded binary input into thermometer outputs. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `b0 b1 en th0 th1 th2 th3`.

Return exactly one fenced `spectre` code block.
