Create only the DUT Verilog-A model for `offset_calibration_fsm`. Do not generate a testbench.

Required module: `offset_calibration_fsm`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, comp, trim`.
Behavior: update trim state on clock edges using comparator polarity. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst comp trim`.

Return exactly one complete Verilog-A code block for `offset_calibration_fsm.va`.
