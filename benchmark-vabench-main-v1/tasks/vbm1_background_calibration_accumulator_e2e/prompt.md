Write a pure Verilog-A `background_calibration_accumulator` DUT and a minimal Spectre testbench.

Required module: `background_calibration_accumulator`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, accum`.
Behavior: slowly accumulate signed background error with saturation. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err accum`.

Testbench requirements: include `background_calibration_accumulator.va`, instantiate the DUT with positional port order `(clk rst err accum)`, save `clk rst err accum`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
