The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module thermometer_decoder_guarded(b0, b1, en, th0, th1, th2, th3);
    input b0, b1, en, th0, th1, th2; output th3;
    electrical b0, b1, en, th0, th1, th2, th3;
    analog begin V(th3) <+ transition(V(b0), 0, 500p, 500p); end
endmodule

```

Required module: `thermometer_decoder_guarded`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, en, th0, th1, th2, th3`.
Behavior: decode a guarded binary input into thermometer outputs. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=120n maxstep=500p` and saves waveform columns `b0 b1 en th0 th1 th2 th3`.

Return exactly one complete Verilog-A code block for module `thermometer_decoder_guarded`.
