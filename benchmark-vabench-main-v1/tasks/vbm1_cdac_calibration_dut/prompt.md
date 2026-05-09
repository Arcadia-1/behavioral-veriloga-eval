Create only the DUT Verilog-A model for `cdac_calibration`. Do not generate a testbench.

Required module: `cdac_calibration`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, trim`.
Behavior: accumulate comparator error into a bounded CDAC trim voltage. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err trim`.

Return exactly one complete Verilog-A code block for `cdac_calibration.va`.
