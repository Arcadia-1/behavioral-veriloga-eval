The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module settling_time_measurement_tb(step, vout, done);
    input step, vout; output done;
    electrical step, vout, done;
    analog begin V(done) <+ transition(V(step), 0, 500p, 500p); end
endmodule

```

Required module: `settling_time_measurement_tb`. Ports, all `electrical`, exactly as named and ordered: `step, vout, done`.
Behavior: stimulate and expose a settling response for measurement. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `step vout done`.

Return exactly one complete Verilog-A code block for module `settling_time_measurement_tb`.
