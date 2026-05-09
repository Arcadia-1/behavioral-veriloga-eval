Create only the DUT Verilog-A model for `peak_detector`. Do not generate a testbench.

Required module: `peak_detector`. Ports, all `electrical`, exactly as named and ordered: `vin, rst, vout`.
Behavior: track and hold the maximum input value until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vin rst vout`.

Return exactly one complete Verilog-A code block for `peak_detector.va`.
