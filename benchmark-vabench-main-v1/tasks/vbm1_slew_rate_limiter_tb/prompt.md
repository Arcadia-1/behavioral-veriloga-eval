Given a voltage-domain DUT module `slew_rate_limiter`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `slew_rate_limiter.va`. Positional port order: `(vin vout)`.

Required module: `slew_rate_limiter`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: limit output slew rate while tracking the input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `vin vout`.

Return exactly one fenced `spectre` code block.
