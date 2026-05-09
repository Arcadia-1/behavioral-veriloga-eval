Write a pure Verilog-A `offset_calibration_fsm` DUT and a minimal Spectre testbench.

Required module: `offset_calibration_fsm`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, comp, trim`.
Behavior: update trim state on clock edges using comparator polarity. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst comp trim`.

Testbench requirements: include `offset_calibration_fsm.va`, instantiate the DUT with positional port order `(clk rst comp trim)`, save `clk rst comp trim`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
