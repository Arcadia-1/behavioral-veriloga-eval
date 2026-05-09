Write a pure Verilog-A `debounce_latch` DUT and a minimal Spectre testbench.

Required module: `debounce_latch`. Ports, all `electrical`, exactly as named and ordered: `sig, rst_n, out`.
Behavior: ignore short glitches and assert only after a stable high input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=140n maxstep=500p` and saves waveform columns `sig rst_n out`.

Testbench requirements: include `debounce_latch.va`, instantiate the DUT with positional port order `(sig rst_n out)`, save `sig rst_n out`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
