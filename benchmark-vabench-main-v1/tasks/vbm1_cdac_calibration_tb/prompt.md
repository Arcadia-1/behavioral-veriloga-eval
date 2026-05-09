Given a voltage-domain DUT module `cdac_calibration`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `cdac_calibration.va`. Positional port order: `(clk rst err trim)`.

Required module: `cdac_calibration`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, trim`.
Behavior: accumulate comparator error into a bounded CDAC trim voltage. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err trim`.

Return exactly one fenced `spectre` code block.
