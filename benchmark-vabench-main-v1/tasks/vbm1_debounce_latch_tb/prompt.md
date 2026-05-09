Given a voltage-domain DUT module `debounce_latch`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `debounce_latch.va`. Positional port order: `(sig rst_n out)`.

Required module: `debounce_latch`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, out`.
Behavior: ignore short glitches and assert only after a stable high input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=140n maxstep=500p` and saves waveform columns `sig rst_n out`.

Return exactly one fenced `spectre` code block.
