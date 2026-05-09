The following implementation is intentionally wrong because it only mirrors its first input. Fix the behavior without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module leaky_hold(sample, rst, vout);
    input sample, rst; output vout;
    electrical sample, rst, vout;
    analog begin V(vout) <+ transition(V(sample), 0, 500p, 500p); end
endmodule

```

Required module: `leaky_hold`. Ports, all `electrical`, exactly as named and ordered: `sample, rst, vout`.
Behavior: sample a value and decay it slowly until reset. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=170n maxstep=500p` and saves waveform columns `sample rst vout`.

Return exactly one complete Verilog-A code block for module `leaky_hold`.
