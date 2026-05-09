Write a pure Verilog-A `slew_rate_limiter` DUT and a minimal Spectre testbench.

Required module: `slew_rate_limiter`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: limit output slew rate while tracking the input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `vin vout`.

Testbench requirements: include `slew_rate_limiter.va`, instantiate the DUT with positional port order `(vin vout)`, save `vin vout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
