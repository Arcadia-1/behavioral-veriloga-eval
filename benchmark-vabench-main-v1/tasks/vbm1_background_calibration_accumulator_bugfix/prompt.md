The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module background_calibration_accumulator(clk, rst, err, accum);
    input clk, rst, err; output accum;
    electrical clk, rst, err, accum;
    analog begin V(accum) <+ transition(V(clk), 0, 500p, 500p); end
endmodule

```

Required module: `background_calibration_accumulator`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, accum`.
Behavior: slowly accumulate signed background error with saturation. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err accum`.

Return exactly one complete Verilog-A code block for module `background_calibration_accumulator`.
