Given a voltage-domain DUT module `gain_trim_controller`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `gain_trim_controller.va`. Positional port order: `(clk rst meas target gain_ctrl)`.

Required module: `gain_trim_controller`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, meas, target, gain_ctrl`.
Behavior: move gain control toward a target measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `clk rst meas target gain_ctrl`.

Return exactly one fenced `spectre` code block.
