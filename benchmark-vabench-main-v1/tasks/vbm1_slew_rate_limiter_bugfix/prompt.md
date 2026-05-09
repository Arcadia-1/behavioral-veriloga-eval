The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module slew_rate_limiter(vin, vout);
    input vin; output vout;
    electrical vin, vout;
    analog begin V(vout) <+ transition(V(vin), 0, 500p, 500p); end
endmodule

```

Required module: `slew_rate_limiter`. Ports, all `electrical`, exactly as named and ordered: `vin, vout`.
Behavior: limit output slew rate while tracking the input. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=160n maxstep=500p` and saves waveform columns `vin vout`.

Return exactly one complete Verilog-A code block for module `slew_rate_limiter`.
