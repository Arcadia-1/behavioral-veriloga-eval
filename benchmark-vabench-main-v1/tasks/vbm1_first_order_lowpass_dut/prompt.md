Create only the DUT Verilog-A model for `first_order_lowpass`. Do not generate a testbench.

Required module: `first_order_lowpass`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: implement a first-order low-pass response. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `vin vout`.

Return exactly one complete Verilog-A code block for `first_order_lowpass.va`.
