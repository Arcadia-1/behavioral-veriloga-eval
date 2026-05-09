Given a voltage-domain DUT module `segmented_dac`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `segmented_dac.va`. Positional port order: `(b0 b1 t0 t1 t2 vref vss aout)`.

Required module: `segmented_dac`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, t0, t1, t2, vref, vss, aout`.
Behavior: combine binary and unary segments into a monotonic analog output. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=150n maxstep=500p` and saves waveform columns `b0 b1 t0 t1 t2 vref vss aout`.

Return exactly one fenced `spectre` code block.
