The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module file_metric_writer(vin, done);
    input vin; output done;
    electrical vin, done;
    analog begin V(done) <+ transition(V(vin), 0, 500p, 500p); end
endmodule

```

Required module: `file_metric_writer`. Ports, all `electrical`, exactly as named and ordered: `vin, done`.
Behavior: open a public string-parameter file and expose a completion waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=90n maxstep=500p` and saves waveform columns `vin done`.

Return exactly one complete Verilog-A code block for module `file_metric_writer`.
