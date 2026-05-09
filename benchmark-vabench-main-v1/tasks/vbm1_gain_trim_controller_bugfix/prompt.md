The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module gain_trim_controller(clk, rst, meas, target, gain_ctrl);
    input clk, rst, meas, target; output gain_ctrl;
    electrical clk, rst, meas, target, gain_ctrl;
    analog begin V(gain_ctrl) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `gain_trim_controller`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, meas, target, gain_ctrl`.
Behavior: move gain control toward a target measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `clk rst meas target gain_ctrl`.

Return exactly one complete Verilog-A code block for module `gain_trim_controller`.
