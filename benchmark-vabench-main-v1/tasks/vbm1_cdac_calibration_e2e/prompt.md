Write a pure Verilog-A `cdac_calibration` DUT and a minimal Spectre testbench.

Required module: `cdac_calibration`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, trim`.
Behavior: accumulate comparator error into a bounded CDAC trim voltage. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err trim`.

Testbench requirements: include `cdac_calibration.va`, instantiate the DUT with positional port order `(clk rst err trim)`, save `clk rst err trim`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
