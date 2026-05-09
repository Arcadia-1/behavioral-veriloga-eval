Write a pure Verilog-A `gain_trim_controller` DUT and a minimal Spectre testbench.

Required module: `gain_trim_controller`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, meas, target, gain_ctrl`.
Behavior: move gain control toward a target measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `clk rst meas target gain_ctrl`.

Testbench requirements: include `gain_trim_controller.va`, instantiate the DUT with positional port order `(clk rst meas target gain_ctrl)`, save `clk rst meas target gain_ctrl`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
