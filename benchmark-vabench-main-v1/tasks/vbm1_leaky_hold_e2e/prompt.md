Write a pure Verilog-A `leaky_hold` DUT and a minimal Spectre testbench.

Required module: `leaky_hold`. Ports, all `electrical`, exactly as named and ordered: `sample, rst, vout`.
Behavior: sample a value and decay it slowly until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=170n maxstep=500p` and saves waveform columns `sample rst vout`.

Testbench requirements: include `leaky_hold.va`, instantiate the DUT with positional port order `(sample rst vout)`, save `sample rst vout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
