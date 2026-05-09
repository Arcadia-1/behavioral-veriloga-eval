The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module precision_rectifier(vin, vout);
    input vin; output vout;
    electrical vin, vout;
    analog begin V(vout) <+ transition(V(vin), 0, 500p, 500p); end
endmodule

```

Required module: `precision_rectifier`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: drive only the positive part of the input waveform. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `vin vout`.

Return exactly one complete Verilog-A code block for module `precision_rectifier`.
