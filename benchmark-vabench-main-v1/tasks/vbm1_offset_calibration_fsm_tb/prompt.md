Given a voltage-domain DUT module `offset_calibration_fsm`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `offset_calibration_fsm.va`. Positional port order: `(clk rst comp trim)`.

Required module: `offset_calibration_fsm`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, comp, trim`.
Behavior: update trim state on clock edges using comparator polarity. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst comp trim`.

Return exactly one fenced `spectre` code block.
