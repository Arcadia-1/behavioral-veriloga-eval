Given a voltage-domain DUT module `leaky_hold`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `leaky_hold.va`. Positional port order: `(sample rst vout)`.

Required module: `leaky_hold`. Ports, all `electrical`, exactly as named and ordered: `sample, rst, vout`.
Behavior: sample a value and decay it slowly until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=170n maxstep=500p` and saves waveform columns `sample rst vout`.

Return exactly one fenced `spectre` code block.
