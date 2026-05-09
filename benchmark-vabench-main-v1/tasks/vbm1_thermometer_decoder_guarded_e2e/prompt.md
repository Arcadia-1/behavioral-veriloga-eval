Write a pure Verilog-A `thermometer_decoder_guarded` DUT and a minimal Spectre testbench.

Required module: `thermometer_decoder_guarded`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, en, th0, th1, th2, th3`.
Behavior: decode a guarded binary input into thermometer outputs. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `b0 b1 en th0 th1 th2 th3`.

Testbench requirements: include `thermometer_decoder_guarded.va`, instantiate the DUT with positional port order `(b0 b1 en th0 th1 th2 th3)`, save `b0 b1 en th0 th1 th2 th3`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
