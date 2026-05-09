Write a pure Verilog-A `segmented_dac` DUT and a minimal Spectre testbench.

Required module: `segmented_dac`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, t0, t1, t2, vref, vss, aout`.
Behavior: combine binary and unary segments into a monotonic analog output. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=150n maxstep=500p` and saves waveform columns `b0 b1 t0 t1 t2 vref vss aout`.

Testbench requirements: include `segmented_dac.va`, instantiate the DUT with positional port order `(b0 b1 t0 t1 t2 vref vss aout)`, save `b0 b1 t0 t1 t2 vref vss aout`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
