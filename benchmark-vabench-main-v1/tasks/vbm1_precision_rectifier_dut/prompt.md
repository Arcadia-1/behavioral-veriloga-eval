Create only the DUT Verilog-A model for `precision_rectifier`. Do not generate a testbench.

Required module: `precision_rectifier`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: drive only the positive part of the input waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `vin vout`.

Return exactly one complete Verilog-A code block for `precision_rectifier.va`.
