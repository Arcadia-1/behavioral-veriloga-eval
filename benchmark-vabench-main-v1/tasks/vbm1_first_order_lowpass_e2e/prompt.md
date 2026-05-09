Write a pure Verilog-A `first_order_lowpass` DUT and a minimal Spectre testbench.

Required module: `first_order_lowpass`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: implement a first-order low-pass response. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `vin vout`.

Testbench requirements: include `first_order_lowpass.va`, instantiate the DUT with positional port order `(vin vout)`, save `vin vout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
