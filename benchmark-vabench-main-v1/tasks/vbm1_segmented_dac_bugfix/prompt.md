The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module segmented_dac(b0, b1, t0, t1, t2, vref, vss, aout);
    input b0, b1, t0, t1, t2, vref, vss; output aout;
    electrical b0, b1, t0, t1, t2, vref, vss, aout;
    analog begin V(aout) <+ transition(V(b0), 0, 500p, 500p); end
endmodule

```

Required module: `segmented_dac`. Ports, all `electrical`, exactly as named and ordered: `b0, b1, t0, t1, t2, vref, vss, aout`.
Behavior: combine binary and unary segments into a monotonic analog output. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=150n maxstep=500p` and saves waveform columns `b0 b1 t0 t1 t2 vref vss aout`.

Return exactly one complete Verilog-A code block for module `segmented_dac`.
